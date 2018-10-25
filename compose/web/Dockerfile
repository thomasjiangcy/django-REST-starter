FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN apk update && \
    apk add git && \
    # psycopg2 dependencies
    apk add --virtual .build-deps build-base libc-dev gcc python3-dev libxslt-dev musl-dev && \
    apk add postgresql-dev && \
    # Pillow dependencies
    apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev && \
    # CFFI dependencies
    apk add libffi-dev py-cffi

RUN addgroup -S django && \
    adduser -S -G django django

RUN mkdir -p /var/log/celery /var/run/celery

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip3 install --no-cache-dir --disable-pip-version-check -r /requirements/prod.txt && \
    rm -rf /requirements && \
    apk del .build-deps

COPY ./compose/web/scripts/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/web/scripts/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/web/scripts/start-celery /start-celery
RUN sed -i 's/\r//' /start-celery
RUN chmod +x /start-celery
RUN chown django /start-celery

COPY . /app

RUN chown -R django /app

WORKDIR /app

ENTRYPOINT [ "/entrypoint" ]
