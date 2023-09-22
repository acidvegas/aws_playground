provider "aws" {
  region  = var.aws_region
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "LambdaExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "this" {
  count = var.instance_count
  function_name = "FUNK-${count.index}"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.lambda_execution_role.arn
  runtime       = "python3.8"
  filename = "lambda_function.zip"
  source_code_hash = filebase64sha256("lambda_function.zip")
  timeout = 15
}