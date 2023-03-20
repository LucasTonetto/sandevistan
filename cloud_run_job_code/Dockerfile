# Dockerfile padrão para imagens em python no Cloud Run
# Pode ser alterado se necessário

# base python image
FROM python:3.8-slim-buster

# create a virtual environment
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# RUN source $VIRTUAL_ENV/bin/activate

# copy requirement.txt file 
# COPY requirements.txt requirements.txt

COPY . /var/cloud_runv_service

WORKDIR /var/cloud_runv_service

# install packages listed in copied requirements.txt file
# RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD python3 main.py