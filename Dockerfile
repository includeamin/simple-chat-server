FROM includeamin/chichi_websocket_baseimage:v1
EXPOSE 3000
COPY . app
WORKDIR app
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]