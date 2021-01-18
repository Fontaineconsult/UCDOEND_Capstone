FROM python:3.7


## Step 1:
WORKDIR /var/www/capstone/site

## Step 2:
COPY ./accessiblebookchecker /accessiblebookchecker
COPY . requirements.txt ./


## Step 3:
# hadolint ignore=DL3013
RUN apt update &&\
    apt-get install libpq-dev python-dev -y &&\
    apt-get install apache2 -y &&\
    apt-get install nano &&\
    apt-get install libapache2-mod-wsgi-py3 python-dev -y


RUN python -m pip install --upgrade pip

RUN pip3 install psycopg2-binary

RUN pip3 install --trusted-host pypi.python.org -r  requirements.txt

COPY  capstone.conf /etc/apache2/sites-available
COPY  capstone.wsgi /var/www/capstone


RUN a2ensite capstone.conf
RUN a2dissite 000-default.conf

RUN echo "y" | pip uninstall toastedmarshmallow==2.15.2.post1
RUN pip install toastedmarshmallow==2.15.2.post1


## Step 4:
EXPOSE 80

## Step 5:


