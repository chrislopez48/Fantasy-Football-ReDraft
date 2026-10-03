terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }                           #aws,azzure,docker, github etc have providers

  }
}

provider "aws" {
  region = var.aws_region
}