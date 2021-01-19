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

                logger.debug(instance_id_name)
                logger.debug(launch_time)
        logger.info("Described with no invalid IDs")
        return instance_launch_times

    except ClientError as e:
        instance_launch_times = {}
        for row in instance_list:
            launch_time = describe_try(row)
            instance_launch_times[row] = launch_time

            logger.debug(instance_launch_times[row])
            logger.debug(launch_time)
        logger.error(str(e),
                     "This error is being caught and individual instances of exception causing list will go to describe_try()")
        logger.info(instance_launch_times)
        return instance_launch_times

    except Exception as e:
        logger.error(str(e))
        return None
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])
        return None


def describe_try(instance):
    logger.info(f"Attempt to describe individual instance {instance} from problem ASG")
    instance = str(instance)
    try:
        response = ec2_client.describe_instances(
            InstanceIds=[instance]
        )
        logger.info("Getting response...")
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                launch_time = instance["LaunchTime"]

                logger.debug(instance)
                logger.debug(launch_time)
                logger.info("Handled successfully")

                return launch_time
    except:
        logger.error(f"Failed to describe {instance}:", sys.exc_info()[0])
        return None


def instance_time(instance_launch_times):
    instance_uptime = {}
    for instance_id, launch_time in instance_launch_times.items():
        if launch_time is not None:
            timedelta = datetime.now(launch_time.tzinfo) - launch_time
            instance_uptime[instance_id] = timedelta.total_seconds()

            logger.debug('instance id: ', instance_id)
            logger.debug('instance Timestamp: creationDate: ', launch_time)
            logger.debug('instance Timestamp: delta: ', timedelta.total_seconds())
        else:
            instance_uptime[instance_id] = None
            logger.info(f"instance {instance_id} invalid id timestamp = None")
    logger.debug(instance_uptime)
    return instance_uptime


def handler():
    logger.info("Fetching the uptime for all EC2 instances...")
    asg_instance_uptime = {}
    for asg_name, list_of_instances in describe_asg().items():
        asg_instance_uptime[asg_name] = instance_time(describe_instances(list_of_instances))
        logger.info(asg_name)
        logger.info(asg_instance_uptime[asg_name])
    return asg_instance_uptime


handler()
