![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.


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


