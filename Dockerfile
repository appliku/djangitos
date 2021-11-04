FROM python:3.8.12-bullseye
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0
ENV COLUMNS 80
RUN apt-get update \
 && apt-get install -y --force-yes \
 nano python3-pip gettext chrpath libssl-dev libxft-dev \
 libfreetype6 libfreetype6-dev  libfontconfig1 libfontconfig1-dev\
  && rm -rf /var/lib/apt/lists/* \
ENV NODE_VERSION=16.13.0
ENV NVM_DIR=/root/.nvm
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.37.2/install.sh | bash
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version
WORKDIR /code/
COPY requirements.txt /code/
COPY requirements-dev.txt /code/
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
COPY . /code/
