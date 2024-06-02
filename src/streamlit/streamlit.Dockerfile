# FROM alpine:latest
FROM python:slim

ADD src/streamlit /home/shield/src/streamlit

WORKDIR /home/shield

ENV ENVIRONMENT=docker

VOLUME /home/volume/
EXPOSE 8501

RUN apt-get update \
&& apt-get install python3-pip -y

RUN pip3 install -r /home/shield/src/streamlit/streamlit_requirements.txt

# RUN apk update && \
#     apk upgrade && \
#     apk add --no-cache python3 && \
#     apk add --no-cache py3-pip
# 
# RUN pip3 install -r /home/shield/src/streamlit/streamlit_requirements.txt \
#     --break-system-packages

CMD streamlit run src/streamlit/homepage.py --server.port=8501 --server.address=0.0.0.0