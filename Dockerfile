FROM python:3-slim
WORKDIR /app

ADD . .

RUN python3 -m pip install -r requirements.txt

CMD ["python", "app.py"]