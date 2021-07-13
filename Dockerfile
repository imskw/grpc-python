FROM python:3.8.10-buster

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./src /workspace

WORKDIR /workspace

RUN python -m grpc_tools.protoc -I./ --python_out=./ ./protos/book.proto
RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ ./protos/book_interface.proto

CMD ["python", "grpc_app.py"]
