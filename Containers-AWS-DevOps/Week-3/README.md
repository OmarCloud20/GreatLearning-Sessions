# DevOps Tutorial:
 
# CI/CD using AWS Pipeline to Build and Deploy Containers on AWS Fargate

### Prerequisites

1. We have an existing ECR cluster.
2. We have a running Task Definition. 
3. We will spin up **Cloud9** instance to push to files CodeCommit repo. 


**Note** to avoid any hiccups, follow the resources/files naming as per the tutorial. 


### 1. Create a Private Image Repository in AWS ECR (Elastic Container Registry):

- Name the ECR repo, **mysite**.  repo URI should similar to below:

``xxxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/mysite``


**Note** make sure you create the repository in the same AWS region where you intend to create and run the pipeline.

### 2. Create AWS CodeCommit repository

- Name the CodeCommit repo, **mysite**. Clone the **mysite** repo to **Cloud9**. Then, clone the below GitHub repo as well. The GitHub repo contains all files for the static website and the pipeline. Move all files from the GitHub repo (Containers-AWS-DevOps -> Week-3) to the CodeCommit repo, **mysite**. 


[GreatLearning-Sessions](https://github.com/OmarCloud20/GreatLearning-Sessions)