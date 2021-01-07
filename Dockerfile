FROM wesbarnett/apache-flask:bionic-x86_64


## Step 1:
WORKDIR /app

## Step 2:
COPY ./accessiblebookchecker /accessiblebookchecker
COPY . requirements.txt ./

## Step 3:
# hadolint ignore=DL3013
RUN apt update &&\
    apt-get install libpq-dev python-dev
    pip install psycopg2-binary
    apt install apache2 -y &&\
    apt-get install libapache2-mod-wsgi-py3 python-dev -y

RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt


RUN apache2ctl startInvoking 'systemctl start apache2'.

## Step 4:
EXPOSE 80

## Step 5:


