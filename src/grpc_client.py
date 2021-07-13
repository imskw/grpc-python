import argparse

import grpc

from protos import book_pb2, book_interface_pb2, book_interface_pb2_grpc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--book_id', type=int, required=True)

    args = parser.parse_args()

    book_id = args.book_id
    request_param = book_interface_pb2.GetBookParam(id=book_id)

    # サーバーに接続する
    with grpc.insecure_channel("localhost:8500") as channel:
        stub = book_interface_pb2_grpc.BookManagerStub(channel)
        response = stub.get(request_param)

    print(response)


if __name__ == '__main__':
    main()
