# telescope-ec2-age

## Ticket

Problem 
    The telemetry team do not currently have good visibility of the age of the AMIs that are running. We need better observability of instance lifecycles to see how quickly changes in Git make their way to deployment, and to give us better visibility of how old and therefore how at risk they are. 
 
Requirements
    Python
    Tests
 

Suggested Methodology
 
    Find all ASGs (Auto Scaling Groups)
    Find Launch Configuration for each ASG
    Get age of AMI configured in Launch Configuration
    Record age of AMI in use by ASG


Questions / Known Unknowns
    Where to host, maybe a Lambda, maybe collectd (problem with cross account access to AMI details?)?
    How often we 
 
Notes
    Infra has built a Lambda which does a lot of this but does not record the data - it just fires notifications at Slack, we can provide contact details for this.
    ASG age can be derived from the ASG name as well as via API call.
    
Future features
    Count of EC2 instances per ASG
    Age of AMI in use by each EC2 instance
 

Acceptance Criteria
    New metrics path in Grafana for ASG AMI age, something like "asg.<asg-base-name>.ami-age"
    New metrics path in Grafana for ASG creation time, something like "asg.<asg-base-name>.asg-age"
    A dashboard for teams to use to view:
    Uptime of instances in ASG
    Age of AMI in use by ASG
    How long since ASG was last deployed

    
### License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").
