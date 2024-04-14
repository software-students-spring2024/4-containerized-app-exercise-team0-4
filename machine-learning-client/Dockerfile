FROM python:3.8
WORKDIR /machine-learning-client
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg
# Install PocketSphinx Python bindings
RUN pip3 install pocketsphinx
ADD . .
CMD [ "python3", "main.py"]