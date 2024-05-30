FROM mysql:latest

ENV MYSQL_DATABASE=my_sensors_database
ENV MYSQL_USER=docker_user
ENV MYSQL_PASSWORD=Matteo2004x!
ENV MYSQL_ROOT_PASSWORD=Matteo2004x!

WORKDIR /app
# Copia il file di configurazione YAML nella directory corretta

COPY create_database.py /app

# Definisci i volumi che si desidera montare
VOLUME /app/data

# Esponi la porta 3306 per consentire la connessione al database MySQL
EXPOSE 3306

# Comando di avvio
CMD ["mysqld","create_database.py"]