from botocore.stub import Stubber
import boto3
from src.aws import ec2 as ec2_mod




def test_list_instances_no_instances():
client = boto3.client('ec2', region_name='us-east-1')
stub = Stubber(client)
response = {'Reservations': []}
stub.add_response('describe_instances', response)
stub.activate()


# monkeypatch the internal client creator to return our stubbed client
ec2_mod._ec2_client = lambda region_name=None: client


instances = ec2_mod.list_instances(region_name='us-east-1')
assert instances == []


stub.deactivate()