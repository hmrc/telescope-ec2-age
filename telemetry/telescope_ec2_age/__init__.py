import warnings
# Ignore Boto3 Python deprecation warnings
from boto3.exceptions import PythonDeprecationWarning
warnings.filterwarnings("ignore", category=PythonDeprecationWarning)

APP_NAME = 'telescope-ec2-age'
APP_VERSION = "0.1.0"
METRICS_PREFIX = "telemetry.telescope.asg"
