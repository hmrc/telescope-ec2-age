import graphyte

from telemetry.telescope_ec2_age import METRICS_PREFIX
from telemetry.telescope_ec2_age.logger import get_app_logger

logger = get_app_logger()


def remove_asg_suffix_code(asg_name):
    print(asg_name)
    split = asg_name.split('-asg', 1)[0]
    print(split)
    return split


def publish_asgs_to_graphite(autoscaling_groups_data, graphite_host):
    logger.info("Publishing ASG age to graphite")
    for asg_name, conf_and_age in autoscaling_groups_data.items():
        asg_name = remove_asg_suffix_code(asg_name)
        for launch_conf, asg_age in conf_and_age.items():
            send_asg_data(asg_name, asg_age, graphite_host)


def send_asg_data(asg, age, graphite_host):
    graphyte.init(graphite_host, prefix=METRICS_PREFIX)
    graphyte.send(asg + '.asg' + '.age-seconds', age)


def publish_amis_to_graphite(images_data, graphite_host):
    logger.info("Publishing AMIs age to graphite")
    for asg_name, image_and_age in images_data.items():
        asg_name = remove_asg_suffix_code(asg_name)
        for image, asg_age in image_and_age.items():
            send_ami_age_data(asg_name, asg_age, graphite_host)
            send_ami_id_data(asg_name, image, graphite_host)


def send_ami_age_data(asg, age, graphite_host):
    graphyte.init(graphite_host, prefix=METRICS_PREFIX)
    graphyte.send(asg + '.ami' + '.age-seconds', age)


def send_ami_id_data(asg, image_id, graphite_host):
    graphyte.init(graphite_host, prefix=METRICS_PREFIX)
    graphyte.send(asg + '.ami.' + image_id, 0)


def publish_instances_to_graphite(instances_data, graphite_host):
    for asg_name, instances_and_age in instances_data.items():
        asg_name = remove_asg_suffix_code(asg_name)
        for instance_name, asg_age in instances_and_age.items():
            send_instance_data(asg_name, instance_name, asg_age, graphite_host)


def send_instance_data(asg, instance, age, graphite_host):
    graphyte.init(graphite_host, prefix=METRICS_PREFIX)
    graphyte.send(asg + "." + instance + '.age-seconds', age)
