# DevOps Tutorial:
 
# CI/CD using AWS Pipeline to Build and Deploy Containers on AWS Fargate

### Prerequisites

1. We have an existing ECS cluster.
2. We have a running Task Definition using an image from ECR repo.
3. We will spin up **Cloud9** instance to push to files to CodeCommit repo. 


**Note** follow the resources/files naming as per the tutorial. 
---
<br />

### 1. Create a Private Image Repository in AWS ECR (Elastic Container Registry):


- Name the ECR repo, **mysite**. The repo **URI** should similar to below:

``xxxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/mysite``


**Note** make sure you create the repository in the same AWS region where you intend to create and run the pipeline.

---
<br />

### 2. Create AWS CodeCommit repository

- Name the CodeCommit repo, **mysite**. Clone the **mysite** repo to **Cloud9**. Then, download the [mysite.zip](https://github.com/OmarCloud20/GreatLearning-Sessions/tree/main/Containers-AWS-DevOps/Week-3/mysite.zip) and extract it in the CodeCommit repo, **mysite**. 

```
sudo wget https://github.com/OmarCloud20/GreatLearning-Sessions/raw/main/Containers-AWS-DevOps/Week-3/mysite.zip
unzip mysite.zip
```

Then, we will move all files from **mysite** to local directory:
```
mv mysite/* .
```


- Once all files are moved to **mysite** folder (local repo) in Cloud9, push the files to CodeCommit using the below git commands:

```
git add .
git commit -am "first commit"
git push
```

- Check out CodeCommit and you should see all pushed files in the repo. 

---
<br />

### 3. Create AWS CodePipeline:

1. Add CodeCommit as a source stage.
2. Add CodeBuild as a build stage.
3. Create a build project:
    Under **Environment:**
    - Managed image
    - Operating system: Ubuntu
    - Runtime(s): Standard
    - Image: aws/codebuild/standard:5.0
    - Environment type: Linux
    - Privileged: **check** this option 
    - New service role: leave the default role name as it. A new role will be created. Capture the role's ARN because we will need to create an inline policy to allow CodeBuild to push to images to ECR. 
    - Under **Additional configuration**: click on **Add environment variabless** and then add the following:

    <br />

    | Name              | Value               |     Type     |
    | :----:            | :----:             |  :----: |
    | AWS_DEFAULT_REGION| us-east-1           |   Plaintext  | 
    | AWS_ACCOUNT_ID    | your-aws-account-#  |   Plaintext  |
    | IMAGE_TAG         | latest              |   Plaintext  |
    | IMAGE_REPO_NAME   | your-ECR-repo-name (not URI)  |   Plaintext  |

    - No further changes are needed. Click on **Continue to CodePipeline**
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

4. Skip adding a deploy stage. 



**Note** the Pipeline will run as soon as the CodeCommit repo is updated, and if it succeeds, we shall see the new image in our ECR repo. 


We have completed creating building images and pushing them to our private ECR repo successfully. 

---
<br />

### 4. Deploy a Static Website Container from ECR to Fargate:

- We will need to use the old ECS console to create a Task Definition for our static website container. Under **Task execution IAM role**, if we don't find **ecsTaskExecutionRole**, then we need to create one as this role authorized ECS to pull private images. 

From the IAM console and under Roles: 

1. Create a role.
2. Under **Use cases for other AWS services**, select **Elastic Container Service**.
3. Then, select, **Elastic Container Service Task**. Next. 
4. Add permission policy **AmazonECSTaskExecutionRolePolicy** to the role. 
5. Name the role, **ecsTaskExecutionRole**

For information about how to configure this role, please refer to [AWS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html). You may also find [How do I allow Amazon ECS tasks to pull images from an Amazon ECR image repository](https://aws.amazon.com/premiumsupport/knowledge-center/ecs-tasks-pull-images-ecr-repository/) article beneficial. 


**Note** once you have created **ecsTaskExecutionRole**, you can proceed a create a Task Definition using the URI from the ECR private repo. Then, deploy the Task Definition as a service to the ECS cluster. Verify that the static website is up and running prior to proceeding to the next step.

---
<br />

### 5. Add a Deployment Stage to the Pipeline:

This is stage is to deploy a container from the newly built image of our static website from the private ECR to Fargate. 

**Note** for input artifacts, select **BuildArtifact**. 