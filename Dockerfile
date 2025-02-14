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

# Download and install `ta-lib`
RUN wget https://github.com/ta-lib/ta-lib/archive/refs/tags/v0.6.1.tar.gz -O ta-lib.tar.gz && \
    tar -xzf ta-lib.tar.gz && \
    cd ta-lib-0.6.1  && \
    chmod +x autogen.sh && ./autogen.sh && \
    ./configure --prefix=/usr --build=aarch64-unknown-linux-gnu && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib-0.6.1 ta-lib.tar.gz

COPY ./pyproject.toml ./poetry.lock* ./src main.py /app/

RUN poetry install

ENV PATH="/opt/poetry/bin:$PATH"
ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "main.py"]