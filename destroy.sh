#!/bin/bash

set -e

echo "🗑️  Destroying Website Monitoring System"

# Ask for confirmation
read -p "Are you sure you want to destroy all resources? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "❌ Destruction cancelled"
    exit 0
fi

# Destroy
echo "💥 Destroying resources..."
terraform destroy -auto-approve

echo ""
echo "✅ All resources destroyed"
echo ""