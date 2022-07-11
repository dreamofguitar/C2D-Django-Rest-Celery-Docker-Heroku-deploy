# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8000

ENV DEBIAN_FRONTEND=noninteractive

RUN   apt-get update && apt-get install -y --no-install-recommends && apt-get install -y python3-dev build-essential \
        locales \
        tzdata \
        ca-certificates \
        libpq-dev \
        && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
        && echo 'LANG="en_US.UTF-8"'>/etc/default/locale \
        && dpkg-reconfigure --frontend=noninteractive locales \
        && update-locale LANG=en_US.UTF-8 \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt 

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder:con2drs-back. Please enter the Python path to wsgi file.
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "C2D.wsgi"]

#Prueba ejecucióón con django para medir el timeout que manda con gunicorn
CMD python manage.py runserver 0.0.0.0:8000


