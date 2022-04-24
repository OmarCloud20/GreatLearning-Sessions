### 1. Install Docker on AWS EC2 (Linux 2):

```
#! /bin/sh
yum update -y
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
chkconfig docker on
```


### 2. Install Portainer:

[Portainer official website](https://docs.portainer.io/v/ce-2.9/start/install/server/docker/linux)



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