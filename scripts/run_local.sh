set -e
source .venv/bin/activate
python -m src.cli ec2-list --region ${1:-us-east-1}