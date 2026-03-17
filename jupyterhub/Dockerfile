FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

RUN pip install --no-cache-dir \
    jupyterhub==4.0.2 \
    jupyterlab==4.0.9 \
    notebook==7.0.6 \
    ipywidgets \
    jupyterhub-idle-culler

RUN useradd -m -s /bin/bash admin && \
    useradd -m -s /bin/bash user1 && \
    useradd -m -s /bin/bash user2

RUN pip install --no-cache-dir \
    jupyterlab \
    notebook \
    ipykernel

RUN mkdir -p /srv/jupyterhub/data && \
    chmod 755 /srv/jupyterhub

WORKDIR /srv/jupyterhub

EXPOSE 8100 8101

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
