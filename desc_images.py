from datetime import datetime, timedelta, tzinfo
import boto3
import desc_launch_conf

ec2_client = boto3.client('ec2', region_name='eu-west-2')


def dictionary_handler_assign():
    return launch_dict(recieve_launch_confs_from_launch_conf())


def launch_dict(launch_conf_dict):
    dictionary = {}
    for asg_name, launch_d in launch_conf_dict.items():
        for conf, image in launch_d.items():
            image_age = ami_time_handler(describe_imageIds(image))
            if image_age != None:
                dictionary[asg_name] = {image: image_age}
    return dictionary


def recieve_launch_confs_from_launch_conf():
    return desc_launch_conf.handler_launch_images()


def describe_imageIds(image_id):
    try:
        response = ec2_client.describe_images(
            ImageIds=[
                image_id
            ]
        )
        for image in response["Images"]:
            creation_date = image["CreationDate"]
        return creation_date
    except:
        return


def ami_time_handler(creation_date_string):
    if creation_date_string == None:
        return creation_date_string
    time_obj = datetime.strptime(
        creation_date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    timedelta = datetime.now(time_obj.tzinfo) - time_obj
    return timedelta.days


# for i in dictionary_handler_assign().items():
#     print(i)
