import pytest
from unittest.mock import patch, MagicMock
from src.sc_ec2_auto_cost_opt_stop_and_reporter import lambda_handler, kill_all, stop_instances, send_sns_message

@pytest.fixture
def ec2_client_mock():
    with patch('boto3.client') as mock:
        yield mock

@pytest.fixture
def sts_client_mock():
    with patch('boto3.client') as mock:
        yield mock

@pytest.fixture
def sns_client_mock():
    with patch('boto3.client') as mock:
        yield mock

def test_stop_instances(ec2_client_mock):
    stopped_instances = []
    instance_id = 'i-1234567890abcdef0'
    ec2_client_mock.stop_instances.return_value = {'StoppingInstances': [{'InstanceId': instance_id}]}

    stop_instances(ec2_client_mock, instance_id, stopped_instances)

    assert instance_id in stopped_instances
    ec2_client_mock.stop_instances.assert_called_once_with(InstanceIds=[instance_id])

def test_kill_all(ec2_client_mock):
    response = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-1234567890abcdef0",
                        "State": {"Name": "running"},
                        "LaunchTime": datetime.now(timezone.utc) - timedelta(hours=5),
                        "Tags": [{"Key": "live", "Value": "no"}]
                    }
                ]
            }
        ]
    }
    ec2_client_mock.describe_instances.return_value = response

    stopped_instances = kill_all(ec2_client_mock, response)

    assert "i-1234567890abcdef0" in stopped_instances

def test_send_sns_message(sns_client_mock):
    stopped_instances = ['i-1234567890abcdef0']
    account_id = '123456789012'
    account_name = 'test-account'
    sns_client_mock.publish.return_value = {}

    send_sns_message(stopped_instances, account_id, account_name)

    sns_client_mock.publish.assert_called_once()

def test_lambda_handler(ec2_client_mock, sts_client_mock, sns_client_mock):
    sts_client_mock.get_caller_identity.return_value = {"Account": "123456789012"}
    ec2_client_mock.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-1234567890abcdef0",
                        "State": {"Name": "running"},
                        "LaunchTime": datetime.now(timezone.utc) - timedelta(hours=5),
                        "Tags": [{"Key": "live", "Value": "no"}]
                    }
                ]
            }
        ]
    }
    with patch('boto3.client') as mock_client:
        mock_client.side_effect = [ec2_client_mock, sts_client_mock, sns_client_mock]
        response = lambda_handler({}, {})

    assert response['statusCode'] == 200
    assert 'stopped_instances' in response['body']
    assert 'i-1234567890abcdef0' in response['body']['stopped_instances']