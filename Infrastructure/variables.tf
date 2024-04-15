variable "aws_region" {
  type        = string
  description = "Default region to deploy"
}

variable "app_name" {
  type        = string
  description = "Application name to deploy"
}

variable "env_name" {
  type        = string
  description = "Environment name to deploy"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR VPC"
}

variable "public_subnets_cidr" {
  type        = list(string)
  description = "The list of public subnets to deploy"
}

variable "availability_zones" {
  type        = list(string)
  description = "The list of availability zones to deploy"
}

variable "private_subnets_cidr" {
  type        = list(string)
  description = "The list of private subnets to deploy"
}

variable "db_username" {
  type        = string
  description = "Username to connect to rds"
}
variable "db_password" {
  type        = string
  description = "Password to connect to rds"
}
variable "lambda_path_code" {
  type        = string
  description = "Handler name to run lambda"
}
variable "lambda_path_layer" {
  type        = string
  description = "Layer path to lambda"
}
variable "runtime" {
  type        = string
  description = "Runtime to lambda"
}
variable "timeout" {
  type        = string
  description = "Timeout to lambda"
}
