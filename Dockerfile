FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python-dev \
    python-setuptools \
    python-pip \
    rpi.gpio

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY fan_control.py /app

CMD ["python", "fan_control.py"]
