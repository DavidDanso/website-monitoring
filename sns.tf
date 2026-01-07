resource "aws_sns_topic" "alerts" {
  name = "website-monitoring-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.email_address
}