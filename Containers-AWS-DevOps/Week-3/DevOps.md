


### Prerequisites

1. We have an existing ECR cluster.
2. We have a running Task Definition. 
3. We will spin up **Cloud9** instance to push to files CodeCommit repo. 


**Note** follow the resources/files naming as per the tutorial. 


### 1. Create a Private Image Repository in AWS ECR (Elastic Container Registry):

- Name the ECR repo, **mysite**. It repo URI should similar to below:

``xxxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/mysite``


**Note** make sure you create the repository in the same AWS region where you intend to create and run the pipeline.

### 2. Create AWS CodeCommit repository

- Name the CodeCommit repo, **mysite**. Clone the **mysite** repo to **Cloud9**. Then, clone the below GitHub repo as well. The GitHub repo contains all files for the static website and the pipeline. Move all files from the GitHub repo to the CodeCommit repo, **mysite**. 






### 3. Create AWS CodePipeline:

1. Add CodeCommit as a source stage.
2. Add CodeBuild as a build stage.
3. Create a build project:
    A. Under **Environment:**
    - Managed image
    - Operating system: Ubuntu
    - Runtime(s): Standard
    - Image: aws/codebuild/standard:4.0
    - Environment type: Linux
    - Privileged: **check** this option 
    - New service role: leave the default role name as it. A new role will be created. Capture the role's ARN because we will need to create an inline policy to allow CodeBuild to push to images to ECR. 
    - Open a second tab and head to IAM console to create the below inline policy for the CodeBuild role:

        ```
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "VisualEditor0",
                    "Effect": "Allow",
                    "Action": [
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:CompleteLayerUpload",
                        "ecr:GetAuthorizationToken",
                        "ecr:InitiateLayerUpload",
                        "ecr:PutImage",
                        "ecr:UploadLayerPart"
                    ],
                    "Resource": "*"
                }
            ]
        }
        ```
    - Under **Additional configuration**: click on **Add environment variabless** and then add the following:
    
    | Name              | Value               |     Type     |
    | :----:            | :----:             |  :----: |
    | AWS_DEFAULT_REGION| us-east-1           |   Plaintext  | 
    | AWS_ACCOUNT_ID    | your-aws-account-#  |   Plaintext  |
    | IMAGE_TAG         | latest              |   Plaintext  |
    | IMAGE_REPO_NAME   | your-ECR-repo-name  |   Plaintext  |

    - No further changes are needed. Click on **Continue to CodePipeline**
4. Add **AWS ECS** as a deploy stage. 
    - Select existing Cluster and service name.


**Note** the Pipeline will fail the **build stage**. We will need to create a role that allows 



1- Create **ecsTaskExecutionRole**.
2- Select **Elastic Container Service Task**
3- Attach **AmazonECSTaskExecutionRolePolicy**
4- Name the role, **ecsTaskExecutionRole**

[Task!](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html)
https://aws.amazon.com/premiumsupport/knowledge-center/ecs-tasks-pull-images-ecr-repository/



### 2. Install Portainer
https://docs.portainer.io/v/ce-2.9/start/install/server/docker/linux


1- Create a volume for portainer:

```
docker volume create portainer_data
```

2- Download and install Poetainer Server container:

```
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:latest
```

3- Access portainer UI:

https://[EC2-public-IP-Address]:9443


**Note** make sure you add a rule to the EC2 security group to open port *9443* to your local ip address. 