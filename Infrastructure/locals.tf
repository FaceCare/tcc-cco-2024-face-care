locals {
  project_name = "${var.app_name}-${var.env_name}"

  get_variables = [
    # { "name" = "DB_DATABASE", "value" = module.rds_crm_core.cluster_database_name },
    # { "name" = "DB_PORT", "value" = tostring(module.rds_crm_core.cluster_port) },
    # { "name" = "DB_HOSTNAME", "value" = module.rds_crm_core.cluster_hostname },
    # { "name" = "DB_USERNAME", "value" = module.rds_crm_core.cluster_username },
  ]
  get_secrets = [
    # { "name" = "DB_PASSWORD", "valueFrom" = module.rds_crm_core.cluster_password_version_arn },
  ]
  get_secret_arns = [for secret in local.get_secrets : secret.valueFrom]
  get_env = {
    # "DB_DATABASE" = module.rds_crm_core.cluster_database_name
    # "DB_PORT"     = tostring(module.rds_crm_core.cluster_port)
    # "DB_HOSTNAME" = module.rds_crm_core.cluster_hostname
    # "DB_USERNAME" = module.rds_crm_core.cluster_username
    # "DB_PASSWORD" = module.rds_crm_core.cluster_password_version_arn
  }

  parameters_containers = {
    # app_name        = var.app_name,
    # env_name        = var.env_name,
    # container_cpu   = var.container_cpu,
    # container_mem   = var.container_mem,
    # container_port  = var.container_port,
    # ecr_repo        = aws_ecr_repository.aws_ecr.repository_url,
    # ecr_tag         = var.ecr_tag
    # log_group_id    = aws_cloudwatch_log_group.ecs.id,
    # aws_region      = var.aws_region,
    # app_environment = var.env_name
    # environment     = jsonencode(local.get_variables)
    # secrets         = jsonencode(local.get_secrets)
  }
  # revision_task_definition = max(aws_ecs_task_definition.crm_core_infra.revision, data.aws_ecs_task_definition.main.revision)

}
