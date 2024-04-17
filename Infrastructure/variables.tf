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
