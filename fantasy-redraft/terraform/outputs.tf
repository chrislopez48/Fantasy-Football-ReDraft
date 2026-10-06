output "fantasy_data_bucket_name" {
  value = aws_s3_bucket.fantasy_data.bucket
}


output "fantasy_data_bucket_arn" {
  value = aws_s3_bucket.fantasy_data.arn
}

output "ecr_repository_url" {
  value = aws_ecr_repository.fantasy_pipeline.repository_url
}