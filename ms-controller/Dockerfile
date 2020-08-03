FROM python:3.6-slim-buster

COPY . /app
WORKDIR /app
ENV LANG C.UTF-8
ENV PYTHON_VERSION 3.8
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "worker.py"]