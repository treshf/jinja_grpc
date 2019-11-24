import time
from concurrent import futures
import grpc

import test_pb2
import test_pb2_grpc
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader('foopkg/templates'))


class TestServicer(test_pb2_grpc.DataServicer):
    def gen(self, request, context):
        print(request.param, request.adr)
        response = test_pb2.html()
        if os.path.exists(request.adr):
            try:
                template = env.get_template(request.adr)
                response.data = template.render()
            except:
                response.res = test_pb2.html.NOTDATA
            else:
                response.res = test_pb2.html.OK
        else:
            response.res = test_pb2.html.NOTADR
        context.set_code(grpc.StatusCode.OK)
        return response


def serve(adr='[::]:6066'):
    # создаем сервер
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    # прикреплям хандлеры
    test_pb2_grpc.add_DataServicer_to_server(TestServicer(), server)
    # запускаемся на порту 6066
    print('Starting server on port 6066.')
    server.add_insecure_port(adr)
    server.start()
    # работаем час или до прерывания с клавиатуры

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
