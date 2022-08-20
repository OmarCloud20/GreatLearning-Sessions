### What is AWS Session Manager 

Session Manager is a fully managed AWS Systems Manager capability. Session Manager allows to access and manage Amazon EC2 fromm a browser without the need to SSH into the EC2. For more information about [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) refer to AWS documentation. 


---

### How to Configure Session Manager 

1. Create an IAM role.
2. Attach AWS managed policy `AmazonSSMManagedInstanceCore` to the role. 
3. Attach the role to the EC2. 


For more details about Session Manager configuration, refer to [AWS documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-instance-profile.html)