resource "aws_cloudwatch_event_rule" "check_schedule" {
  name                = "website-check-schedule"
  description         = "Trigger URL checker every ${var.check_interval_minutes} minutes"
  schedule_expression = "rate(${var.check_interval_minutes} minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.check_schedule.name
  target_id = "url-checker-lambda"
  arn       = aws_lambda_function.url_checker.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.url_checker.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.check_schedule.arn
}