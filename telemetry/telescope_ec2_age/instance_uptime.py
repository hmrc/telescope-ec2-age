import boto3
from datetime import datetime
import sys
from botocore.exceptions import ClientError
from telemetry.telescope_ec2_age.logger import get_app_logger

autoscaling_client = boto3.client('autoscaling', region_name='eu-west-2')
ec2_client = boto3.client('ec2', region_name='eu-west-2')
logger = get_app_logger()


def describe_asg():
    response = autoscaling_client.describe_auto_scaling_groups()
    asgs = {}
    for asg in response["AutoScalingGroups"]:
        instance_list = []
        asg_name = asg["AutoScalingGroupName"]
        for instance in asg["Instances"]:
            if instance != "":
                id_of_instance = instance["InstanceId"]
                instance_list.append(id_of_instance)
            asgs[asg_name] = instance_list
    return asgs


def describe_instances(instance_list):
    try:
        response = ec2_client.describe_instances(
            InstanceIds=instance_list
        )
        instance_launch_times = {}
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                launch_time = instance["LaunchTime"]
                instance_id_name = instance["InstanceId"]
                instance_launch_times[instance_id_name] = launch_time
        return instance_launch_times
    except ClientError as e:
        logger.error(str(e))
        return None
    except Exception as e:
        logger.error(str(e))
        return None
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])
        return None


def instance_time(instance_launch_times):
    if instance_launch_times is None:
        return instance_launch_times
    instance_uptime = {}
    for instance_id, launch_time in instance_launch_times.items():
        timedelta = datetime.now(launch_time.tzinfo) - launch_time
        instance_uptime[instance_id] = timedelta.total_seconds()

        logger.debug('instance id: ' + str(instance_id))
        logger.debug('intance Timestamp: creationDate: ' + str(launch_time))
        logger.debug('instance Timestamp: delta: ' + str(timedelta.total_seconds()))
    return instance_uptime


def handler():
    logger.info("Fetching the uptime for all EC2 instances...")
    asg_instance_uptime = {}
    for asg_name, list_of_instances in describe_asg().items():
        logger.debug('asg name:' + str(asg_name))
        asg_instance_uptime[asg_name] = instance_time(describe_instances(list_of_instances))
    return asg_instance_uptime
