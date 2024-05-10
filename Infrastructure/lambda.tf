data "aws_caller_identity" "current" {}

data "archive_file" "code" {
  type        = "zip"
  source_dir  = var.lambda_path_code
  output_path = "./outputs/${local.project_name}-src.zip"
  excludes    = [".idea", ".circleci", "*.pyc", "tests", "packages", "layer", "python", ".git", "venv", "requirements.txt"]
}
data "archive_file" "layer" {
  type        = "zip"
  source_dir  = "${var.lambda_path_layer}/layer"
  output_path = "./outputs/${local.project_name}-layer.zip"
}

resource "aws_lambda_layer_version" "this" {
  filename                 = "./outputs/${local.project_name}-layer.zip"
  layer_name               = "${local.project_name}-layer"
  description              = "${local.project_name}-layer"
  source_code_hash         = data.archive_file.layer.output_base64sha256
  compatible_runtimes      = [var.runtime]
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_function" "image_processing" {
  function_name    = "${local.project_name}-image-processing"
  role             = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/LabRole"
  handler          = "app.lambda_handler"
  runtime          = var.runtime
  timeout          = var.timeout
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256
  layers           = [aws_lambda_layer_version.this.arn]
  environment {
    variables = local.get_env
  }
  dynamic "vpc_config" {
    for_each = length(var.public_subnets_cidr) > 0 ? [1] : []
    content {
      subnet_ids         = [aws_subnet.public_subnet[0].id]
      security_group_ids = [aws_security_group.lambda_security_group.id]
    }
  }
}

resource "aws_lambda_permission" "image_processing_permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.image_processing.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.s3_raw.id}"
}
