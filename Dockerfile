FROM python:3.8-alpine
WORKDIR /app
COPY . .
RUN apk add build-base
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3", "main.py"]