FROM php:8.1.0RC5-apache-buster

RUN apt-get update
RUN apt-get install -y libpq-dev
RUN docker-php-ext-install pdo pdo_pgsql pgsql

COPY config/php.ini /usr/local/etc/php/php.ini