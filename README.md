# 🌐 AWS Website Uptime Monitor

A serverless, automated website monitoring system built with Terraform and AWS. It periodicially checks the health of your websites and sends email alerts via Amazon SNS if any site is down or returns a non-200 status code.

## ✨ Features

- **Automated Monitoring**: Leverages Amazon EventBridge to trigger checks at configurable intervals (default: every 5 minutes).
- **Serverless Execution**: Uses AWS Lambda for cost-effective, scalable website health checks.
- **Instant Alerts**: Integrates with Amazon SNS to send email notifications immediately upon detection of a failure.
- **Multi-URL Support**: Easily monitor multiple websites simultaneously.
- **Easy Deployment**: Fully automated deployment and teardown using Terraform and helper shell scripts.

## 🛠️ Tech Stack

- **Cloud Provider**: AWS (Lambda, SNS, EventBridge, CloudWatch)
- **Infrastructure as Code**: Terraform
- **Backend**: Python 3.10+
- **Automation**: Bash Scripts

## 🚀 Getting Started

### Prerequisites

1.  **AWS Account**: An active AWS account.
2.  **AWS CLI**: Configured with appropriate permissions.
3.  **Terraform**: Installed on your local machine.

### Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/DavidDanso/website-monitoring.git
    cd website-monitoring
    ```

2.  **Configure Variables**:
    Copy the example configuration file and update it with your settings:
    ```bash
    cp terraform.tfvars.example terraform.tfvars
    ```
    Edit `terraform.tfvars`:
    - `email_address`: The email where you want to receive alerts.
    - `urls_to_check`: A list of website URLs to monitor.
    - `check_interval_minutes`: Frequency of checks (e.g., `5`).

3.  **Deploy**:
    Run the deployment script:
    ```bash
    ./deploy.sh
    ```
    *Follow the prompts and type `yes` when asked to confirm the deployment.*

4.  **Confirm Email Subscription**:
    Check your inbox (and spam folder) for an AWS Notification - Subscription Confirmation email. **You must click the "Confirm Subscription" link to receive alerts.**

## 📊 Monitoring & Logs

You can monitor the checks in real-time or view historical logs using the AWS CLI or the AWS Management Console.

**View Live Logs via CLI:**
```bash
aws logs tail /aws/lambda/website-url-checker --follow
```

## 🧹 Cleanup

To remove all created resources and avoid unnecessary AWS charges:
```bash
./destroy.sh
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
