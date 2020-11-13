import desc_asg
import desc_images
import instance_uptime
import graphyte

asg_data = desc_asg.asg_age_handler()
ami_data = desc_images.dictionary_handler_assign()
instance_data = instance_uptime.handler()


def remove_code(asg_name):
    split = asg_name.split('-asg', 1)[0]
    return split


def asg_looper(asg_dict):
    for asg_name, dictionary in asg_dict.items():
        asg_name = remove_code(asg_name)
        for launch_conf, asg_age in dictionary.items():
            send_asg_data(asg_name, asg_age)


def send_asg_data(asg, age):
    # print(asg)
    # print(age)
    graphyte.init('graphite', prefix='sam')
    graphyte.send('asg.'+asg+'.'+asg+'.asg-age-days', age)


def ami_looper(ami_dict):
    for asg_name, dictionary in ami_dict.items():
        asg_name = remove_code(asg_name)
        for image, asg_age in dictionary.items():
            send_ami_data(asg_name, image, asg_age)


def send_ami_data(asg, ami, age):
    # print(asg)
    # print(ami)
    # print(age)
    graphyte.init('graphite', prefix='sam')
    graphyte.send('asg.'+asg+'.'+ami+'.ami-age-days', age)


def instance_looper(instance_dict):
    for asg_name, dictionary in instance_dict.items():
        asg_name = remove_code(asg_name)
        for instance_name, asg_age in dictionary.items():
            send_instance_data(asg_name, instance_name, asg_age)


def send_instance_data(asg, instance, age):
    # print(asg)
    # print(instance)
    # print(age)
    graphyte.init('graphite', prefix='sam')
    graphyte.send('asg.'+asg+'.'+instance+'.instance-age-days', age)


asg_looper(asg_data)
ami_looper(ami_data)
instance_looper(instance_data)
