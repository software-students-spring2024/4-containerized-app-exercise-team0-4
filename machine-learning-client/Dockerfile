FROM python:3.8-slim-buster
WORKDIR /machine-learning-client
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ADD . .
CMD [ "python3", "main.py"]