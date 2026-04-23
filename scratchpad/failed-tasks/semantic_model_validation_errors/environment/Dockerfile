FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl \
    git \
    nodejs \
    npm \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyyaml

RUN useradd -m -s /bin/bash user
USER user
WORKDIR /home/user

RUN mkdir -p /home/user/myproject
COPY --chown=user:user inconvo.yaml /home/user/myproject/inconvo.yaml

CMD ["/bin/bash"]