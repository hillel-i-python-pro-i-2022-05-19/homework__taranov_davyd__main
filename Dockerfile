FROM python:3.10

ARG WORKDIR=/wd

RUN apt update && apt upgrade -y

WORKDIR ${WORKDIR}

COPY requirements.txt requirements.txt

RUN pip install --requirement requirements.txt

COPY ./main.py main.py
COPY ./app app
COPY ./tools tools
COPY ./results results
COPY ./core core
COPY ./.run .run

ENTRYPOINT ["python", "main.py"]