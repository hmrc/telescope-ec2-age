import boto3
import telemetry.telescope_ec2_age.desc_launch_conf as desc_launch_conf
import logging
import sys
from botocore.exceptions import ClientError
from datetime import datetime
from telemetry.telescope_ec2_age.logger import get_logger

logger = get_logger()
ec2_client = boto3.client('ec2', region_name='eu-west-2')


def dictionary_handler_assign():
    return launch_dict(receive_launch_confs_from_launch_conf())


def launch_dict(launch_conf_dict):
    dictionary = {}
    for asg_name, launch_d in launch_conf_dict.items():
        for conf, image in launch_d.items():
            image_age = ami_time_handler(describe_image_ids(image))
            if image_age is not None:
                dictionary[asg_name] = {image: image_age}
    return dictionary


def receive_launch_confs_from_launch_conf():
    return desc_launch_conf.handler_launch_images()


def describe_image_ids(image_id):
    try:
        response = ec2_client.describe_images(
            ImageIds=[
                image_id
            ]
        )
        logging.info(response)
        for image in response["Images"]:
            creation_date = image["CreationDate"]
        return creation_date
    except ClientError as e:
        logger.error(str(e))
        return None
    except Exception as e:
        logger.error(str(e))
        return None
    except:
        logger.error("Unexpected error:", sys.exc_info()[0])
        return None


def ami_time_handler(creation_date_string):
    if creation_date_string == None:
        return creation_date_string
    time_obj = datetime.strptime(
        creation_date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    timedelta = datetime.now(time_obj.tzinfo) - time_obj
    return timedelta.days

# for i in dictionary_handler_assign().items():
#     print(i)
