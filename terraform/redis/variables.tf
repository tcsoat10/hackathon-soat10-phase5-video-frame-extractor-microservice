variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "hacka-soat10tc-cluster-eks"
}

# Kubernetes Configuration
variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "default"
}

variable "storage_class" {
  description = "Storage class for PVC"
  type        = string
  default     = "gp2"
}

# Redis Configuration
variable "redis_image" {
  description = "Redis Docker image"
  type        = string
  default     = "redis:7-alpine"
}

variable "redis_port" {
  description = "Redis port"
  type        = number
  default     = 6379
}

variable "redis_replicas" {
  description = "Number of Redis replicas"
  type        = number
  default     = 1
}

variable "redis_max_memory" {
  description = "Redis max memory configuration"
  type        = string
  default     = "256mb"
}

variable "redis_storage_size" {
  description = "Redis storage size"
  type        = string
  default     = "10Gi"
}

# Resource Limits
variable "redis_memory_limit" {
  description = "Redis memory limit"
  type        = string
  default     = "512Mi"
}

variable "redis_cpu_limit" {
  description = "Redis CPU limit"
  type        = string
  default     = "500m"
}

variable "redis_memory_request" {
  description = "Redis memory request"
  type        = string
  default     = "256Mi"
}

variable "redis_cpu_request" {
  description = "Redis CPU request"
  type        = string
  default     = "250m"
}

variable "redis_password"{
  type        = string
}