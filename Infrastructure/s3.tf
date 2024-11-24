resource "aws_s3_bucket" "s3_raw" {
  bucket = "${local.project_name}-raw-bucket"

  tags = {
    Name = "${local.project_name}-raw-bucket"
  }
}
resource "aws_s3_bucket" "s3_consumed" {
  bucket = "${local.project_name}-consumed-bucket"

  tags = {
    Name = "${local.project_name}-consumed-bucket"
  }
}

resource "aws_s3_bucket" "s3_saved_model" {
  bucket = "${local.project_name}-saved-model-bucket"

  tags = {
    Name = "${local.project_name}-saved-model-bucket"
  }
}