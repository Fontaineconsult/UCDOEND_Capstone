FROM python:3.7.3-stretch

## Step 1:
WORKDIR /app

## Step 2:
COPY ./accessiblebookchecker /accessiblebookchecker
COPY . requirements.txt ./

## Step 3:
# hadolint ignore=DL3013
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt


## Step 4:
EXPOSE 5000

## Step 5:


