# Проект: Деплой на сервер с использованием Docker Compose

## Оглавление
1. [Подготовка проекта](#1)
2. [Редактирование конфигурации Nginx](#2)
3. [Создание самоподписанных SSL сертификатов](#3)
4. [Настройка базы данных PostgreSQL](#4)
5. [Подключение к базе данных извне](#5)
6. [Пошаговая инструкция по деплою](#6)

<a name="1"></a>
## 1. Подготовка проекта
1. Сначала сделайте форк проекта на GitHub:
    - Перейдите на страницу проекта на GitHub: `https://github.com/yourusername/yourproject`.
    - Нажмите кнопку "Fork" в верхнем правом углу, чтобы создать копию проекта в своем аккаунте.

2. Склонируйте форкнутый проект:
    ```sh
    git clone https://github.com/yourusername/yourforkedproject.git
    ```

3. Перейдите в директорию проекта:
    ```sh
    cd yourforkedproject
    ```

<a name="2"></a>
## 2. Редактирование конфигурации Nginx
Для того чтобы ваш проект работал с вашим доменом или IP-адресом, вам необходимо отредактировать файл конфигурации Nginx `nginx.conf`.

**Шаблон конфигурационного файла nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name yourdomain.com yourip;

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name yourdomain.com yourip;

        ssl_certificate /etc/nginx/certs/your_certificate.crt;
        ssl_certificate_key /etc/nginx/certs/your_key.key;

        error_log /var/log/nginx/error.log debug;
        access_log /var/log/nginx/access.log;

        location / {
            proxy_pass http://fastapi:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

**Что нужно изменить:**
- `server_name yourdomain.com yourip` — замените на ваш домен и/или IP-адрес.
- `ssl_certificate /etc/nginx/certs/your_certificate.crt` — путь к вашему SSL сертификату.
- `ssl_certificate_key /etc/nginx/certs/your_key.key` — путь к вашему приватному ключу.

<a name="3"></a>
## 3. Создание самоподписанных SSL сертификатов
Для создания самоподписанных SSL сертификатов выполните следующие команды:

1. Перейдите в директорию для сертификатов:
    ```sh
    cd nginx/certs
    ```

2. Создайте самоподписанный сертификат:
    ```sh
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout meteostation.key -out meteostation.crt
    ```

3. Введите информацию, запрашиваемую OpenSSL (необходимо заполнить поля: Country, State, City, Organization, Common Name).

4. Ваши сертификаты будут находиться в директории `nginx/certs`:
    - `meteostation.crt` — сертификат.
    - `meteostation.key` — приватный ключ.

<a name="4"></a>
## 4. Настройка базы данных PostgreSQL
В конфигурационном файле `docker-compose.yml` у вас уже есть настройки для базы данных PostgreSQL:

```yaml
services:
  db:
    image: postgres:16.3
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=irtsu
      - POSTGRES_PASSWORD=irtsu_meteostation
      - POSTGRES_DB=project
    ports:
      - "5432:5432"
    restart: unless-stopped
```

<a name="5"></a>
## 5. Подключение к базе данных извне
Для подключения к базе данных PostgreSQL извне используйте следующие параметры:

- **Host:** IP-адрес вашего сервера или `localhost`, если вы подключаетесь с того же сервера.
- **Port:** 5432
- **Database Name:** `project`
- **Username:** `irtsu`
- **Password:** `irtsu_meteostation`

**Пример команды для подключения через psql:**
```sh
psql -h your_server_ip -p 5432 -U irtsu -d project
```

<a name="6"></a>
## 6. Пошаговая инструкция по деплою
1. Склонируйте проект и перейдите в его директорию:
    ```sh
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Отредактируйте файл конфигурации Nginx `nginx.conf`:
    - Замените `server_name` на ваш домен и/или IP-адрес.
    - Убедитесь, что пути к SSL сертификатам корректны.

3. Создайте самоподписанные SSL сертификаты:
    ```sh
    cd nginx/certs
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout meteostation.key -out meteostation.crt
    ```

4. Запустите Docker Compose для развертывания проекта:
    ```sh
    docker-compose up -d
    ```

5. Проверьте работу проекта, открыв ваш домен или IP-адрес в браузере.

Эти шаги помогут вам развернуть проект на сервере с использованием Docker Compose и настроить его для работы с вашим доменом и самоподписанными SSL сертификатами.