FROM python:3.10.4
LABEL authors="chuckz"


RUN apt-get -y install wget \
    && apt-get clean

RUN pip install pandas sqlalchemy psycopg2-binary

WORKDIR /app
COPY ingest_data.py ingest_data.py
ENTRYPOINT ["python", "ingest_data.py"]