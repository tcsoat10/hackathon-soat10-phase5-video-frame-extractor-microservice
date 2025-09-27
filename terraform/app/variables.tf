variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "hacka-soat10tc-cluster-eks"
}

variable "vpc_cidr_block" {
  default = ["172.31.0.0/16"]
}

variable "accessConfig" {
  default = "API_AND_CONFIG_MAP"
}

variable "node_name" {
  default = "my-nodes-group"
}

variable "policy_arn" {
  default = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
}

variable "instance_type" {
  default = "t3.small"
}

variable "mongo_password" {
  description = "Database user password"
  type        = string
}

variable "mongo_db" {
  default = "zipper_service"
}

variable "mongo_user" {
  description = "Database username"
  type        = string
}

variable "mongo_host" {
  type        = string
  default = ""
}

variable "mongo_port" {
  type        = string
  default = "27017"
}


variable "frames_api_key" {}

variable "aws_access_key_id" {
  description = "AWS Access Key"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Key"
  type        = string
}

variable "aws_session_token" {
  description = "AWS Session Token"
  type        = string
}

variable "aws_account_id" {}

variable "application_image" {
  description = "Docker image for the application"
  type        = string
  default     = ""
}

locals {
  application_image = "${var.aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/soattc-frames-app:latest"
}