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

    asg_dict = {}
    for asg in response["AutoScalingGroups"]:
        instance_list = []
        asg_name = asg["AutoScalingGroupName"]
        for instance in asg["Instances"]:
            if instance != "":
                id_of_instance = instance["InstanceId"]
                instance_list.append(id_of_instance)
            asg_dict[asg_name] = instance_list
    return asg_dict


def describe_instances(instance_list):
    try:
        response = ec2_client.describe_instances(
            InstanceIds=instance_list
        )
        instance_dictionary = {}
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                launch_time = instance["LaunchTime"]
                instance_id_name = instance["InstanceId"]
                instance_dictionary[instance_id_name] = launch_time
        return instance_dictionary
    except ClientError as e:
        logger.error(str(e))
        return None
    except Exception as e:
        logger.error(str(e))
        return None
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])
        return None


def instance_time(dictionary):
    if dictionary is None:
        return dictionary
    time_dict = {}
    for key, launch_time in dictionary.items():
        timedelta = datetime.now(launch_time.tzinfo) - launch_time
        time_dict[key] = timedelta.total_seconds()

        logger.debug('instance id: ' + str(key))
        logger.debug('intance Timestamp: creationDate: ' + str(launch_time))
        logger.debug('instance Timestamp: delta: ' + str(timedelta.total_seconds()))
    return time_dict


def handler():
    logger.info("Fetching the uptime for all EC2 instances...")
    new_dict = {}
    for asg_name, list_of_instances in describe_asg().items():
        logger.debug('asg name:' + str(asg_name))
        new_dict[asg_name] = instance_time(describe_instances(list_of_instances))
    return new_dict
