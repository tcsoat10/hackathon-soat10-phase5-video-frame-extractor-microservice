# Video Frame Extractor Microservice - SOAT10 - Pós Tech Arquitetura de Software - FIAP

# Tópicos
- [Descrição do Projeto](#descrição-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Executando o Projeto](#executando-o-projeto)
- [Comunicação com os demais serviços](#comunicação-com-os-demais-serviços)
- [Secrets Necessários](#secrets-necessários)


# Descrição do Projeto

O projeto consiste em um portal onde um usuário autenticado pode enviar um vídeo e receber um arquivo zip contendo os frames de seu vídeo. Este microsserviço é responsável por separar os frames do vídeo enviado.

Esta aplicação é parte de um ecossistema distribuído em seis repositórios, executando inteiramente na AWS, com deploy via Terraform.

 [Topo](#tópicos)

# Tecnologias Utilizadas
- [Python 3.12](https://www.python.org/downloads/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Kubernetes](https://kubernetes.io/)
- [Terraform](https://developer.hashicorp.com/terraform)
- [AWS Elastic Kubernetes Service (EKS)](https://aws.amazon.com/pt/eks/)
- [AWS Elastic Container Registry (ECR)](https://aws.amazon.com/pt/ecr/)
- [AWS Simple Storage Service (S3)](https://aws.amazon.com/pt/s3/)
- [Github Actions](https://github.com/features/actions)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/stable/)

 [Topo](#tópicos)

# Executando o Projeto
Este projeto não é executado localmente. O deploy ocorre automaticamente na AWS via GitHub Actions, fazendo uso do Terraform.

Este projeto está estruturado em seis repositórios:

- 1 - [Infraestrutura](https://github.com/tcsoat10/hackathon-soat10-phase5-eks-infra)
- 2 - [Zipper](https://github.com/tcsoat10/hackathon-soat10-phase5-zipper-microservice)
- 3 - [Frame Extractor](https://github.com/tcsoat10/hackathon-soat10-phase5-video-frame-extractor-microservice)
- 4 - [Authenticator](https://github.com/tcsoat10/hackathon-soat10-phase5-auth-microservice)
- 5 - [API Principal](https://github.com/tcsoat10/hackathon-soat10-phase5-api)
- 6 - [Frontend](https://github.com/tcsoat10/hackathon-soat10-phase5-frontend)

 [Topo](#tópicos)

# Comunicação com os demais serviços

- O deploy da infra Kubernetes é feito em um cluster EKS. Dentro deste cluster, o deploy da aplicação é feito em um pod, e tem seu acesso gerenciado por um Load Balancer.
- A aplicação enxerga o banco de dados disponível e realiza as migrações necessárias.
- Cada serviço tem um bucket S3 que é utilizado como backend do Terraform. Cada serviço que necessite de informações de outros serviços busca estas informações em seus respectivos buckets, automatizando o processo de deploy.

 [Topo](#tópicos)

# Secrets Necessários
- AWS_ACCESS_KEY_ID: Access Key ID da conta AWS
- AWS_ACCOUNT_ID: Account ID da conta AWS
- AWS_SECRET_ACCESS_KEY: Secret Access Key da conta AWS
- AWS_SESSION_TOKEN: token de sessão da conta da AWS, necessário para contas temporárias, como da AWS Academy
- DB_PASSWORD: senha do usuário do banco MongoDB
- DB_ROOT_PASSWORD: senha do usuário root do MongoDB
- DB_USERNAME: usuário do banco MongoDB
- FRAMES_MICROSERVICE_X_API_KEY: chave da API, para validar as requisições recebidas
- REDIS_PASSWORD: senha de acesso ao Redis
- ZIPPER_MICROSERVICE_X_API_KEY: chave da API do microsserviço zipper, para enviar requisições válidas

[Topo](#tópicos)
