FROM python:3.7.3-slim
COPY ./ /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --upgrade pip
RUN pip install nativeAPI_wheel/intersystems_irispython-3.2.0-py3-none-any.whl
RUN pip install pymongo[srv]
RUN pip install flask
RUN pip install flask-cors
RUN pip install flask-restful
RUN pip install dnspython
RUN pip install psycopg2-binary==2.9.4
RUN pip install flask-sqlalchemy
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]