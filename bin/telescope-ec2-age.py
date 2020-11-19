#!/usr/bin/env python
import logging

import fire

import telemetry.telescope_ec2_age.send_graphite_message as send_graphite_message
import telemetry.telescope_ec2_age.desc_asg as desc_asg
import telemetry.telescope_ec2_age.desc_images as desc_images
import telemetry.telescope_ec2_age.instance_uptime as instance_uptime
from telemetry.telescope_ec2_age import APP_NAME, APP_VERSION
from telemetry.telescope_ec2_age.logger import create_app_logger


def main(log_level=logging.INFO, graphite_host="graphite"):
    logger = create_app_logger(log_level)
    logger.info("Running %s v%s" % (APP_NAME, APP_VERSION))
    asg_data = desc_asg.asg_age_handler()
    ami_data = desc_images.dictionary_handler_assign()
    instance_data = instance_uptime.handler()

    send_graphite_message.publish_asgs_to_graphite(asg_data, graphite_host)
    send_graphite_message.publish_amis_to_graphite(ami_data, graphite_host)
    send_graphite_message.publish_instances_to_graphite(instance_data, graphite_host)


if __name__ == '__main__':
    fire.Fire(main)
