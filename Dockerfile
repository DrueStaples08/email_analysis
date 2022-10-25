# Dockerfile for email analysis
FROM python:3.9 as email_run
WORKDIR /app
COPY . /app
RUN pip install -U pip
RUN apt-get update
RUN apt-get install -y gcc libc6-dev make
RUN pip install -U wheel
RUN pip install -U setuptools
RUN pip install -r requirements.txt
RUN mkdir -p /root/.config/matplotlib
RUN echo "backend : Agg" > /root/.config/matplotlib/matplotlibrc
RUN [ "python", "-c", "import nltk; nltk.download('all')" ]
RUN python visualizations.py
RUN echo 'Finished!'