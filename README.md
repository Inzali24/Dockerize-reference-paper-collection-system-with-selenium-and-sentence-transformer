# Dockerize-reference-paper-collection-system-with-selenium-and-sentence-transformer 
## Set up & Installation.
## Run the frontend and backend Application with Docker
## Clone/Fork the Git repository
### 1. Navigate to the frontend project directory
`cd automation`
### 2. Docker Build using frontend DockerFile in project
**Windows**

`docker build -t frontend .`
<br>

**macOS/Linux**

`docker build -t frontend .`

### 3. Navigate to the backend project directory

`cd matching`

### 4. Docker Build using backend DockerFile in project

**Windows**

`docker build -t backend .`
<br>

**macOS/Linux**

`docker build -t backend .`

### 5. See the Docker image          

**Windows** 

```docker images```          

**macOS/Linux**

```$docker images```

You will see your image like this.

| REPOSITORY | TAG | IMAGE ID | CREATED | SIZE |
|  ----------------- | ----------------- | ----------------- | ----------------- | ----------------- |
| frontend | latest | 5457fc3fd8bb | 1 minute ago | 1.25GB |
| backend | latest | 8a8d86377604 | 2 minutes ago | 8.09GB |

### 6. Run Docker image

`docker run -dp 4200:4200 frontend`
`docker run -dp 5000:5000 backend`

### 5. Run Docker image

Now the system is running in port:4200 and you can access from browser via localhost:4200

## Congratulations! You can now search the most relevant references for your paper.

