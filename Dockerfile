FROM python:3.9-slim

# Create the user
RUN groupadd --gid 1000 user \
    && useradd --uid 1000 --gid 1000 -m user && \
    mkdir -p /opt/app && \
    chmod 777 /opt/app && \
    mkdir /data && \
    chmod 777 /data

COPY src /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt

USER user

CMD ["python", "app.py"]