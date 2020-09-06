FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"


ADD requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app

COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/static

RUN adduser --disabled-password --gecos '' user

RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

USER user

CMD ["entrypoint.sh"]
