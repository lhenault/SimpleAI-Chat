FROM python:3.11

ENV PYTHONBUFFERED 1

ADD . .
RUN pip install -r requirements.txt

CMD ["python", "./main.py"]