FROM alpine:latest

ADD /src/data/make_dataset.py /home/shield/src/data/
ADD /src/data/make_dataset_requirements.txt /home/shield/src/data/

# Unused ADD: 
# ADD /src/data/requirements_make_dataset.txt /home/shield/data/preprocessed

WORKDIR /home/shield/

EXPOSE 8002

RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 && \
    apk add --no-cache py3-pip

RUN pip3 install -r /home/shield/src/data/make_dataset_requirements.txt \
    --break-system-packages

CMD ["/bin/sh", "-c", " \
# Import raw data (previously created in step 1) from volume to container:
cp -r ../volume/data data ; \
# Run preprocessing:
python3 src/data/make_dataset.py ;\
# Copy processed files to volume for persistency:
cp -r data/preprocessed/ ../volume/data\
"]
