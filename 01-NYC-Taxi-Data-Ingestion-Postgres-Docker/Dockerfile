FROM python:3.13.1

COPY requirements.txt /app/requirements.txt
COPY data /app/data
RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY pipe.py data_ingestion.py

ENTRYPOINT [ "python" , "data_ingestion.py" ]
