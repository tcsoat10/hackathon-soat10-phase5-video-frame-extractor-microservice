# Celery Worker Outputs
output "celery_worker_deployment_name" {
  description = "Name of the Celery worker deployment"
  value       = kubernetes_deployment.frames_celery_worker.metadata[0].name
}

output "celery_worker_replicas" {
  description = "Number of Celery worker replicas"
  value       = kubernetes_deployment.frames_celery_worker.spec[0].replicas
}

output "celery_worker_namespace" {
  description = "Namespace of the Celery worker"
  value       = kubernetes_deployment.frames_celery_worker.metadata[0].namespace
}

# Celery Beat Outputs
output "celery_beat_deployment_name" {
  description = "Name of the Celery beat deployment"
  value       = kubernetes_deployment.frames_celery_beat.metadata[0].name
}

output "celery_beat_namespace" {
  description = "Namespace of the Celery beat"
  value       = kubernetes_deployment.frames_celery_beat.metadata[0].namespace
}

# Celery Configuration Outputs
output "celery_broker_url" {
  description = "Celery broker URL being used"
  value       = data.terraform_remote_state.redis.outputs.celery_broker_url
}

output "celery_result_backend" {
  description = "Celery result backend URL being used"
  value       = data.terraform_remote_state.redis.outputs.celery_result_backend
}

# Resource Information
output "celery_resources" {
  description = "Resource allocation for Celery components"
  value = {
    worker = {
      replicas = var.celery_worker_replicas
      memory_limit = var.celery_worker_memory_limit
      cpu_limit = var.celery_worker_cpu_limit
      memory_request = var.celery_worker_memory_request
      cpu_request = var.celery_worker_cpu_request
    }
    beat = {
      replicas = 1
      memory_limit = var.celery_beat_memory_limit
      cpu_limit = var.celery_beat_cpu_limit
      memory_request = var.celery_beat_memory_request
      cpu_request = var.celery_beat_cpu_request
    }
  }
}