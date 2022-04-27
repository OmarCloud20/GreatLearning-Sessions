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
docker run -d -p 5000:80 site_1
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
docker run -d -p 6000:80 site_2
```
**Note:** we have mapped the container port 80 to the host on port 6000. We can change the host port to any other port as we like.


We have successfully containerized our static website and we can view the site on *public-IP-address:6000*.

---


#### Conclusion: 

By running command `docker images`, we shall see all images on our device. Notice the difference in size between the site_1 and site_2 images. The difference in size is due to the base images we have utilized to build these Docker images. Keep this in mind when you create images in the future. 

Also, notice that we have not mapped the volume to persist the data. Without creating a container volume or mapping to a local storage volume, any changes made to the data or files are not persistent and will be lost once the container is stopped.



---
