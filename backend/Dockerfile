# FROM python:3.10.6-alpine3.16
FROM python:3.10.8-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update -y
RUN apt-get install -y mediainfo
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./app /app
COPY ./static /static
CMD ["uvicorn", "--proxy-headers", "--forwarded-allow-ips='*'", "--root-path", "/api", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]