provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc10-phase5-frames-service"
    key    = "celery/terraform.tfstate"
    region = "us-east-1"
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

# Celery Worker Deployment
resource "kubernetes_deployment" "frames_celery_worker" {
  metadata {
    name      = "frames-celery-worker"
    namespace = var.namespace
    labels = {
      app       = "frames-celery-worker"
      component = "celery"
    }
  }
  spec {
    replicas = var.celery_worker_replicas
    selector {
      match_labels = {
        app = "frames-celery-worker"
      }
    }
    template {
      metadata {
        labels = {
          app       = "frames-celery-worker"
          component = "celery"
        }
      }
      spec {
        container {
          name  = "frames-celery-worker"
          image = var.application_image
          command = ["celery", "-A", "src.config.celery_app", "worker", "--loglevel=info", "--concurrency=${var.celery_worker_concurrency}"]          
          
          # Variáveis de ambiente do Celery
          env {
            name  = "CELERY_BROKER_URL"
            value = "redis://:${data.terraform_remote_state.redis.outputs.redis_password}@${data.terraform_remote_state.redis.outputs.redis_host}:${data.terraform_remote_state.redis.outputs.redis_port}/0"
          }
          
          # Variáveis de ambiente do MongoDB
          env {
            name  = "MONGO_HOST"
            value = var.mongo_host
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
            name  = "AWS_ACCESS_KEY_ID"
            value = var.aws_access_key_id
          }
          env {
            name  = "AWS_SECRET_ACCESS_KEY"
            value = var.aws_secret_access_key
          }
          env {
            name  = "AWS_DEFAULT_REGION"
            value = "us-east-1"
          }
          env {
            name  = "SQS_QUEUE_NAME"
            value = var.sqs_queue_name
          }
          env {
            name  = "ENVIRONMENT"
            value = var.environment
          }
          env {
            name  = "REDIS_HOST"
            value = data.terraform_remote_state.redis.outputs.redis_host
          }
          env {
            name  = "REDIS_PORT"
            value = data.terraform_remote_state.redis.outputs.redis_port
          }

          
          resources {
            limits = {
              memory = var.celery_worker_memory_limit
              cpu    = var.celery_worker_cpu_limit
            }
            requests = {
              memory = var.celery_worker_memory_request
              cpu    = var.celery_worker_cpu_request
            }
          }
          
          # Health checks para worker
          liveness_probe {
            exec {
              command = ["celery", "-A", "src.config.celery_app", "inspect", "ping"]
            }
            initial_delay_seconds = 60
            period_seconds        = 30
            timeout_seconds       = 10
            failure_threshold     = 3
          }
        }
      }
    }
  }
}

# Celery Beat Deployment (Scheduler)
resource "kubernetes_deployment" "frames_celery_beat" {
  metadata {
    name      = "frames-celery-beat"
    namespace = var.namespace
    labels = {
      app       = "frames-celery-beat"
      component = "celery"
    }
  }
  spec {
    replicas = 1 # Always 1 for beat scheduler
    selector {
      match_labels = {
        app = "frames-celery-beat"
      }
    }
    template {
      metadata {
        labels = {
          app       = "frames-celery-beat"
          component = "celery"
        }
      }
      spec {
        container {
          name  = "frames-celery-beat"
          image = var.application_image
          command = ["celery", "-A", "src.config.celery_app", "beat", "--loglevel=info"]
          
          # Variáveis de ambiente do Celery
          env {
            name  = "CELERY_BROKER_URL"
            value = "redis://:${var.redis_password}@${data.terraform_remote_state.redis.outputs.celery_broker_url}"
          }          
          
          # Variáveis de ambiente do MongoDB
          env {
            name  = "MONGO_HOST"
            value = var.mongo_host
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
            name  = "MONGO_PORT"
            value = var.mongo_port
          }
          env {
            name  = "MONGO_URI"
            value = data.terraform_remote_state.mongo.outputs.mongo_uri
          }          
          
          resources {
            limits = {
              memory = var.celery_beat_memory_limit
              cpu    = var.celery_beat_cpu_limit
            }
            requests = {
              memory = var.celery_beat_memory_request
              cpu    = var.celery_beat_cpu_request
            }
          }
        }
      }
    }
  }
}
