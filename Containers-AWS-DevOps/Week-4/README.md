# Terraform Tutorial
 
## Create Terraform templates to spin up an EC2 and to create an S3 bucket

### Prerequisites

1. Install AWS CLI v2
2. Create an AWS IAM user 
3. Install Terraform

---
<br />

### 1. Install AWS CLI v2


Refer to [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) for installing the AWS CLI version 2. 

- For Linux x86 (64-bit):


```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- To inspect the version of the AWS CLI on Linux:

```
aws --version
```

---
<br />

### 2. Create an AWS IAM user to run Terraform from a local device

For CLI access, we need an access key ID and secret access key. Therefore, we need to create an IAM user to obtain the access keys instead of AWS account root user access keys. IAM lets us securely control access to AWS services and resources in your AWS account. 

Once we have created an IAM user and have obtained the access keys, we will configure the AWS CLI. During the configuration process, we will enter the access key ID, secret access key, default region name and default output format. Below is an example. 


| Prompt                            | Example Value                           |     
| :-------------------------------: | :---------------------------------------: |  
| AWS Access Key ID [None]:         | AKIAIOSFODNN7EXAMPLE                      |   
| AWS Secret Access Key [None]:     | ywJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY | 
| Default region name [None]:       | us-east-1                                 |  
| Default output format [None]:     | json                                      | 


Now, let's configure the AWS CLI:

```
aws configure --profile Terraform
```

**Note** add flag `profile` to the command is to give this profile a name and to refrain from using it as a default profile. The profile flag is very handy, especially if you have multiple profile configured. **BuildArtifact**. 
---
<br />

### 3. Install Terraform

Refer to [Download Terraform](https://www.terraform.io/downloads) official site to download and install Terraform for your environment. 

- For Linux Ubuntu/Debian (amd64):

```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
```

- To inspect the version of Terraform on Linux:

```
terraform --version
```

---
<br />

### Basic Terraform Commands

| Commands            | Usage             |     
| :----:            | :----:             |  
| terraform init| Download any plugins required to run templates         |   
| terraform plan  | Will give you a list of resources that will be created/deleted |  
| terraform apply        | WIll create/delete resources            |   
| terraform destroy  | Will delete all the resources created by Terraform  |   
| terraform fmt | Will format the file with proper indentation |   

---
<br />

### Terraform to spin up an EC2

Utilize any text/code editor of your choice, create a file with a `.tf` extension and paste the below:

```
provider "aws" {
    profile = "Terraform"
    region = "us-east-1"
    
}

resource "aws_instance" "demo_instance" {
   
    ami = "ami-042e8287309f5df03"
    instance_type = "t2.micro"
    
    tags = {
        Name = "Terraform_Demo"
        
          }
    
}
```


Run the below Terraform commands to provision the EC2:

```
terraform init
terraform plan
terraform apply
```

Run the below Terraform command to destroy the EC2:

```
terraform destroy
```

---
<br />

### Terraform to create an S3 bucket


Utilize any text/code editor of your choice, create a file with a `.tf` extension and paste the below:

```
provider "aws" {
    profile = "Terraform"
    region = "us-east-1"
    
}

resource "aws_instance" "demo_instance" {
   
    ami = "ami-042e8287309f5df03"
    instance_type = "t2.micro"
    
    tags = {
        Name = "Terraform_Demo"
        
          }
    
}
```


Run the below Terraform commands to provision the EC2:

```
terraform init
terraform plan
terraform apply
```

Run the below Terraform command to destroy the EC2:

```
terraform destroy
```

---
<br />

