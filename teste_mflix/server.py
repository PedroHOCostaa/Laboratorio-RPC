
from concurrent import futures
import logging

import grpc
import mflix_pb2
import mflix_pb2_grpc


class Greeter(mflix_pb2_grpc.GreeterServicer):
    def CreateFilm(self, request, context):
        print("Metodo CreateFilm ...")
        print("Titulo: ", request.titulo)
        print("Ano: ", request.ano)
        print("Duração: ", request.duracao)
        filme = mflix_pb2.Filme()
        filme = request
        return filme
    
    def ReadFilm(self, request, context):
        print("Metodo ReadFilm ...")
        filme = mflix_pb2.Filme()
        filme.titulo = "Filme " + request.id
        filme.ano = 2000 + int(request.id)
        filme.duracao = 120 + int(request.id) * 10
        return filme

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mflix_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
