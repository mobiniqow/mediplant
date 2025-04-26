FROM python:3.12-slim

# اضافه کردن مخزن Ubuntugis و نصب GDAL نسخه جدید
RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
    && apt-get update && apt-get install -y \
    gdal-bin=3.10.* \
    libgdal-dev=3.10.* \
    python3-gdal=3.10.* \
    && rm -rf /var/lib/apt/lists/*

# بررسی نسخه GDAL
RUN gdal-config --version

WORKDIR /app

COPY ./req.txt /app/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r req.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--env", "DJANGO_SETTINGS_MODULE=mediplant.settings.prod", "--bind", "0.0.0.0:8000", "--workers", "3"]
