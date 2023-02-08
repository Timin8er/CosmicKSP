FROM python:3.11.1

WORKDIR /usr/src/app

COPY ./setup.py .
COPY ./README.md .

COPY CosmicKSP/ ./CosmicKSP/
COPY CosmicRelay/ ./CosmicRelay/

RUN pip install .