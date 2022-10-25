# workdir 
# pip insatl requiremtns
# cd into workdir 
# run visulations command


# Dockerfile for email analysis

FROM python:3.9 as email_run
WORKDIR /app
COPY . /app
# RUN pip install --upgrade pip
RUN pip install -U pip
RUN apt-get update
RUN apt-get install -y gcc libc6-dev make
# RUN apt-get -y install libc-dev
RUN pip install -U wheel
RUN pip install -U setuptools
# RUN apt-get -y install build-essential
# RUN pip install -U pip
RUN pip install -r requirements.txt
# RUN python -m nltk.downloader punkt stopwords wordnet
# RUN pip install nltk
# RUN python -m nltk.downloader punkt
# RUN python -m nltk.downloader stopwords
# RUN python -m nltk.downloader wordnet
# RUN python -m nltk.downloader omw-1.4
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# CMD python
# CMD import nltk
# CMD nltk.download()

RUN [ "python", "-c", "import nltk; nltk.download('all')" ]

# ENTRYPOINT [ "python" ]
# CMD [ "visualizations.py" ]
RUN python visualizations.py
RUN echo 'Finished!'

# First, update your pip installer as shown below.
# 1
# python - m pip install – upgrade pip
# Then upgrade your wheel by using:
# 1
# pip install - upgrade wheel
# Then finally upgrade the setuptools.
# 1
# pip install - upgrade setuptools



# # dev
# FROM python:3 as devrun
# WORKDIR /app
# COPY . /app
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# WORKDIR /app/MLAPI
# EXPOSE 5000
# # EXPOSE 3306
# ENV FLASK_APP=mlapi.py
# ENV FLASK_ENV=development
# ENV FLASK_RUN_PORT=5000
# # ENV FLASK_RUN_PORT=3306
# ENV FLASK_RUN_HOST=0.0.0.0
# # ENV FLASK_RUN_HOST=35.192.180.222
# ENTRYPOINT [ "python" ]
# CMD [ "mlapi.py" ]

# `docker build --target devrun -t flask-app-dev:latest .`


# `docker run -d -p 5000:5000 flask-app-dev`