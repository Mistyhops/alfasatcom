FROM python:3.9-alpine
RUN mkdir /app
RUN apk add --no-cache libusb-dev curl
COPY ./src /app/src
COPY test_db.sql /app/test_db.sql
WORKDIR /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ENV DB_HOST="127.0.0.1"
ENV DB_NAME="testdb"
ENV DB_PASSWD=""
ENV DB_USER="postgres"
ENV CORS_ALLOWED_ORIGINS="*"
CMD ["uvicorn", "src.main:app", "--port", "8010", "--host", "0.0.0.0"]
