FROM alpine:latest

ADD /src/monitoring/monitoring.py /home/shield/src/monitoring/
ADD /src/monitoring/monitor_api.py /home/shield/src/monitoring/
ADD /src/monitoring/monitoring_requirements.txt /home/shield/src/monitoring/

WORKDIR /home/shield/

ENV ENVIRONMENT=docker

VOLUME /home/volume/
EXPOSE 8008

RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 && \
    apk add --no-cache py3-pip

RUN pip3 install -r /home/shield/src/monitoring/monitoring_requirements.txt \
    --break-system-packages

# CMD tail -f /dev/null 
# CMD python3 src/monitoring/monitoring.py \
CMD uvicorn --app-dir src/monitoring monitor_api:api --reload --host=0.0.0.0 --port=8008\