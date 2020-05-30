FROM python:3.7.3-slim
COPY ./ /app
WORKDIR /app
RUN pip install nativeAPI_wheel/irisnative-1.0.0-cp34-abi3-linux_x86_64.whl
RUN pip install pymongo
RUN pip install flask
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]