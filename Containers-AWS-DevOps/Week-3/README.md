# DevOps Tutorial:
 
# CI/CD using AWS Pipeline to Build and Deploy Containers on AWS Fargate

### Prerequisites

1. We have an existing ECR cluster.
2. We have a running Task Definition using an image from ECR repo.
3. We will spin up **Cloud9** instance to push to files to CodeCommit repo. 


**Note** follow the resources/files naming as per the tutorial. 


### 1. Create a Private Image Repository in AWS ECR (Elastic Container Registry):


- Name the ECR repo, **mysite**. The repo **URI** should similar to below:

``xxxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/mysite``


**Note** make sure you create the repository in the same AWS region where you intend to create and run the pipeline.

### 2. Create AWS CodeCommit repository

- Name the CodeCommit repo, **mysite**. Clone the **mysite** repo to **Cloud9**. Then, clone the below GitHub repo as well. The GitHub repo contains all files for the static website and the pipeline. Move all files in folder Week-3 of Containers-AWS-DevOps to the CodeCommit repo, **mysite**. 


[GreatLearning-Sessions](https://github.com/OmarCloud20/GreatLearning-Sessions)

- Once all files are moved to **mysite** folder (local repo) in Cloud9, push the files to CodeCommit using the below git commands:

```
git add .
git commit -am "first commit"
git push
```

- Check out CodeCommit and you should see all pushed files in the repo. 

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