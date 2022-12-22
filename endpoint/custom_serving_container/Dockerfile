FROM python:3.9-slim

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY model.txt .
COPY app.py .

ENTRYPOINT ["python", "app.py"]
