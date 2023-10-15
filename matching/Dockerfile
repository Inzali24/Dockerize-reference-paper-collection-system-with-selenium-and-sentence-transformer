# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y \
curl
RUN  apt-get update \
  && apt-get install -y wget \
  && apt-get install -y unzip \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get update && apt-get install -y gnupg2\
  && apt-get update && apt-get install -y curl unzip jq

#old ChromeDriver
# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     curl -sS -o /tmp/chromedriver_linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.92/linux64/chromedriver-linux64.zip && \
#     unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     rm /tmp/chromedriver_linux64.zip && \
#     chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
#     ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver
ARG CHROMEDRIVER_VERSION='117'

# Install Chrome WebDriver
RUN CHROMEDRIVER_URL=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json | \
  jq -r --arg version "$CHROMEDRIVER_VERSION" '[.versions[] | select(.version | startswith($version + "."))] | last | .downloads.chromedriver[] | select(.platform == "linux64").url') && \
  mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
  curl -sS -o /tmp/chromedriver_linux64.zip "$CHROMEDRIVER_URL" && \
  unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
  rm /tmp/chromedriver_linux64.zip && \
  chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver-linux64/chromedriver && \
  ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver


# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /matching
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /matching/

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]