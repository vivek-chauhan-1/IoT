import boto3
import os

sns_topic_arn = os.environ.get('sns_topic_arn')
num_devices = os.environ.get('num_devices')
service_role_arn = os.environ.get('service_role_arn')
device_name = os.environ.get('device_name')


def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    response = ssm.send_command(
        InstanceIds=[
            os.environ.get('cloud9_id'),
        ],
        DocumentName='AWS-RunRemoteScript',
        Parameters={
            'sourceType': ['S3'],
            'sourceInfo': ['{\"path\": \"https://hm-iot-infra-bucket.s3.amazonaws.com/virtual_device_creator/pub_sub.sh\"}'],
            'commandLine': ['bash pub_sub.sh {0} {1}'.format(num_devices, device_name)]
        },
        OutputS3Region='us-east-1',
        OutputS3BucketName='hm-iot-infra-bucket',
        OutputS3KeyPrefix='PubSubRunStatus',
        ServiceRoleArn=service_role_arn,
        NotificationConfig={
            'NotificationArn': sns_topic_arn,
            'NotificationEvents': ['Success', 'Failed'],
            'NotificationType': 'Invocation'
        }
    )