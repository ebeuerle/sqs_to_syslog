import os
import yaml


class ConfigHelper(object):
    def __init__(self):
        config = self.read_yml('configs')
        self.rl_aws_region = config["prisma_cloud"]["aws_region"]
        self.rl_aws_queue = config["prisma_cloud"]["aws_sqs_queue"]
        self.rl_syslog_host = config["prisma_cloud"]["syslog_host"]


    @classmethod
    def read_yml(self, f):
        yml_path = os.path.join(os.path.dirname(__file__), "../config/%s.yml" % f)
        with open(yml_path,'r') as stream:
            return yaml.safe_load(stream)