FROM python:3.11

WORKDIR /expt
ENV TZ=Asia/Tokyo

COPY requirements.txt /tmp/pip-tmp/
RUN pip install --disable-pip-version-check --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "app/logging_config.json", "--no-access-log", "--no-use-colors"]
