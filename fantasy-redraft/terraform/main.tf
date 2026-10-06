resource "aws_s3_bucket" "fantasy_data" {
  bucket = var.bucket_name

  tags = {
    Project     = "Fantasy Football Data Platform"
    Environment = "dev"
  }
}

resource "aws_ecr_repository" "fantasy_pipeline" {
  name = "fantasy-redraft"
}