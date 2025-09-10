import ffmpeg
import os
from typing import List

class FFmpegWrapper:
    def extract_frames(self, video_path: str, output_dir: str) -> List[str]:
        """
        Extrai frames de um vídeo a 1 frame por segundo.
        Retorna uma lista de caminhos para os frames extraídos.
        """
        print(f"Extraindo frames de {video_path} para {output_dir}")
        
        try:
            (
                ffmpeg
                .input(video_path)
                .filter('fps', fps='1')
                .output(os.path.join(output_dir, 'frame_%04d.png'), start_number=0)
                .run(capture_stdout=True, capture_stderr=True, quiet=True)
            )
        except ffmpeg.Error as e:
            import traceback
            traceback.print_exc()

            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e

        extracted_files = sorted(
            [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.png')]
        )
        print(f"Extração concluída. {len(extracted_files)} frames gerados.")
        return extracted_files

__all__ = ["FFmpegWrapper"]
