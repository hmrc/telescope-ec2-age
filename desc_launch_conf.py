import boto3
import desc_asg
autoscaling_client = boto3.client('autoscaling', region_name='eu-west-2')


def handler_launch_images():
    return iterator(recieve_launch_confs_from_asg())


def recieve_launch_confs_from_asg():
    conf_dict = desc_asg.handle_launch_conf_dict()
    return conf_dict


def iterator(dict_asg_conf):
    data_dict = {}
    for asg_name, conf_name in dict_asg_conf.items():
        dictionary = describe_launch_conf(conf_name)
        data_dict[asg_name] = dictionary
    return data_dict


def describe_launch_conf(launch_name):
    response = autoscaling_client.describe_launch_configurations(
        LaunchConfigurationNames=[
            launch_name
        ]
    )
    for launch_config in response["LaunchConfigurations"]:
        image_id = launch_config["ImageId"]
        lcn = launch_config["LaunchConfigurationName"]
        return {lcn: image_id}

# for i in handler_launch_images().items():
#     print(i)