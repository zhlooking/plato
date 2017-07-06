FROM python:3.6.1

# set working directory
RUN mkdir -p /usr/src/plato
WORKDIR /usr/src/plato

# add requirements (to leverage docker cache)
ADD ./requirements.txt /usr/src/plato/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
ADD . /usr/src/plato

# run server
CMD python manage.py runserver -h 0.0.0.0
