### 1. Install Docker on AWS EC2 (Linux 2):

Add the below snippet to the `user data` during the creating of the EC2 instance.

```
#! /bin/sh
yum update -y
amazon-linux-extras install docker
service docker start
usermod -a -G docker ec2-user
chkconfig docker on
```
---

### 2. Install Portainer:

[Portainer official website](https://docs.portainer.io/v/ce-2.9/start/install/server/docker/linux)



1. Create a volume for Portainer:

```
docker volume create portainer_data
```

2. Download and install Poetainer Server container:

```
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:latest
```

3. Access Portainer User Interface using the instance public IP address and port `9443`. Make sure you're using `https` protocol. 


https://EC2-public-IP-Address:9443


**Note** make sure you add a rule to the EC2 security group to open port *9443* to your local IP address. 

---

### 3. Dockerize Hello World Java Application:

1. Create a `Dockerfile` in the opt folder:

```
cd /opt/ 
sudo mkdir helloworld && cd helloworld
sudo nano Dockerfile
```

2. Paste the below snippet into the Dockerfile and save it:

```
------------
# A custom docker image with OpenJava 11, Tomcat 9 with default ROOT and HelloWorld applications
# The valid uri are / and /HelloWorld
# ---------------------------------------------------------------------------------------------

FROM openjdk:11
MAINTAINER Greatlearning

RUN apt update \
    && apt install -y wget \
    && mkdir /opt/tomcat/

RUN wget https://d6opu47qoi4ee.cloudfront.net/tomcat/apache-tomcat-9.0.53.tar.gz \
    && tar xvfz apache*.tar.gz \
    && mv apache-tomcat-9.0.53/* /opt/tomcat/. \
    && cd /opt/tomcat/webapps \
    && wget https://d6opu47qoi4ee.cloudfront.net/HelloWorld.war \
    && java -version

WORKDIR /opt/tomcat/webapps

EXPOSE 8080

CMD ["/opt/tomcat/bin/catalina.sh", "run"]
```

> Note: to save the file using `nano` text editor:
a. hold down `ctrl` and click `x`

b. type in `y`

c. click enter


