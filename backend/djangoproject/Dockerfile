# FROM python:3.11.1-alpine3.17
# FROM python:3.11.1-bullseye
# FROM python:3.11.1-buster
# FROM python:3.11.1-slim
FROM python:3.11.1-bullseye

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary


ENV LIBRD_VER=1.3.0

RUN pip install Pyrebase4
RUN pip install confluent_kafka

RUN pip install kafka-python


COPY . .

EXPOSE 8000
WORKDIR /usr/src/app

#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "migrate", "sessions"]
#CMD ["exec", "gunicorn", "prod.wsgi:application", "-b", "0.0.0.0:8000", "--reload"]
#CMD ["python", "manage.py", "runsslserver", "--certificate", "rootCA.crt", "--key", "rootCA.key", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "createsuperuser"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["sh", "-c", "echo 'y' | python manage.py makemigrations --merge && python manage.py runserver 0.0.0.0:8000"]
