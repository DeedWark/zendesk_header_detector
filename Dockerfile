FROM python:3.7-alpine

LABEL maintainer="DeedWark - github.com/DeedWark"

WORKDIR /app

COPY app/ /app

ARG ZENDESK_TOKEN
ENV ZENDESK_TOKEN=${ZENDESK_TOKEN}

RUN pip3 install -r requirements.txt

CMD ["python", "/app/zendesk_header_detecter.py"]
