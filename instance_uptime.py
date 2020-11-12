import boto3
from datetime import datetime, timedelta, timezone, tzinfo

autoscaling_client = boto3.client('autoscaling', region_name='eu-west-2')
ec2_client = boto3.client('ec2', region_name='eu-west-2')


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


def instance_time(dictionary):
    time_dict = {}
    for key, launch_time in dictionary.items():
        timedelta = datetime.now(launch_time.tzinfo) - launch_time
        time_dict[key] = timedelta.days
    return time_dict


def handler():
    new_dict = {}
    for asg_name, list_of_instances in describe_asg().items():
        new_dict[asg_name] = instance_time(describe_instances(list_of_instances))
    return new_dict

# for i in handler().items():
#     print(i)