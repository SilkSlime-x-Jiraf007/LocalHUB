FROM python:3.10.6-alpine3.16
ENV PYTHONDONTWRITEBYTECODE 1
RUN apk add build-base
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./app /app
COPY ./static /static
CMD ["uvicorn", "--proxy-headers", "--forwarded-allow-ips='*'", "--root-path", "/api", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]