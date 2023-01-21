# How to Create ECS Cluster and Task Definition

## Step 1: Create ECS Cluster

**Important:** the below steps are using the new ECS console. 

1. Go to ECS Service
2. Click on Create Cluster
3. Enter the Cluster Name
4. For Networking, leave the selected default VPC and subnet
5. Click on Create

>Note: Fargate is the default launch type for ECS. 

## Step 2: Create Task Definition

1. Go to Task Definitions
2. Click on Create new Task Definition
3. Enter the Task Definition Name
4. Under Container - 1, enter the Container Name and image URI respectively

> Note: The image URI is the URI of the Docker image that you want to run. In our case, it's the URI for mysite repository from ECR.

5. For Container Port, enter 80. This is the port that the container is listening on.
6. Click on "Next"
7. Click on "Next" again
8. Click "Create"

## Step 3: Run Task Definition as a Service

1. Go to the ECS Service
2. Click on the Cluster Name which we created in step 1
3. Under Services, click on Deploy
4. Under Compute configuration, select Launch type as Fargate
5. Under Deployment configuration, select Service
6. Under Task Definition, select the Task Definition Name which we created in step 2 from the drop down menu
7. Under Service name, enter the Service Name
8. Under Number of tasks, enter 1
9. Under Networking, select the default VPC and subnet
10. For Security group, select Create new security group. Enter the Security group name and description. Add Add new rule and add the following inbound rule:
    - Type: HTTP, Source: Anywhere
11. Under Load balancing, select Application Load Balancer to create a new load balancer. Follow the steps to create a new load balancer:
- Enter the Load balancer name
- Choose container to load balance: select the Container Name which we created previously
- Listener port: 80, Protocol: HTTP
- Target group name: enter the Target group name
- Health check path: enter the health check path. In our case, it's /
- Health check interval: 10

12. Click on "Deploy"

## Step 4: Test the Service

1. Go to the ECS Service
2. Click on the Cluster Name which we created in step 1
3. Under Services, click on the Service Name which we created in step 3
4. Click on Networking tab and open the DNS name of the load balancer in a new tab
5. You should see the website running

**Important:** If you see the following error, it means that the security group is not configured correctly. You may click on Logs tab to see the error message.






