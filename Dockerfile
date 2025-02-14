FROM python:3.12-slim

WORKDIR /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev libffi-dev wget tar \
    autoconf automake libtool pkg-config && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O- https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* main.py /app/
COPY ./src /app/src/

RUN poetry install

ENV PATH="/opt/poetry/bin:$PATH"
ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "main.py"]