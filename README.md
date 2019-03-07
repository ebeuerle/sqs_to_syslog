# RedLock SQS poller to Syslog 

Version: *1.0*
Author: *Eddie Beuerlein*

### Summary
This script will poll an AWS SQS queue for RedLock alerts and then format them and send them to a syslog listener (locally or remote). 

### Requirements and Dependencies

1. Python 2.7.10 or newer

2. OpenSSL 1.0.2 or newer

(if using on Mac OS, additional items may be nessessary.)

3. Pip

```sudo easy_install pip```

4. Requests (Python library)

```sudo pip install requests```

5. YAML (Python library)

```sudo pip install pyyaml```

### Configuration

1. Navigate to *sqs_to_syslog/config/configs.yml*

2. Fill out your AWS key, AWS secret, aws sqs queue and aws region as well as syslog server(defaults to localhost).

3. Schedule to run the main script via cron or something similar: python poll_n_write.py

### Run

```
python poll_n_write.py

```
