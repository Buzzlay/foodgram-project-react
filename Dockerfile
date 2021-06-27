FROM python:3.9.5

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r ./requirements.txt

RUN apt update && apt install wkhtmltopdf -y

COPY . .