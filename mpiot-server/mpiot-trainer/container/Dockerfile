FROM        python:3.7

ENV         MESSENGER_HOST localhost

ENV         MESSENGER_PORT 6379

ENV         PATH="/usr/bin/cmake/bin:${PATH}"

COPY        dependencies.txt /

COPY        requirements.txt /

RUN         apt-get -y update

RUN         apt-get -y upgrade

RUN         xargs -a dependencies.txt apt-get -f install -y
      
RUN         pip install --upgrade pip 

RUN         pip install -r requirements.txt

RUN         apt-get install -y 

RUN         xargs -a dependencies.txt apt-get -f install -y --fix-missing

COPY        entrypoint.sh /

ENTRYPOINT [ "bash", "./entrypoint.sh" ]