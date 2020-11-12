import boto3
from datetime import timedelta, datetime, tzinfo

autoscaling_client = boto3.client('autoscaling', region_name='eu-west-2')


def handle_launch_conf_dict():
    asg_dict, conf_diction = describe_asgs_launch_conf()
    return filter_dict(conf_diction)


def asg_age_handler():
    asg_dict, conf_diction = describe_asgs_launch_conf()
    return asg_dict


def describe_asgs_launch_conf():
    response = autoscaling_client.describe_auto_scaling_groups()
    conf_dict = {}
    asg_dict = {}
    for asg in response["AutoScalingGroups"]:
        asg_name = asg["AutoScalingGroupName"]
        asg_launch = asg.get("LaunchConfigurationName")
        asg_time = asg["CreatedTime"]

        uptime = age_returner(asg_time)

        asg_dict[asg_name] = {asg_launch: uptime}
        conf_dict[asg_name] = asg_launch
    return asg_dict, conf_dict


def filter_dict(conf_diction):
    filtered_absent_confs = {}
    for key, value in conf_diction.items():
        if value != None:
            filtered_absent_confs[key] = value
    return filtered_absent_confs


def age_returner(age):
    timedelta = datetime.now(age.tzinfo) - age
    return timedelta.days

# for i in asg_age_handler().items():
#     print(i)