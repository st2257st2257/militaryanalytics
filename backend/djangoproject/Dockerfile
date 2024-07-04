FROM python:3.11.1-alpine3.17

RUN apk add g++ postgresql-dev cargo gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
WORKDIR /usr/src/app

#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
#CMD ["exec", "gunicorn", "prod.wsgi:application", "-b", "0.0.0.0:8000", "--reload"]
#CMD ["python", "manage.py", "runsslserver", "--certificate", "rootCA.crt", "--key", "rootCA.key", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["sh", "-c", "echo 'y' | python manage.py makemigrations --merge && python manage.py runserver 0.0.0.0:8000"]
