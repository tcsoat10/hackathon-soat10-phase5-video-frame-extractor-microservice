# AWS Configuration
variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "hacka-soat10tc-cluster-eks"
}

# Kubernetes Configuration
variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "default"
}

variable "redis_password" {
  description = "Password for Redis"
  type        = string  
  sensitive   = true
}

# Application Configuration
variable "application_image" {
  description = "Docker image for the application"
  type        = string
  default     = ""
}

locals {
  application_image = "${var.aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/soattc-frames-app:latest"
}

# MongoDB Configuration
variable "mongo_port" {
  description = "MongoDB port"
  type        = string
  default     = "27017"
}

variable "mongo_host" {
  description = "MongoDB host"
  type        = string
  default     = "video-frame-extractor-microservice-mongodb"
}

# Celery Worker Configuration
variable "celery_worker_replicas" {
  description = "Number of Celery worker replicas"
  type        = number
  default     = 2
}

variable "celery_worker_concurrency" {
  description = "Number of concurrent worker processes"
  type        = number
  default     = 2
}

variable "celery_worker_memory_limit" {
  description = "Celery worker memory limit"
  type        = string
  default     = "1Gi"
}

variable "celery_worker_cpu_limit" {
  description = "Celery worker CPU limit"
  type        = string
  default     = "1000m"
}

variable "celery_worker_memory_request" {
  description = "Celery worker memory request"
  type        = string
  default     = "512Mi"
}

variable "celery_worker_cpu_request" {
  description = "Celery worker CPU request"
  type        = string
  default     = "500m"
}

# Celery Beat Configuration
variable "celery_beat_memory_limit" {
  description = "Celery beat memory limit"
  type        = string
  default     = "256Mi"
}

variable "celery_beat_cpu_limit" {
  description = "Celery beat CPU limit"
  type        = string
  default     = "250m"
}

variable "celery_beat_memory_request" {
  description = "Celery beat memory request"
  type        = string
  default     = "128Mi"
}

variable "celery_beat_cpu_request" {
  description = "Celery beat CPU request"
  type        = string
  default     = "100m"
}

variable "environment"{
  default     = "production"
}

variable "sqs_queue_name"{
  default     = "extract_frames_queue"
}

variable "aws_secret_access_key" {}
variable "aws_access_key_id" {}
variable "aws_session_token" {}
variable "aws_account_id" {}
variable "zipper_api_key" {}