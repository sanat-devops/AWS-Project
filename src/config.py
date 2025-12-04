from pathlib import Path
from dotenv import load_dotenv
import os


env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
load_dotenv(env_path)


DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
DRY_RUN = os.environ.get('DRY_RUN', 'true').lower() in ('1', 'true', 'yes')