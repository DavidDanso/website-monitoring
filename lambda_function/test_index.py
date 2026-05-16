import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

# We must set these environment variables before importing index.py 
# because index.py loads them at module initialization time.
os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:123456789012:MyTopic'
os.environ['URLS_TO_CHECK'] = json.dumps(['https://example.com'])
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# Add the directory containing this file to the python path so 'import index' works
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import index

@patch('index.http.request')
@patch('index.send_alert')
def test_200_response_healthy(mock_send_alert, mock_request):
    """Test that a 200 response is treated as healthy."""
    # Setup mock response for the HTTP GET request
    mock_response = MagicMock()
    mock_response.status = 200
    mock_request.return_value = mock_response

    # Execute the lambda handler
    result = index.lambda_handler({}, {})

    # Assert that no failures were recorded and no alert was sent
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['failed'] == 0
    mock_send_alert.assert_not_called()

@patch('index.http.request')
@patch('index.send_alert')
def test_non_200_response_failure(mock_send_alert, mock_request):
    """Test that a non-200 response (e.g. 500) is treated as a failure."""
    # Setup mock response to simulate a server error
    mock_response = MagicMock()
    mock_response.status = 500
    mock_request.return_value = mock_response

    # Execute the lambda handler
    result = index.lambda_handler({}, {})

    # Assert that the failure was recorded and an alert was triggered
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['failed'] == 1
    assert body['failures'][0]['url'] == 'https://example.com'
    assert body['failures'][0]['status'] == 500
    mock_send_alert.assert_called_once()
