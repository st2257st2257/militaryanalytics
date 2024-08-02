FROM python:3.11.1-alpine3.17

RUN apk add g++ postgresql-dev cargo gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev
# RUN apt-get update && apt-get install -y \
#     librdkafka-dev \

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary

# RUN pip upgrade
# RUN pip install librdkafka
# RUN pip install kafka-connect-py
# RUN pip install confluent_kafka
RUN apk update && apk add git
# RUN git clone https://github.com/Microsoft/vcpkg
# RUN cd vcpkg
# RUN ./bootstrap-vcpkg.sh
# RUN vcpkg integrate install
# RUN vcpkg install librdkafka

# install librdkafka
ENV LIBRD_VER=1.3.0
RUN apk add --no-cache --virtual .make-deps bash make wget git gcc g++ && apk add --no-cache musl-dev zlib-dev openssl zstd-dev pkgconfig libc-dev
RUN wget https://github.com/edenhill/librdkafka/archive/v${LIBRD_VER}.tar.gz
RUN tar -xvf v${LIBRD_VER}.tar.gz && cd librdkafka-${LIBRD_VER} && ./configure --prefix /usr && make && make install

# install kafka lib for python
RUN pip install Pyrebase4
## RUN pip install -y python3-dev build-essential librdkafka-dev
## RUN pip install confluent_kafka

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && apk add --no-cache librdkafka-dev
# RUN pip install confluent-kafka
# install kafka-python
RUN pip install kafka-python


COPY . .

EXPOSE 8000
WORKDIR /usr/src/app

#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN python manage.py migrate sessions

#CMD ["python", "manage.py", "makemigrations"]
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "migrate", "sessions"]
#CMD ["exec", "gunicorn", "prod.wsgi:application", "-b", "0.0.0.0:8000", "--reload"]
#CMD ["python", "manage.py", "runsslserver", "--certificate", "rootCA.crt", "--key", "rootCA.key", "0.0.0.0:8000"]
#CMD ["python", "manage.py", "createsuperuser"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["sh", "-c", "echo 'y' | python manage.py makemigrations --merge && python manage.py runserver 0.0.0.0:8000"]
