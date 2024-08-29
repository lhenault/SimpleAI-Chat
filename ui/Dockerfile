FROM python:3.11

ENV PYTHONBUFFERED 1

ADD . .
RUN pip install -r requirements.txt

# CMD ["python", "./main.py"]
CMD ["streamlit", "run", "./main.py", "--server.port=8888", "--server.address=0.0.0.0", "--browser.gatherUsageStats=0"]