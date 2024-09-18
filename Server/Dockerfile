FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt-get install -y python3.10
RUN apt-get install -y python3.10-venv
RUN apt-get install -y python3.10-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y postgresql
RUN apt-get install -y postgresql-client
RUN apt-get install -y libpq-dev

RUN mkdir app

WORKDIR /app
COPY . /app

RUN ls -al

RUN pip3 install -r ./requirements.txt

CMD ["python3", "./run.py"]
