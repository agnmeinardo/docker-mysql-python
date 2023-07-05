FROM python:latest

WORKDIR /src/python
COPY requirements.txt /src/python/requirements.txt
RUN pip install -r requirements.txt
COPY /python /src/python

#CMD ["python","./execution.py"]
