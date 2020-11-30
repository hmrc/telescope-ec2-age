from telemetry.telescope_ec2_age.desc_asg import describe_asgs_launch_conf


#should refactor asgs for response being outside function
def test_response_get():
    test_response = 'test'
    describe_asgs_launch_conf(test_response)

def test_response():
    asg_dict, conf_dict = describe_asgs_launch_conf()
    assert type(asg_dict) == dict
    assert type(conf_dict) == dict
    for asg_name, dict in asg_dict.items():
        assert asg_name == type(str)
        for asg_launch, uptime in dict.items():
            assert  asg_launch == type(str)
            assert uptime == type(int)
