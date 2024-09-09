
from concurrent import futures
import logging

import grpc
import mflix_pb2
import mflix_pb2_grpc


class Carteiro(mflix_pb2_grpc.GreeterServicer):
    def CreateFilm(self, request, context):
        print("Metodo CreateFilm ...")
        print("Titulo: ", request.filme.titulo)
        print("Ano: ", request.filme.ano)
        print("Duração: ", request.filme.duracao)
        confirmacao = mflix_pb2.Confirmacao()
        confirmacao.filme = request.filme
        confirmacao.resultado = request.op
        return confirmacao
    def ReadFilm(self, request, context):
        print("Metodo ReadFilm ...")
        return mflix_pb2.HelloReply(message="Hello again, %s!" % request.name)

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mflix_pb2_grpc.add_CarteiroServicer_to_server(Carteiro(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
