# telescope-ec2-age
 
### Motivation 
 
The Telemetry team do not currently have good visibility of the age of the AMIs that are running. We need better observability of instance lifecycles to see how quickly changes in Git make their way to deployment, and to give us better visibility of how old and therefore how at risk they are. 
 
## Features

### Current

* Find all ASGs (Auto Scaling Groups)
* Find Launch Configuration for each ASG
* Get age of AMI configured in Launch Configuration
* Record age of AMI in use by ASG 

### Next (scheduled or in development)
    
* Count of EC2 instances per ASG
* Age of AMI in use by each EC2 instance

## Requirements

* [Python >=3.5](https://docs.python.org/3/)
* [Poetry](https://python-poetry.org/)

### Install dependencies

```bash
make build
```

### Run tests

```bash
make test-py3-dev
```

### Run the application

```bash
ssh -L 2003:graphite:2003 <graphite-frontend-ip-address>
aws-profile -p webops-integration-RoleInterimPlatformDeity make run-py3
```

### List actions available

```bash
make help
```

### License

This code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html"). 
 