FROM mcr.microsoft.com/devcontainers/python:0-3.11

ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=DL3008
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
   && echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list \
   && apt-get update && export DEBIAN_FRONTEND=noninteractive \
   && apt-get -y install --no-install-recommends postgresql-client-15 \
   && rm -rf /var/lib/apt/lists/*
