
FROM jenkins/inbound-agent:jdk21

USER root

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        docker.io \
        curl \
        unzip && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSl \
    "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
    -o /tmp/awscliv2.zip && \
    unzip -q /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm -rf /tmp/aws /tmp/awscliv2.zip

USER jenkins
