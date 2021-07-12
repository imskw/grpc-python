import csv

import grpc
from concurrent.futures import ThreadPoolExecutor
from protos import book_pb2, book_interface_pb2_grpc

books = {}
with open('data/book_sample.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for line in reader:
        books.update({line[0]: {key: value for key, value in zip(header, line)}})


class BookManager(book_interface_pb2_grpc.BookManager):
    def get(self, request, context):
        book_id = request.id
        book = books[str(book_id)]

        response = book_pb2.Book(
            id=int(book["id"]),
            title=book["title"],
            book_type=book_pb2.Book.BookType.Value(book["book_type"])
        )
        print(book["book_type"])
        print('book_type', book_pb2.Book.BookType.Value(book["book_type"]))
        return response


def main():
    # Serverオブジェクトを作成
    server = grpc.server(ThreadPoolExecutor(max_workers=2))

    # Servicerに登録
    book_interface_pb2_grpc.add_BookManagerServicer_to_server(BookManager(), server)

    # PORTの設定
    server.add_insecure_port('[::]:8500')

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
