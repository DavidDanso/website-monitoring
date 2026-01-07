import json
import os
import urllib3
import boto3
from datetime import datetime

http = urllib3.PoolManager()
sns_client = boto3.client('sns')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
URLS_TO_CHECK = json.loads(os.environ['URLS_TO_CHECK'])

def lambda_handler(event, context):
    print(f"Starting website checks at {datetime.utcnow().isoformat()}")
    
    failed_urls = []
    
    for url in URLS_TO_CHECK:
        try:
            print(f"Checking {url}...")
            response = http.request('GET', url, timeout=10.0)
            
            if response.status == 200:
                print(f"✓ {url} is UP (status: {response.status})")
            else:
                error_msg = f"✗ {url} returned status {response.status}"
                print(error_msg)
                failed_urls.append({
                    'url': url,
                    'status': response.status,
                    'reason': f"Status code: {response.status}"
                })
                
        except Exception as e:
            error_msg = f"✗ {url} is DOWN - Error: {str(e)}"
            print(error_msg)
            failed_urls.append({
                'url': url,
                'status': 'error',
                'reason': str(e)
            })
    
    # Send notification if any URLs failed
    if failed_urls:
        send_alert(failed_urls)
        print(f"Alert sent for {len(failed_urls)} failed URL(s)")
    else:
        print("All URLs are healthy")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'checked': len(URLS_TO_CHECK),
            'failed': len(failed_urls),
            'failures': failed_urls
        })
    }

def send_alert(failed_urls):
    subject = f"⚠️ Website Alert: {len(failed_urls)} Site(s) Down"
    
    message_lines = [
        "Website Monitoring Alert",
        f"Time: {datetime.utcnow().isoformat()}",
        "",
        "The following sites are down:",
        ""
    ]
    
    for failure in failed_urls:
        message_lines.append(f"URL: {failure['url']}")
        message_lines.append(f"Status: {failure['status']}")
        message_lines.append(f"Reason: {failure['reason']}")
        message_lines.append("")
    
    message = "\n".join(message_lines)
    
    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
    except Exception as e:
        print(f"Failed to send SNS notification: {str(e)}")