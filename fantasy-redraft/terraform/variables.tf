variable "aws_region" {
  description = "AWS region for fantasy football infrastructure"
  type        = string
  default     = "us-east-1"
}


variable "bucket_name" {
  description = "S3 bucket name for fantasy football pipeline data"
  type        = string
}