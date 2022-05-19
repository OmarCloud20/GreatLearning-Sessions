# How to Install and Configure AWS Unified CloudWatch Agent on AWS EC2 (Ubuntu 20.04 LTS):

### The Unified CloudWatch agent enables you to do the following:

1. Collect more system-level metrics from Amazon EC2 instances across operating systems. The metrics can include in-guest metrics, in addition to the metrics for EC2 instances. 

2. Collect system-level metrics from on-premises servers. These can include servers in a hybrid environment as well as servers not managed by AWS.

3. Retrieve custom metrics from your applications or services using the StatsD and `collectd` protocols. `StatsD` is supported on both Linux servers and servers running Windows Server. `collectd` is supported only on Linux servers.

4. Collect logs from Amazon EC2 instances and on-premises servers, running either Linux or Windows Server.

---

### Step 1: Setting up the environment:

1. Creating the EC2 instance : Create a new EC2 instance (t2.micro running Ubuntu 20.04 LTS). Make sure port 22 is open in the instance security group. 

2. Attach the pre-created IAM role “LabInstanceProfile” to the EC2 instance created above. Alternatively, if you are performing this on your personal account, you will need to create an IAM role with the CloudWatchFullAccess policy attached.

3. Log in to the instance using your preferred SSH client of choice.

4. Run the following commands to install the required dependencies:

```
sudo apt update && sudo apt install collectd -y && sudo apt install awscli -y
```

Now, let's configure the AWS CLI and leave the access keys and secret access keys fields blank. We will need to just configure the region code to point to `us-east-1` and the output format as “json”. Note, you might give this profile an arbitrary name. 

```
aws configure --profile [name for the profile]
```
---

### Step 2: Installing Cloudwatch Agent:

1. Install the agent using the following steps:


```
sudo chown ubuntu:ubuntu -R /opt
mkdir /opt/softwares
cd /opt/softwares
get https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
```

2. Start the installation wizard using the following command:

```
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

> Note: Enable the "common metrics" by selecting the defaults for all the questions. Collect logs from directory `/var/log/syslog` and select **Advanced** for the question “Which default metrics config do you want?”.


Please, refer to [AWS documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/create-cloudwatch-agent-configuration-file-wizard.html) for more details about creating the CloudWatch agent configuration file. 

---


### Step 3: Observing the Output:


1. In the CloudWatch management console, select metrics under the “EC2” namespace as well to see the metrics being monitored.

2. Also, under `Custom Namespaces` metrics, select `CWAgent` and observe the metrics being monitored. 

> Note that this might take some time to show up. 


---