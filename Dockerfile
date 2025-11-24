FROM postgres:16

ENV POSTGRES_PASSWORD=yourpassword
ENV POSTGRES_DB=mtgdb
ENV POSTGRES_USER=postgres

# Install Python for converting JSON and importing
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip psycopg2-binary

ENV PATH="/opt/venv/bin:$PATH"
# Create folder for initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy your JSON file into the container
COPY cards.json /docker-entrypoint-initdb.d/cards.json

# Copy the Python import script and SQL schema initializer
COPY init/load_cards.sh /docker-entrypoint-initdb.d/load_cards.sh
COPY init/load_cards.py /docker-entrypoint-initdb.d/load_cards.py

COPY init/init.sql /docker-entrypoint-initdb.d/init.sql

# Ensure scripts are executable
# RUN chmod +x /docker-entrypoint-initdb.d/load_cards.py
RUN chmod +x /docker-entrypoint-initdb.d/load_cards.sh

# COPY init/transform.sql /docker-entrypoint-initdb.d/transform.sql

# Ensure scripts are executable
