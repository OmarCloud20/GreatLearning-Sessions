# How to Install and Configure AWS Unified CloudWatch Agent on AWS EC2 (Ubuntu 20.04 LTS):

### The Unified CloudWatch agent enables you to do the following:

1. Collect more system-level metrics from Amazon EC2 instances across operating systems. The metrics can include in-guest metrics, in addition to the metrics for EC2 instances. 

2. Collect system-level metrics from on-premises servers. These can include servers in a hybrid environment as well as servers not managed by AWS.

3. Retrieve custom metrics from your applications or services using the StatsD and `collectd` protocols. `StatsD` is supported on both Linux servers and servers running Windows Server. `collectd` is supported only on Linux servers.

4. Collect logs from Amazon EC2 instances and on-premises servers, running either Linux or Windows Server.

---

### Step 1: Setting up the environment:

1. Creating the EC2 instance : Create a new EC2 instance (t2.micro running Ubuntu 20.04 LTS). Make sure port 22 is open in the instance security group. 

2. Attach the pre-created IAM role “LabInstanceProfile” to the EC2 instance created above. Alternatively, if you are performing this on your personal account, you will need to create an IAM role with the CloudWatchFullAccess policy attached. Please, refer to [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-iam-roles-for-cloudwatch-agent-commandline.html) to create an IAM role to use with the CloudWatch agent on an EC2 instance. Once you have the role created, you would need to attach to the EC2 instance. 

> Note: the needed AWS managed policy is `CloudWatchAgentServerPolicy`. Moreover, we might need to add an inline policy to allow the agent to modify the retention policy. 

3. Log in to the instance using your preferred SSH client of choice.

4. Run the following commands to install the required dependencies:

```
sudo apt update && sudo apt install collectd -y && sudo apt install awscli -y
```

Now, let's configure the AWS CLI and leave the access keys and secret access keys fields blank. We will need to just configure the region code to point to `us-east-1` and the output format as “json”.

```
aws configure
```
---

### Step 2: Installing Cloudwatch Agent:

1. Install the agent using the following steps:


```
sudo chown ubuntu:ubuntu -R /opt
mkdir /opt/softwares
cd /opt/softwares
```
```
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
```

2. Start the installation wizard using the following command:

```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

> Note: Enable the "common metrics" by selecting the defaults for all questions. Collect logs from directory `/var/log/syslog` and select **Advanced** for the question **Which default metrics config do you want?.** 


Please, refer to [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-cloudwatch-agent-configuration-file-wizard.html) for more details about creating the CloudWatch agent configuration file. 

3. Start the CloudWatch agent:

To start the agent fot the first time, run the below command:

```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s
```
For more information about this command, refer to [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-commandline-fleet.html#:~:text=Start the CloudWatch agent using the command line).

> Note: if we need to start, restart, stop or even check the status of the CloudWatch agent, we can use the below commands:

```
sudo systemctl status amazon-cloudwatch-agent.service
sudo systemctl start amazon-cloudwatch-agent.service
sudo systemctl restart amazon-cloudwatch-agent.service
sudo systemctl stop amazon-cloudwatch-agent.service
```

---


### Step 3: Observing the Output:


1. From the CloudWatch management console, select metrics under the custom `CWAgent` namespace. Explore the metrics being monitored.

2. Also, under `EC2` Namespaces metrics, select `Per-Instance Metrics` and observe the metrics being monitored for the Instanceid and Instance name. 

> Note that this might take some time to show up. 

---

### Extra Mile: A Stress Tool to Simulate a Stress for testing:


`Sysbench` is a command line app to run benchmarks on our system/instance. It is mainly intended for testing CPU, memory and file throughput as well. We can install this utility to simulate a stress on our EC2 to push CloudWatch agent to present it on our metrics.

To install Sysbench in Ubuntu, run the command below:

```
sudo apt install sysbench
```
We can increase or decrease the threads to simulate the stress:

```
sysbench cpu --threads=5 run
```

Monitor the results of the stress on our EC2 instance by Sysbench.

