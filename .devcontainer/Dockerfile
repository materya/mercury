FROM mercury_dev

USER root

ARG DEV_PACKAGES="\
  git \
"

RUN apt-get update \
  && apt-get install -y --no-install-recommends $DEV_PACKAGES \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
