FROM python:3.10
ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/wd
ARG USER=user
ARG UID=1000

WORKDIR ${WORKDIR}

RUN useradd --system ${USER} --uid=${UID} && \
    chown --recursive ${USER} ${WORKDIR}

RUN apt update && apt upgrade -y

COPY --chown=${USER} requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

COPY --chown=${USER} ./main.py main.py
COPY --chown=${USER} ./app app
COPY --chown=${USER} ./tools tools
COPY --chown=${USER} ./core core
COPY --chown=${USER} ./Makefile Makefile

USER ${USER}

VOLUME ${WORKDIR}/result