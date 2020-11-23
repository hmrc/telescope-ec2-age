from telemetry.telescope_ec2_age.send_graphite_message import remove_asg_suffix_code


def test_remove_asg_suffix_code():
    asg_name = "classic-services-admin-asg-20180820125956688700000007"
    expected_result = "classic-services-admin"

    result = remove_asg_suffix_code(asg_name)
    assert result == expected_result