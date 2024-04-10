terraform {
  backend "s3" {}
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      ENVIRONMENT = lookup({
        dev = "DEV",
        stg = "STG",
        prd = "PRD"
      }, terraform.workspace)

      OWNER = lookup({
        dev = "TCC_DEV",
        stg = "TCC_STG",
        prd = "TCC_PRD"
      }, terraform.workspace)

      PRODUCT = lookup({
        dev = "TCC",
        stg = "TCC",
        prd = "TCC"
      }, terraform.workspace)

      ManagedBy  = "terraform"
      Repository = "https://github.com/EnanHenrique/tcc-cco-2024.git"
      CreatedAt  = "10/04/2024"
    }
  }
}
