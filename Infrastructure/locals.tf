locals {
  project_name = "${var.app_name}-${var.env_name}"

  get_variables = [
  ]
  get_secrets = [
  ]
  get_secret_arns = [for secret in local.get_secrets : secret.valueFrom]
  get_env = {
  }

  parameters_containers = {
  }

}