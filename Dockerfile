FROM ghcr.io/materya/datascience:3.8-buster-slim

WORKDIR /workspace

COPY . .

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends make git \
  && make install-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHON_MODULES="\
  ipykernel \
"

RUN pip install --upgrade pip \
  && pip install --no-cache-dir $PYTHON_MODULES

USER cloud
