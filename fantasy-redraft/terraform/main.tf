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

resource "aws_ecs_cluster" "fantasy_cluster" {
  name = "fantasy-redraft-cluster"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "fantasy-redraft-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task_role" {
  name = "fantasy-redraft-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "ecs_task_s3_policy" {
  name = "fantasy-redraft-s3-policy"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "s3:PutObject"
        ]

        Resource = "${aws_s3_bucket.fantasy_data.arn}/*"
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "fantasy_pipeline" {
  name              = "/ecs/fantasy-redraft"
  retention_in_days = 7
}

resource "aws_ecs_task_definition" "fantasy_pipeline" {
  family                   = "fantasy-redraft-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  cpu    = "256"
  memory = "512"

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "fantasy-redraft"
      image     = "131715058630.dkr.ecr.us-east-1.amazonaws.com/fantasy-redraft:latest"
      essential = true

      logConfiguration = {
        logDriver = "awslogs"

        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.fantasy_pipeline.name
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "fantasy_pipeline" {
  name        = "fantasy-redraft-sg"
  description = "Security group for fantasy redraft Fargate task"
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}