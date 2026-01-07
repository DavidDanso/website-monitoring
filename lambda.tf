resource "aws_iam_role" "lambda_role" {
  name = "url-checker-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "url-checker-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.alerts.arn
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.url_checker.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_function" "url_checker" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "website-url-checker"
  role            = aws_iam_role.lambda_role.arn
  handler         = "index.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.alerts.arn
      URLS_TO_CHECK = jsonencode(var.urls_to_check)
    }
  }
}