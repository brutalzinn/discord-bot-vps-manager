FROM php:7.4-fpm

#https://www.ti-enxame.com/pt/docker/executando-composer-instala-dentro-de-um-dockerfile/833985041/
RUN apt-get update && apt-get install -y libpq-dev
RUN docker-php-ext-install pdo pdo_pgsql pgsql
RUN ln -s /usr/local/etc/php/php.ini-production /usr/local/etc/php/php.ini
RUN sed -i -e 's/;extension=pgsql/extension=pgsql/' /usr/local/etc/php/php.ini
RUN sed -i -e 's/;extension=pdo_pgsql/extension=pdo_pgsql/' /usr/local/etc/php/php.ini
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer


RUN apt-get install -y \
        libzip-dev \
        zip 

RUN docker-php-ext-install \
    zip \
    iconv \
    fileinfo

WORKDIR /var/www/html


# COPY tinyfilemanager.php index.php
# COPY config-sample.php config.php
# RUN sed -i "s/\$root_path =.*;/\$root_path = \$_SERVER['DOCUMENT_ROOT'].'\/data';/g" config.php && \
#     sed -i "s/\$root_url = '';/\$root_url = 'data\/';/g" config.php

CMD ["sh", "-c", "composer require firebase/php-jwt && php -S 0.0.0.0:80"]