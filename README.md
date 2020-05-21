# Prisma Cloud SQS poller to Syslog 

Version: *1.1*
Author: *Eddie Beuerlein*

### Summary
This script will poll an AWS SQS queue for Prisma Cloud alerts and then format them and send them to a syslog listener (locally or remote). This can be used for QRadar as well by using the LEEF named script.

### Requirements and Dependencies

1. Python 3.x or newer

2. Requests (Python library)

```sudo pip install requests```

3. YAML (Python library)

```sudo pip install pyyaml```

### Configuration

1. Set environment variables for AWS Key/Secret per boto3 instructions
```
Boto3 will check these environment variables for credentials:

AWS_ACCESS_KEY_ID
The access key for your AWS account.
AWS_SECRET_ACCESS_KEY
The secret key for your AWS account.
AWS_SESSION_TOKEN
The session key for your AWS account. This is only needed when you are using temporary credentials. The AWS_SECURITY_TOKEN environment variable can also be used, but is only supported for backwards compatibility purposes. AWS_SESSION_TOKEN is supported by multiple AWS SDKs besides python.
```
2. Navigate to *sqs_to_syslog/config/configs.yml*

3. Setup the sqs queue and aws region as well as syslog server(defaults to localhost) in the config/configs.yml

4. Schedule to run the main script via cron or something similar: python poll_n_write.py

### Run

```
python poll_n_write.py

or

python poll_n_write_leef.py (for QRadar)

```
