FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN python3 -m pip install -r requirements.txt
ADD . /app

CMD ["python", "app.py"]