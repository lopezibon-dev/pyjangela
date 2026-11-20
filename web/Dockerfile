# web edukiontzia: Apache + mod_wsgi + Django
# Debian trixie: Apache eta mod_wsgi sistemakoak (ez da mod_wsgi konpilatzen)
# eta Python 3.13 (Django 6-k Python 3.12+ behar du)
FROM debian:trixie-slim

# Apache, mod_wsgi, Python eta mysqlclient konpilatzeko behar dena
RUN apt-get update && apt-get install -y --no-install-recommends \
        apache2 libapache2-mod-wsgi-py3 \
        python3 python3-venv python3-dev \
        build-essential pkg-config default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Ingurune birtuala Debianen Python-arekin (mod_wsgi-k python-home bezala erabiltzen du)
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodea kopiatu eta fitxategi estatikoak bildu (STATIC_ROOT); DBrik ez da behar
COPY . .
RUN SECRET_KEY=build python manage.py collectstatic --noinput

# Apache: gure gunea bakarrik
COPY docker/apache.conf /etc/apache2/sites-available/jangela.conf
RUN a2dissite 000-default && a2ensite jangela

EXPOSE 80
CMD ["sh", "docker/entrypoint.sh"]
