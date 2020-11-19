#!/usr/bin/env python

import telemetry.telescope_ec2_age.send_graphite_message as send_graphite_message
import telemetry.telescope_ec2_age.desc_asg as desc_asg
import telemetry.telescope_ec2_age.desc_images as desc_images
import telemetry.telescope_ec2_age.instance_uptime as instance_uptime
from telemetry.telescope_ec2_age.logger import get_logger

asg_data = desc_asg.asg_age_handler()
ami_data = desc_images.dictionary_handler_assign()
instance_data = instance_uptime.handler()

if __name__ == '__main__':
    logger = get_logger()
    logger.debug("Starting application...")
    exit(0)
    send_graphite_message.publish_asgs_to_graphite(asg_data)
    send_graphite_message.publish_amis_to_graphite(ami_data)
    send_graphite_message.publish_instances_to_graphite(instance_data)