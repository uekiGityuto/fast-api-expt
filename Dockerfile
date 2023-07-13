FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY requirements.txt /tmp/pip-tmp/
RUN pip install --disable-pip-version-check --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY ./app .

ENV PYTHONPATH=/app
