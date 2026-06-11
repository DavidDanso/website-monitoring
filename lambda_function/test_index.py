import unittest
import json
from unittest.mock import patch, MagicMock


# Mock environment variables before importing index
# This prevents os.environ KeyError at import time
ENV_VARS = {
    'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789:test-topic',
    'URLS_TO_CHECK': json.dumps(['https://example.com', 'https://google.com'])
}


class TestLambdaHandler(unittest.TestCase):

    # Test that a 200 response is treated as healthy — no failures recorded
    @patch('index.http')
    @patch.dict('os.environ', ENV_VARS)
    def test_200_response_is_healthy(self, mock_http):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_http.request.return_value = mock_response

        import index
        result = index.lambda_handler({}, {})
        body = json.loads(result['body'])

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(body['failed'], 0)
        self.assertEqual(len(body['failures']), 0)

    # Test that a non-200 response is treated as a failure
    @patch('index.http')
    @patch.dict('os.environ', ENV_VARS)
    def test_non_200_response_is_failure(self, mock_http):
        mock_response = MagicMock()
        mock_response.status = 500
        mock_http.request.return_value = mock_response

        import index
        result = index.lambda_handler({}, {})
        body = json.loads(result['body'])

        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(body['failed'], 2)
        self.assertEqual(body['failures'][0]['status'], 500)

    # Test that a connection exception is recorded as a failure
    @patch('index.http')
    @patch.dict('os.environ', ENV_VARS)
    def test_connection_error_is_failure(self, mock_http):
        mock_http.request.side_effect = Exception("Connection timed out")

        import index
        result = index.lambda_handler({}, {})
        body = json.loads(result['body'])

        self.assertEqual(body['failed'], 2)
        self.assertEqual(body['failures'][0]['status'], 'error')
        self.assertIn('Connection timed out', body['failures'][0]['reason'])

    # Test that send_alert is called when failures exist
    @patch('index.boto3.client')
    @patch('index.http')
    @patch.dict('os.environ', ENV_VARS)
    def test_alert_sent_on_failure(self, mock_http, mock_boto):
        mock_response = MagicMock()
        mock_response.status = 404
        mock_http.request.return_value = mock_response

        mock_sns = MagicMock()
        mock_boto.return_value = mock_sns

        import index
        index.lambda_handler({}, {})

        mock_sns.publish.assert_called_once()

    # Test that no alert is sent when all URLs are healthy
    @patch('index.boto3.client')
    @patch('index.http')
    @patch.dict('os.environ', ENV_VARS)
    def test_no_alert_sent_when_healthy(self, mock_http, mock_boto):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_http.request.return_value = mock_response

        mock_sns = MagicMock()
        mock_boto.return_value = mock_sns

        import index
        index.lambda_handler({}, {})

        mock_sns.publish.assert_not_called()


if __name__ == '__main__':
    unittest.main()