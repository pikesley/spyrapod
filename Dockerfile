FROM python:3.9

ENV PROJECT=spyrapod
ENV APP_PATH=/opt/${PROJECT}

WORKDIR ${APP_PATH}

RUN apt-get update && apt-get install -y \
                                        nodejs \
                                        npm

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN npm install

COPY docker-config/bashrc /root/.bashrc
COPY ./ ${APP_PATH}
