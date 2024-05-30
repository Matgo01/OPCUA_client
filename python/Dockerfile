# Usa l'immagine di base Ubuntu
FROM ubuntu:latest

# Aggiorna i repository e installa Python
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Crea una directory di lavoro all'interno del container
WORKDIR /app

COPY Event.py /app
COPY opcua_client.py /app
COPY sql_alchemy_db.py /app
COPY config_pressure.yaml /app
COPY config_temperature.yaml /app


# ambiente virtuale
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Installa le dipendenze Python
RUN pip install aiofiles==23.2.1 \
    && pip install aiosqlite==0.20.0 \
    && pip install archspec \
    && pip install asgiref==3.8.1 \
    && pip install asyncua==1.1.0 \
    && pip install blinker==1.7.0 \
    && pip install boltons \
    && pip install Brotli \
    && pip install certifi \
    && pip install cffi \
    && pip install charset-normalizer \
    && pip install click==8.1.7 \
    && pip install colorama \
    && pip install contourpy==1.2.1 \
    && pip install cryptography \
    && pip install cycler==0.12.1 \
    && pip install distro \
    && pip install Flask==3.0.3 \
    && pip install fonttools==4.51.0 \
    && pip install greenlet==3.0.3 \
    && pip install gunicorn==21.2.0 \
    && pip install idna \
    && pip install itsdangerous==2.1.2 \
    && pip install Jinja2==3.1.3 \
    && pip install jsonpatch \
    && pip install jsonpointer==2.1 \
    && pip install kiwisolver==1.4.5 \
    && pip install MarkupSafe==2.1.5 \
    && pip install matplotlib==3.8.4 \
    && pip install mysql-connector-python==8.3.0 \
    && pip install numpy==1.26.4 \
    && pip install packaging \
    && pip install pillow==10.3.0 \
    && pip install platformdirs \
    && pip install pluggy \
    && pip install pycosat \
    && pip install pycparser \
    && pip install pyOpenSSL==24.1.0 \
    && pip install pyparsing==3.1.2 \
    && pip install PySocks \
    && pip install python-dateutil==2.9.0.post0 \
    && pip install python-snap7==1.3 \
    && pip install pytz==2024.1 \
    && pip install PyYAML \
    && pip install requests \
    && pip install ruamel.yaml \
    && pip install setuptools==68.2.2 \
    && pip install six==1.16.0 \
    && pip install sortedcontainers==2.4.0 \
    && pip install SQLAlchemy==2.0.29 \
    && pip install sqlalchemy_utils \
    && pip install pymysql \
    && pip install tqdm \
    && pip install truststore \
    && pip install typing_extensions==4.11.0 \
    && pip install urllib3 \
    && pip install websockets \
    && pip install Werkzeug==3.0.2 \
    && pip install wheel==0.41.2 \
    && pip install win-inet-pton \
    && pip install zstandard==0.19.0



# Definisci i volumi che si desidera montare
VOLUME /app/data


CMD ["python3", "opcua_client.py"]


