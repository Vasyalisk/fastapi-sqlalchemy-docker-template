FROM python:3.9
LABEL MAINTAINER="Pixelfield, s.r.o"

ENV PYTHONUNBUFFERED 1
RUN apt-get clean && apt-get update
RUN apt-get update
RUN apt-get install -y netcat
RUN pip install --upgrade pip

WORKDIR /backend
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./backend /backend
ENV PYTHONPATH=/backend

ENTRYPOINT ["/backend/scripts/entrypoint.sh"]