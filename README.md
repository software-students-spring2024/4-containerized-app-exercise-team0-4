![Lint-free](https://github.com/software-students-spring2024/4-containerized-app-exercise-team0-4/actions/workflows/lint.yml/badge.svg)
![CI/CD](https://github.com/software-students-spring2024/4-containerized-app-exercise-team0-4/actions/workflows/build.yaml/badge.svg)
![Log](https://github.com/software-students-spring2024/4-containerized-app-exercise-team0-4/actions/workflows/event-logger.yml/badge.svg)

# Voice Memo Recorder App

## Description 
This app is designed to allow users to generate transcripts of voice recordings. It allows users to use their laptop microphone for recording an audio file. This audio file is analyzed by a Machine Learning Client which generates a transcript of the recording. Transcripts are displayed on the web app for the user to view.

## How to run MongoDB
1. Pull the MongoDB image from Docker
```
docker pull mongo
```
2. Run MongoDB Container
```
docker run --name mongodb -d -p 27017:27017 mongo
```
 - --name mongodb: Names the container "mongodb" for easier reference.
- -d: Runs the container in detached mode.
- -p 27017:27017: Maps port 27017 on the host to port 27017 in the container.
- mongo: Specifies the image to use.

## How to run Docker for web-app and machine-learning-client
1. Build the Docker image for web-app and machine-learning-client
```
docker build -t web-app .
docker build -t machine-learning-client .
```

2. Run the Docker container for web-app and machine-learning-client
```
docker run -p 3000:3000 web-app
docker run machine-learning-client
```

## Team Members
- [Nathanuel Dixon](https://github.com/nathanuel0322)
- [Aarav Sawlani](https://github.com/aaravsawlani)
- [Josh Forlenza](https://github.com/joshforlenza)
- [Eugene Chang](https://github.com/egnechng)
