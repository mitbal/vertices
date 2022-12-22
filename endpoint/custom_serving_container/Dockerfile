FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY model.txt .
COPY app.py .

ENTRYPOINT ["python", "app.py"]
