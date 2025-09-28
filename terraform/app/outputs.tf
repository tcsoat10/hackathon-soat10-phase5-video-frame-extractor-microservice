output "frames_app_lb_endpoint" {
  description = "Endpoint do Load Balancer do frames-app"
  value       = "${kubernetes_service.frames_app_lb.status[0].load_balancer[0].ingress[0].hostname}"
}