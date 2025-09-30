import boto3
import time
from typing import Dict, Any
from botocore.exceptions import ClientError

from src.core.ports.cloud.content_moderation_gateway import ContentModerationGateway

class RekognitionContentModerationGateway(ContentModerationGateway):
    """
    Implementação do gateway de moderação de conteúdo usando Rekognition da AWS
    """
    
    def __init__(self, region_name: str = 'us-east-1', moderation_threshold: float = 50.0):
        self.rekognition_client = boto3.client('rekognition', region_name=region_name)
        self.moderation_threshold = moderation_threshold
        
    def moderate_video_content(self, bucket: str, video_key: str) -> Dict[str, Any]:
        """
        Analisa o conteúdo de um vídeo usando Rekognition da AWS
        """
        try:
            print(f"Iniciando moderação de conteúdo para: s3://{bucket}/{video_key}")
            
            response = self.rekognition_client.start_content_moderation(
                Video={ 'S3Object': { 'Bucket': bucket, 'Name': video_key } },
                MinConfidence=self.moderation_threshold
            )
            
            job_id = response['JobId']
            print(f"Job de moderação iniciado: {job_id}")

            result = self._wait_for_job_completion(job_id)
            moderation_result = self._process_moderation_results(result, job_id)
            
            print(f"Moderação concluída. Conteúdo apropriado: {moderation_result['is_appropriate']}")
            
            return moderation_result
            
        except ClientError as e:
            error_msg = f"Erro ao analisar conteúdo do vídeo: {e}"
            print(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado na moderação: {e}"
            print(error_msg)
            raise Exception(error_msg)
    
    def _wait_for_job_completion(self, job_id: str, max_wait_time: int = 300) -> Dict[str, Any]:
        """
        Aguarda a conclusão do job de moderação de conteúdo
        """
        start_time = time.time()
        check_interval = 10
        
        print(f"Aguardando conclusão do job: {job_id}")
        while time.time() - start_time < max_wait_time:
            try:
                response = self.rekognition_client.get_content_moderation(JobId=job_id)
                status = response['JobStatus']
                
                print(f"Status do job {job_id}: {status}")
                
                if status == 'SUCCEEDED':
                    print(f"Job {job_id} concluído com sucesso")
                    return response
                elif status == 'FAILED':
                    error_msg = f"Job de moderação falhou: {response.get('StatusMessage', 'Erro desconhecido')}"
                    print(error_msg)
                    raise Exception(error_msg)
                
                # Aguarda antes de verificar novamente
                time.sleep(check_interval)
                
            except ClientError as e:
                error_msg = f"Erro ao verificar status do job {job_id}: {e}"
                print(error_msg)
                # Se o tipo do video for incompativel, deve prosseguir sem analisar até tratarmos o problema.
                if e.response['Error']['Code'] == 'InvalidParameterException':
                    print("Tipo de vídeo incompatível. Prosseguindo sem moderação.")
                    return {
                        "is_appropriate": True,
                        "confidence": 0.0,
                        "labels": [],
                        "job_id": job_id,
                        "total_labels_found": 0
                    }
                raise Exception(error_msg)
        
        timeout_msg = f"Timeout aguardando conclusão do job de moderação: {job_id} (max: {max_wait_time}s)"
        print(timeout_msg)
        raise Exception(timeout_msg)
    
    def _process_moderation_results(self, result: Dict[str, Any], job_id: str) -> Dict[str, Any]:
        """
        Processa os resultados da moderação de conteúdo
        """
        moderation_labels = result.get('ModerationLabels', [])
        
        print(f"Total de labels encontrados: {len(moderation_labels)}")
        
        # Verifica se há conteúdo inadequado
        inappropriate_labels = []
        max_confidence = 0.0
        
        for label_info in moderation_labels:
            label = label_info.get('ModerationLabel', {})
            confidence = label.get('Confidence', 0.0)
            name = label.get('Name', '')
            
            print(f"Label detectado: {name} (confiança: {confidence:.2f}%)")
            
            if confidence >= self.moderation_threshold:
                inappropriate_labels.append({
                    'name': name,
                    'confidence': confidence,
                    'parent_name': label.get('ParentName', '')
                })
                max_confidence = max(max_confidence, confidence)
        
        is_appropriate = len(inappropriate_labels) == 0
        
        print(f"Labels inadequados encontrados: {len(inappropriate_labels)}")
        
        return {
            "is_appropriate": is_appropriate,
            "confidence": max_confidence,
            "labels": inappropriate_labels,
            "job_id": job_id,
            "total_labels_found": len(inappropriate_labels)
        }
