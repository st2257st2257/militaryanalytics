FROM python:3.11.1-slim

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8085
WORKDIR /usr/src/app

CMD ["python", "main.py"]
