FROM python:latest

RUN pip install pipenv

RUN apt update && \
    curl -s https://deb.nodesource.com/setup_16.x | bash && \
    apt install nodejs -y

RUN apt-get update && apt-get install -y gnupg software-properties-common && \
    wget -O- https://apt.releases.hashicorp.com/gpg | \
        gpg --dearmor && \
    wget https://releases.hashicorp.com/terraform/1.0.7/terraform_1.0.7_linux_amd64.zip && \
    unzip terraform_1.0.7_linux_amd64.zip && \
    rm terraform_1.0.7_linux_amd64.zip && \
    mv terraform /usr/local/bin/

RUN npm install --global cdktf-cli@latest

COPY . /var/sandevistan

WORKDIR /var/sandevistan/src

RUN pipenv install cdktf-cdktf-provider-aws