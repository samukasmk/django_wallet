FROM python:3.11.3-slim
ARG INSTALL_LIBS=production

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install ubuntu packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y make gcc python-dev libpq-dev && \
    apt clean && \
    apt autoclean && \
    rm -rf /var/lib/apt/lists/*

# Copy files to new image
WORKDIR /opt/django_wallet
COPY . /opt/django_wallet

# Fake sudo command in container
RUN echo '$*' > /bin/sudo
RUN chmod 555 /bin/sudo

# Install library dependencies
RUN echo Building mode: install-$INSTALL_LIBS
RUN make install-$INSTALL_LIBS

# Collect static files on first build
RUN make collect-static-files

# Clean unused files
RUN make clean