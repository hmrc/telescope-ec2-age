import desc_asg
import desc_images
import instance_uptime
import graphyte
import logging
import sys


def get_logger():
    logger = logging.getLogger('telescope-ec2-age')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = get_logger()

asg_data = desc_asg.asg_age_handler()
ami_data = desc_images.dictionary_handler_assign()
instance_data = instance_uptime.handler()


def remove_asg_suffix_code(asg_name):
    split = asg_name.split('-asg', 1)[0]
    return split


def publish_asgs_to_graphite(autoscaling_groups_data):
    logger.info("Publishing ASG age to graphite")
    for asg_name, conf_and_age in autoscaling_groups_data.items():
        asg_name = remove_asg_suffix_code(asg_name)
        for launch_conf, asg_age in conf_and_age.items():
            send_asg_data(asg_name, asg_age)


def send_asg_data(asg, age):
    # print(asg)
    # print(age)
    graphyte.init('graphite', prefix='sam')
    graphyte.send('asg.' + asg + '.' + asg + '.asg-age-days', age)


def publish_amis_to_graphite(images_data):
    for asg_name, image_and_age in images_data.items():
        asg_name = remove_asg_suffix_code(asg_name)
        for image, asg_age in image_and_age.items():
            send_ami_data(asg_name, image, asg_age)


def send_ami_data(asg, ami, age):
    # print(asg)
    # print(ami)
    # print(age)
    graphyte.init('graphite', prefix='sam')
    graphyte.send('asg.' + asg + '.' + ami + '.ami-age-days', age)


def publish_instances_to_graphite(instances_data):
    for asg_name, instances_and_age in instances_data.items():
        asg_name = remove_asg_suffix_code(asg_name)
        for instance_name, asg_age in instances_and_age.items():
            send_instance_data(asg_name, instance_name, asg_age)


def send_instance_data(asg, instance, age):
    # print(asg)
    # print(instance)
    # print(age)
    graphyte.init('graphite', prefix='sam')
    graphyte.send('asg.' + asg + '.' + instance + '.instance-age-days', age)


if __name__ == '__main__':
    logger.debug("starting application")
    print("test")
    publish_asgs_to_graphite(asg_data)
    publish_amis_to_graphite(ami_data)
    publish_instances_to_graphite(instance_data)
