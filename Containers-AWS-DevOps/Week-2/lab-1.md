### Containerize a Static HTML Website using Docker

We had previously used this static website in week 3 of the AWS Managed Services module. Now, we will containerize the static website using several base images to compare container sizes. 

---


#### Part 1: Containerize a Static Website using Ubuntu Base Image:

- Navigate to the **opt** folder and create a new folder for the static site by running the following commands:

```
cd /opt/
sudo mkdir Website && cd Website
```

- Run the following command to download and unzip the website zip file in **Website** folder:

```
sudo wget https://github.com/OmarCloud20/GreatLearning-Sessions/raw/main/AWS-Managed-Services/week-3/s3/s3_site.zip
sudo unzip s3_site.zip
```
- Now, we will create a **Dockerfile**:

```
sudo nano Dockerfile
```

- Add the below Docker commands to the Dockerfile and save it.

```
FROM ubuntu
RUN apt-get update
RUN apt-get install nginx -y
COPY . /var/www/html/
EXPOSE 80
CMD ["nginx","-g","daemon off;"]
```

- From within the **Website** folder, run the below command to build the image:

```
 docker build -t site_1 .
```
**Note:** we have defined the name of the image, **site_1**.

- Now, we are ready to run the container for our static website:

```
docker run -d -p 5500:80 site_1
```
**Note:** we have mapped the container port 80 to the host on port 5000. We can change the host port as we like.


We have successfully containerized our static website and we can view the site on *public-IP-address:5000*.

---

#### Part 2: Containerize a Static Website using Nginx Base Image:


- Let's modify our **Dockerfile** to run Nginx base image instead of Ubuntu. From within **Website** folder, run the following command:

```
sudo nano Dockerfile
```

- Replace the previous content with the below Docker commands and save it.

```
FROM nginx
COPY . /usr/share/nginx/html
EXPOSE 80
```


- From within the **Website** folder, run the below command to build the image:

```
 docker build -t site_2 .
```
**Note:** we have defined the name of the image, **site_2**.

- Now, we are ready to run the container for our static site:

```
docker run -d -p 6500:80 site_2
```
**Note:** we have mapped the container port 80 to the host on port 6000. We can change the host port to any other port as we like.


We have successfully containerized our static website and we can view the site on *public-IP-address:6000*.

---

#### Part 3: Containerize a Static Website using Apache httpd Base Image:

- Let's modify our **Dockerfile** to run Nginx base image instead of Ubuntu. From within **Website** folder, run the following command:

```
sudo nano Dockerfile
```

- Replace the previous content with the below Docker commands and save it.

```
FROM httpd:2.4
COPY . /usr/local/apache2/htdocs/
```


- From within the **Website** folder, run the below command to build the image:

```
 docker build -t site_3 .
```
**Note:** we have defined the name of the image, **site_3**.

- Now, we are ready to run the container for our static site:

```
docker run -d -p 7500:80 site_3
```
**Note:** we have mapped the container port 80 to the host on port 6500. We can change the host port to any other port as we like.


We have successfully containerized our static website and we can view the site on *public-IP-address:6500*.

---

#### Part 4: Push the Containerized Static Website to Docker Hub:

- We will tag the image prior to pushing to Docker Hub:

```
docker tag <image id><tag> <dockerhub username>/<repository name>:latest
```

- Login to the Docker Hub from Terminal by running the below command:

```
docker login
```
**Note:** you will be prompted to enter your Docker Hub username and password. 

- We will need to **tag** the docker image as shown below:

Example:

```
docker tag <image id> <dockerhub username>/<repository name>:latest
```

**Note:** the `repository name` is the name you define for the image. 


- Now, we are ready to push the image to Docker Hub:

```
docker push <Docker Hub username>/<repository name>:latest
```

**Note:** to find the image id, run `docker images`. Make sure you Docker Hub repository is public and not private. 


---

#### Part 5: Push the Containerized Static Website to Amazon Elastic Container Registry (ECR):

- We will create a private repository in ECR with the image name. We will either enable/disable the `Tag immutability` option. 

- We will tag the image prior to pushing it to ECR:

```
docker tag <image id>:<tag> <xxxxxxxxxx.dkr.ecr.us-east-1.amazonaws.com/mysite:latest>
```

>Note: from within our private repo in ECR, we should be able to obtain all Docker commands needed to push images to our private repo. 

- Log in into the ECR by obtaining the logging ECR command for our private repo command from within the repo. 


>Note: you might need to configure AWS CLI with valid credentials to authenticate with ECR in your AWS account. 



- Now, we are ready to push the image to ECR. Follow the Docker push command to complete this task. 

---

#### Conclusion: 

By running command `docker images`, we shall see all pulled images on our device. Notice the difference in sizes between the site_1, site_2 and site_3 images. The difference in size is due to the base images we have utilized to build these Docker images. Keep this in mind when you create images in the future. 

Also, notice that we have not mapped the volume to persist the data. Without creating a container volume or mapping to a local storage volume, any changes made to the data or files are not persistent and will be lost once the container is stopped.



---
