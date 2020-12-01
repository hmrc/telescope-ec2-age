from telemetry.telescope_ec2_age.send_graphite_message import remove_asg_suffix_code, send_ami_age_data, send_ami_id_data, send_asg_data, send_instance_data


def test_remove_asg_suffix_code():
    asg_name = 'classic-services-admin-asg-20180820125956688700000007'
    expected_result = 'classic-services-admin'

    result = remove_asg_suffix_code(asg_name)
    assert result == expected_result

#this needs refactoring just dummy atm for mock graphite WIP
def test_send_asgs():
    asg_name = 'classic-services-admin-asg'
    asg_age = 0
    graphite_mock = 'mock'
    output = send_asg_data(asg_name, asg_age, graphite_mock)
    expected_output = ''
    assert output == expected_output

def test_send_ami_ids():
    return

def test_send_ami_ages():
    return

def test_send_instances():
    return