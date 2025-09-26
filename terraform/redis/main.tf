provider "aws" {
  region = var.aws_region
}

terraform {
  backend "s3" {
    bucket = "soattc10-phase5-frames-service"
    key    = "redis/terraform.tfstate"
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

# ConfigMap para configurações do Redis
resource "kubernetes_config_map" "frames_redis_config" {
  metadata {
    name      = "frames-redis-config"
    namespace = var.namespace
  }

  data = {
    "redis.conf" = <<-EOF
      maxmemory ${var.redis_max_memory}
      maxmemory-policy allkeys-lru
      timeout 0
      tcp-keepalive 300
      databases 16
      requirepass ${var.redis_password}
      # Sem persistência para demonstração
      save ""
      appendonly no
    EOF
  }
}

# Redis Service
resource "kubernetes_service" "redis" {
  metadata {
    name      = "frames-microservice-redis"
    namespace = var.namespace
    labels = {
      app = "frames-microservice-redis"
    }
  }
  spec {
    selector = {
      app = "frames-microservice-redis"
    }
    port {
      name        = "frames-microservice-redis"
      port        = var.redis_port
      target_port = var.redis_port
      protocol    = "TCP"
    }
    type = "ClusterIP"
  }
}

# Redis Deployment
resource "kubernetes_deployment" "redis" {
  metadata {
    name      = "frames-microservice-redis"
    namespace = var.namespace
    labels = {
      app = "frames-microservice-redis"
    }
  }
  spec {
    replicas = var.redis_replicas
    selector {
      match_labels = {
        app = "frames-microservice-redis"
      }
    }
    template {
      metadata {
        labels = {
          app = "frames-microservice-redis"
        }
      }
      spec {
        container {
          name    = "frames-microservice-redis"
          image   = var.redis_image
          command = ["redis-server", "/usr/local/etc/redis/redis.conf"]

          port {
            container_port = var.redis_port
          }

          # Apenas o volume de configuração, sem persistência
          volume_mount {
            name       = "redis-config"
            mount_path = "/usr/local/etc/redis"
            read_only  = true
          }

          resources {
            limits = {
              memory = var.redis_memory_limit
              cpu    = var.redis_cpu_limit
            }
            requests = {
              memory = var.redis_memory_request
              cpu    = var.redis_cpu_request
            }
          }

          liveness_probe {
            exec {
              command = ["redis-cli", "-a", var.redis_password, "ping"]
            }
            initial_delay_seconds = 30
            period_seconds        = 10
            timeout_seconds       = 5
            failure_threshold     = 3
          }

          readiness_probe {
            exec {
              command = ["redis-cli", "-a", var.redis_password, "ping"]
            }
            initial_delay_seconds = 5
            period_seconds        = 5
            timeout_seconds       = 3
            failure_threshold     = 3
          }
        }

        # Apenas o volume de configuração
        volume {
          name = "redis-config"
          config_map {
            name = kubernetes_config_map.frames_redis_config.metadata[0].name
          }
        }
      }
    }
  }
}