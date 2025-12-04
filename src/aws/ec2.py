from datetime import datetime, timezone
import boto3




def _ec2_client(region_name=None):
return boto3.client('ec2', region_name=region_name)




def list_instances(region_name=None, filters=None):
"""
Return a list of instances with basic metadata.


Each item is a dict:
- InstanceId
- State
- InstanceType
- LaunchTime (datetime)
- Tags (dict)
"""
client = _ec2_client(region_name)
paginator = client.get_paginator('describe_instances')
page_iterator = paginator.paginate(Filters=filters or [])


instances = []
for page in page_iterator:
for reservation in page.get('Reservations', []):
for i in reservation.get('Instances', []):
instances.append({
'InstanceId': i.get('InstanceId'),
'State': i.get('State', {}).get('Name'),
'InstanceType': i.get('InstanceType'),
'LaunchTime': i.get('LaunchTime'),
'Tags': {t['Key']: t['Value'] for t in i.get('Tags', [])} if i.get('Tags') else {},
})
return instances




def uptime_seconds(launch_time):
"""Compute uptime in seconds from an AWS LaunchTime (datetime)."""
if launch_time is None:
return None
return (datetime.now(timezone.utc) - launch_time).total_seconds()




if __name__ == '__main__':
import argparse
parser = argparse.ArgumentParser(description='EC2 inventory helper')
parser.add_argument('--region', '-r', default=None)
args = parser.parse_args()


inst = list_instances(region_name=args.region)
for i in inst:
uptime = uptime_seconds(i['LaunchTime'])
hrs = uptime / 3600 if uptime is not None else 'N/A'
print(f"{i['InstanceId']}\t{ i['State']}\t{ i['InstanceType']}\t{hrs:.2f} hrs")