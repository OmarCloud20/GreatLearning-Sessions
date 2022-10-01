# How to Install and Configure AWS Unified CloudWatch Agent on AWS EC2 (Ubuntu 20.04 LTS):

### The Unified CloudWatch agent enables you to do the following:

1. Collect more system-level metrics from Amazon EC2 instances across operating systems. The metrics can include in-guest metrics, in addition to the metrics for EC2 instances. 

2. Collect system-level metrics from on-premises servers. These can include servers in a hybrid environment as well as servers not managed by AWS.

3. Retrieve custom metrics from your applications or services using the StatsD and `collectd` protocols. `StatsD` is supported on both Linux servers and servers running Windows Server. `collectd` is supported only on Linux servers.

4. Collect logs from Amazon EC2 instances and on-premises servers, running either Linux or Windows Server.

---

## Step 1: Spinning up an EC2:

1. Spin up an EC2 instance:

A. Spin up an EC2 instance (t2.micro running Ubuntu 20.04 LTS). 
B. Open port 22 to your local IP address. 

2. Attach the pre-created IAM role “LabInstanceProfile” to the EC2 instance created above (according to the lab). 

Alternatively, if you are running this lab on your personal account, you will need to create an IAM role with the CloudWatchFullAccess policy attached. Please, refer to [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-iam-roles-for-cloudwatch-agent-commandline.html) for more information on how create an IAM role to use with the CloudWatch agent on an EC2 instance. Once you have the role created, attach it to the EC2 instance. 

> Note: the needed AWS managed policy is `CloudWatchAgentServerPolicy`. Moreover, we might need to add an inline policy to allow the agent to modify the retention policy. 

3. SSH to the EC2 instance.

4. Run the following commands to install the required dependencies:

```
sudo apt update
sudo apt install collectd -y
sudo apt install awscli -y
```
5. let's configure the AWS CLI and leave the access keys and secret access keys fields blank. We will need to just configure the region code to point to `us-east-1` and the output format as “json”.

```
aws configure
```


## Step 2: Installing Cloudwatch Agent:


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



- For the question **Do you want to turn StatsD daemon**, select **no**.
- For the question **Which default metrics config do you want?**, select **Advanced**.
- For the question **Do you want to monitor any log files?**, select **yes** and enter the following log file path: `/var/log/syslog`
- For the question **Do you want to specify any additional log files to monitor?**, select **no**.
- For the question **Do you want to store the config in the SSM parameter store?**, select **no**.

All other questions can be answered with the default values.


Please, refer to [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-cloudwatch-agent-configuration-file-wizard.html) for more details about creating the CloudWatch agent configuration file. 

3. Start the CloudWatch agent:

To start the agent for the first time, run the below command:

```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s
```
For more information about this command, refer to [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-commandline-fleet.html#:~:text=Start%20the%20CloudWatch%20agent%20using%20the%20command%20line).


<br>
> Note: if we need to start, restart, stop or even check the status of the CloudWatch agent, we can use the below commands:

```
sudo systemctl status amazon-cloudwatch-agent.service
sudo systemctl start amazon-cloudwatch-agent.service
sudo systemctl restart amazon-cloudwatch-agent.service
sudo systemctl stop amazon-cloudwatch-agent.service
```




## Step 3: Observing the Outputs:


From the CloudWatch management console, select `Metrics` on the left hand menu. Then click on `All metrics`. Under `Custom namespaces`, click on `CWAgent` namespace to explore the metrics being monitored.


> Note the metrics might take some time to show up. 

---

## An Extra Mile: A Stress Tool to Simulate a Stress Test:


[Sysbench](https://github.com/akopytov/sysbench) is a command line tool to run benchmarks on our system/instance. It is mainly intended for testing CPU, memory and file throughput as well. We can install this utility to simulate a stress on our EC2.


To install `Sysbench` on Ubuntu, run the command below:

```
sudo apt install sysbench -y
```

We can increase or decrease the threads to simulate the magnitude of the stress:

```
sysbench cpu --threads=5 run
```
```
sysbench memory --threads=5 run
```


From the CloudWatch console under metrics, monitor the results of the stress test on the EC2 instance.

---



