locals {
  use_mock = (terraform.workspace == "default" || terraform.workspace == "test")
}

data "terraform_remote_state" "mongo" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_mongo_outputs.tfstate"
    } : {
    bucket = "soattc10-phase5-frames-service"
    key    = "env:/${terraform.workspace}/database/terraform.tfstate"
    region = "us-east-1"
  }
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

data "terraform_remote_state" "zipper" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_zipper_outputs.tfstate"
  } : {
    bucket = "soattc10-phase5-zipper-service"
    key    = "env:/${terraform.workspace}/application/terraform.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "redis" {
  backend = local.use_mock ? "local" : "s3"
  config = local.use_mock ? {
    path = "${path.module}/../mock/mock_redis_outputs.tfstate"
  } : {
    bucket = "soattc10-phase5-frames-service"
    key    = "env:/${terraform.workspace}/redis/terraform.tfstate"
    region = "us-east-1"
  }
}