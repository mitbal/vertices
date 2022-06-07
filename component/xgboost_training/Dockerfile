FROM python:3.9

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "xgboost_training.py"]
