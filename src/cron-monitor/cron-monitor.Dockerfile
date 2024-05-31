FROM alpine:latest

ADD /src/cron-monitor/cron-monitor.py /home/shield/src/cron-monitor/
ADD /src/cron-monitor/cronfile /etc/cron.d/cronfile
ADD /src/cron-monitor/cron_logs.txt /home/shield/logs/

WORKDIR /home/shield/

ENV ENVIRONMENT=docker

VOLUME /home/volume/
EXPOSE 8009

RUN apk update \
&& apk add python3 \
&& apk add py3-requests \
&&  apk add --no-cache dcron

RUN chmod 0644 /etc/cron.d/cronfile
RUN chmod +x /home/shield/src/cron-monitor/cron-monitor.py
RUN crontab /etc/cron.d/cronfile 

CMD ["crond", "-f"]