import argparse
from src.aws import ec2 as ec2_mod
from src import config




def cmd_ec2_list(args):
instances = ec2_mod.list_instances(region_name=args.region)
if not instances:
print("No instances found")
return
for i in instances:
uptime = ec2_mod.uptime_seconds(i['LaunchTime'])
hrs = uptime / 3600 if uptime else None
print(f"{i['InstanceId']}: state={i['State']}, type={i['InstanceType']}, uptime_hrs={hrs:.2f}")




def main():
parser = argparse.ArgumentParser(prog='aws-ops-toolkit')
sub = parser.add_subparsers(dest='cmd')


p = sub.add_parser('ec2-list', help='List EC2 instances')
p.add_argument('--region', default=config.DEFAULT_REGION)
p.set_defaults(func=cmd_ec2_list)


args = parser.parse_args()
if not hasattr(args, 'func'):
parser.print_help()
return
args.func(args)




if __name__ == '__main__':
main()