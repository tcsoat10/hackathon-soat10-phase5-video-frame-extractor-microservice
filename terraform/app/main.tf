provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc10-phase5-frames-app"
    key    = "application/terraform.tfstate"
    region = "us-east-1" # ajuste para sua região
  }
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster_name
}

provider "kubernetes" {
  host                   = data.terraform_remote_state.aws.outputs.eks_cluster_endpoint
  cluster_ca_certificate = base64decode(data.terraform_remote_state.aws.outputs.eks_cluster_ca)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

resource "kubernetes_service" "frames_app_lb" {
  metadata {
    name      = "frames-app-lb"
    namespace = "default"
  }
  spec {
    selector = {
      app = "frames-app"
    }
    type = "LoadBalancer"
    port {
      port        = 80
      target_port = 8001
    }
  }
}

resource "kubernetes_deployment" "frames_app" {
  depends_on = [kubernetes_service.frames_app_lb]
  metadata {
    name      = "frames-app"
    namespace = "default"
    labels = {
      app = "frames-app"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "frames-app"
      }
    }
    template {
      metadata {
        labels = {
          app = "frames-app"
        }
      }
      spec {
        container {
          name  = "frames-app"
          image = local.application_image
          env{
            name = "MONGO_HOST"
            value = "mongodb"
          }
          env {
            name  = "MONGO_DB"
            value = data.terraform_remote_state.mongo.outputs.mongo_db
          }
          env {
            name  = "MONGO_USER"
            value = data.terraform_remote_state.mongo.outputs.mongo_user
          }
          env {
            name  = "MONGO_PASSWORD"
            value = data.terraform_remote_state.mongo.outputs.mongo_password
          }
          env {
            name  = "MONGO_PORT"
            value = var.mongo_port
          }
          env {
            name  = "MONGO_URI"
            value = data.terraform_remote_state.mongo.outputs.mongo_uri
          }
          env {
            name  = "ZIPPER_SERVICE_URL"
            value = data.terraform_remote_state.zipper.outputs.zipper_app_lb_endpoint
          }
          env {
            name  = "ZIPPER_SERVICE_X_API_KEY"
            value = var.zipper_api_key
          }
          env {
            name  = "VIDEO_FRAME_EXTRACTOR_MICROSERVICE_X_API_KEY"
            value = var.frames_api_key
          }
          env {
            name  = "MONGO_URI"
            value = data.terraform_remote_state.mongo.outputs.mongo_uri            
          }
          env {
            name  = "REDIS_HOST"
            value = data.terraform_remote_state.redis.outputs.redis_host
          }
          env {
            name  = "REDIS_PORT"
            value = data.terraform_remote_state.redis.outputs.redis_port
          }
          env {
            name  = "AUTH_SOURCE"
            value = data.terraform_remote_state.mongo.outputs.mongo_db  # zipper_microservice
          }
          env {
            name  = "MONGO_CONTAINER_NAME"
            value = data.terraform_remote_state.mongo.outputs.mongo_host  # zipper-microservice-mongodb
          }
          env {
            name  = "REDIS_PASSWORD"
            value = data.terraform_remote_state.redis.outputs.redis_password
          }
          env {
            name  = "BROKER_URL"
            value = "redis://:${data.terraform_remote_state.redis.outputs.redis_password}@${data.terraform_remote_state.redis.outputs.redis_host}:${data.terraform_remote_state.redis.outputs.redis_port}/0"
          }
          env {
            name  = "AWS_ACCESS_KEY_ID"
            value = var.aws_access_key_id
          }
          env {
            name  = "AWS_SECRET_ACCESS_KEY"
            value = var.aws_secret_access_key
          }
          env {
            name  = "AWS_SESSION_TOKEN"
            value = var.aws_session_token
          }
          env {
            name  = "AWS_DEFAULT_REGION"
            value = "us-east-1"
          }
          env {
            name  = "STORAGE_BUCKET"
            value = "video-frame-extractor-hackathon"
          }
          env {
            name  = "STORAGE_VIDEO_PATH"
            value = "video-bucket"
          }
          env {
            name  = "STORAGE_FRAMES_PATH"
            value = "frames-bucket"
          }
          env {
            name  = "SQS_QUEUE_NAME"
            value = "extract_frames_queue"
          }
          port {
            container_port = 8080
          }
        }
      }
    }
  }
}