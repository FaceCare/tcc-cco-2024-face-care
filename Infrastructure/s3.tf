resource "aws_s3_bucket" "s3_raw" {
  bucket = "${local.project_name}-raw-bucket"

  tags = {
    Name = "${local.project_name}-raw-bucket"
  }
}

resource "aws_s3_bucket" "s3_staged" {
  bucket = "${local.project_name}-staged-bucket"

  tags = {
    Name = "${local.project_name}-staged-bucket"
  }
}

resource "aws_s3_bucket" "s3_consumed" {
  bucket = "${local.project_name}-consumed-bucket"

  tags = {
    Name = "${local.project_name}-consumed-bucket"
  }
}

# resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
#   bucket = aws_s3_bucket.s3_raw.id
#   lambda_function {
#     lambda_function_arn = aws_lambda_function.image_processing.arn
#     events              = ["s3:ObjectCreated:*"]
#   }
# }


resource "aws_s3_bucket" "s3_saved_model" {
  bucket = "${local.project_name}-saved-model-bucket"

  tags = {
    Name = "${local.project_name}-saved-model-bucket"
  }
}