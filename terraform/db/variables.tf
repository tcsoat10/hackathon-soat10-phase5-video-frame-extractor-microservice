variable "cluster_name" {
  default = "hacka-soat10tc-cluster-eks"
}

variable "mongo_user" {
  default = "microservice_admin"
}

variable "mongo_password" {}

variable "mongo_root_password" {}

variable "db_name" {
  default = "frames_microservice"
}