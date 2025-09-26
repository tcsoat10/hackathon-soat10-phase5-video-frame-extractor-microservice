locals {
  use_mock = (terraform.workspace == "default" || terraform.workspace == "test")
}

data "terraform_remote_state" "aws" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_eks_outputs.tfstate"
    } : {
    bucket = "soattc10-phase5-aws-infra"
    key    = "env:/${terraform.workspace}/aws-infra/terraform.tfstate"
    region = "us-east-1"
  }
}