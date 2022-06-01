FROM python:3.7.3-slim
COPY ./ /app
WORKDIR /app
RUN pip install nativeAPI_wheel/intersystems_irispython-3.2.0-py3-none-any.whl
RUN pip install pymongo[srv]
RUN pip install flask
RUN pip install flask-cors
RUN pip install flask-restful
RUN pip install dnspython
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]