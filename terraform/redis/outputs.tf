output "redis_service_name" {
  description = "Name of the Redis service"
  value       = kubernetes_service.redis.metadata[0].name
}

output "redis_service_namespace" {
  description = "Namespace of the Redis service"
  value       = kubernetes_service.redis.metadata[0].namespace
}

output "redis_port" {
  description = "Redis service port"
  value       = kubernetes_service.redis.spec[0].port[0].port
}

# Redis Connection Information
output "redis_host" {
  description = "Redis host for internal cluster connections"
  value       = kubernetes_service.redis.metadata[0].name
}

output "redis_url" {
  description = "Complete Redis URL for applications"
  value       = "redis://${kubernetes_service.redis.metadata[0].name}:${kubernetes_service.redis.spec[0].port[0].port}"
}

output "redis_connection_string" {
  description = "Redis connection string with database 0"
  value       = "${kubernetes_service.redis.metadata[0].name}:${kubernetes_service.redis.spec[0].port[0].port}/0"
}

# Celery-specific outputs
output "celery_broker_url" {
  description = "Celery broker URL using Redis"
  value       = "${kubernetes_service.redis.metadata[0].name}:${kubernetes_service.redis.spec[0].port[0].port}/0"
}

output "celery_result_backend" {
  description = "Celery result backend URL using Redis"
  value       = "${kubernetes_service.redis.metadata[0].name}:${kubernetes_service.redis.spec[0].port[0].port}/1"
}

# Redis Deployment Information
output "redis_deployment_name" {
  description = "Name of the Redis deployment"
  value       = kubernetes_deployment.redis.metadata[0].name
}

output "redis_replicas" {
  description = "Number of Redis replicas"
  value       = kubernetes_deployment.redis.spec[0].replicas
}

# Configuration Information
output "redis_config_map_name" {
  description = "Name of the Redis ConfigMap"
  value       = kubernetes_config_map.frames_redis_config.metadata[0].name
}

# Resource Information
output "redis_resource_limits" {
  description = "Redis resource limits"
  value = {
    memory = var.redis_memory_limit
    cpu    = var.redis_cpu_limit
  }
}

output "redis_resource_requests" {
  description = "Redis resource requests"
  value = {
    memory = var.redis_memory_request
    cpu    = var.redis_cpu_request
  }
}

output "redis_password" {
  description = "Redis authentication password"
  value       = var.redis_password
  sensitive   = true
}