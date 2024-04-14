![Lint-free](https://github.com/software-students-spring2024/4-containerized-app-exercise-team0-4/actions/workflows/lint.yml/badge.svg)
![CI/CD](https://github.com/software-students-spring2024/4-containerized-app-exercise-team0-4/actions/workflows/build.yaml/badge.svg)
![Log](https://github.com/software-students-spring2024/4-containerized-app-exercise-team0-4/actions/workflows/event-logger.yml/badge.svg)

# Voice Memo Recorder App

## Description 
This app is designed to allow users to generate transcripts of voice recordings. It allows users to use their laptop microphone for recording an audio file. This audio file is analyzed by a Machine Learning Client which generates a transcript of the recording. Transcripts are displayed on the web app for the user to view.

## Create Docker network
```
docker network create mynetwork
```

## How to run MongoDB in Container
1. Pull the MongoDB image from Docker
```
docker pull mongo
```
2. Run MongoDB Container
```
docker run --name mongodb -d --network mynetwork mongo
```
 - --name mongodb: Names the container "mongodb" for easier reference.
- -d: Runs the container in detached mode.
- -p 27017:27017: Maps port 27017 on the host to port 27017 in the container.
- mongo: Specifies the image to use.

## How to run Docker for web-app and machine-learning-client
1. Build the Docker container for web-app 
```
cd web-app
docker build -t web-app .
```
2. Build the Docker container for machine-learning-client
```
cd ..
cd machine-learning client
docker build -t machine-learning-client .
```

## Run the Docker Containers for web-app and machine-learning-client in the network

1. Run the Docker container for web-app and machine-learning-client
```
docker run --name web-app -d --network mynetwork -p 5001:5001 web-app
docker run --name machine-learning-client -d --network mynetwork -p 5002:5002 machine-learning-client
```

3. Access the web-app at http://127.0.0.1:5001 or http://localhost:5001/

## Team Members
- [Nathanuel Dixon](https://github.com/nathanuel0322)
- [Aarav Sawlani](https://github.com/aaravsawlani)
- [Josh Forlenza](https://github.com/joshforlenza)
- [Eugene Chang](https://github.com/egnechng)
