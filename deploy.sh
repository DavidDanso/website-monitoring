#!/bin/bash

set -e

echo "🚀 Deploying Website Monitoring System"

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found"
    echo "📝 Copy terraform.tfvars.example to terraform.tfvars and update it"
    exit 1
fi

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Validate configuration
echo "✅ Validating configuration..."
terraform validate

# Show plan
echo "📋 Generating deployment plan..."
terraform plan

# Ask for confirmation
read -p "Deploy? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

# Apply
echo "🔨 Deploying..."
terraform apply -auto-approve

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📧 IMPORTANT: Check your email and confirm the SNS subscription"
echo ""
echo "📊 View logs:"
echo "   aws logs tail /aws/lambda/website-url-checker --follow"
echo ""