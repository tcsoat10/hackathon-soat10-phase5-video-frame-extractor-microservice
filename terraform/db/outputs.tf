output "mongo_port" {
  value = 27017
}

output "mongo_uri" {
  value = "mongodb://${var.mongo_user}:${var.mongo_password}@${helm_release.video-frame-extractor-microservice-mongodb.name}:27017/${var.db_name}?authSource=${var.db_name}"
}

output "mongo_db" {
  value = var.db_name
}

output "mongo_user" {
  value = var.mongo_user
}

output "mongo_password" {
  value = var.mongo_password
  sensitive = true
}

output "mongo_host" {
  description = "MongoDB host name (real service name)"
  value       = helm_release.video-frame-extractor-microservice-mongodb.name
}

output "mongo_auth_source" {
  description = "MongoDB authentication source"
  value       = var.db_name
}

output "mongo_container_name" {
  description = "MongoDB service name"
  value       = helm_release.video-frame-extractor-microservice-mongodb.name
}