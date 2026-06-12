variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "email_address" {
  description = "Email address for notifications"
  type        = string
}

variable "urls_to_check" {
  description = "List of URLs to monitor"
  type        = list(string)
  default     = ["https://google.com", "https://aws.amazon.com"]
}

variable "check_interval_minutes" {
  description = "How often to check URLs (in minutes)"
  type        = number
  default     = 5
}