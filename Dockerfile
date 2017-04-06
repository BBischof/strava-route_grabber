FROM python:2.7

RUN mkdir /usr/src/app

COPY pip_requirements /usr/src/app

WORKDIR /usr/src/app

RUN cd /usr/src/app && \
  pip install -r /usr/src/app/pip_requirements

CMD ["python", "route_grabber.py"]
