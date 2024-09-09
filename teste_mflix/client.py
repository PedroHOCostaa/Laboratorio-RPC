from __future__ import print_function

import logging

import grpc
import mflix_pb2
import mflix_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Vai tentar mandar a mensagem ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = mflix_pb2_grpc.GreeterStub(channel)
        titulo = input("Escreva o titulo: ")
        ano = int(input("Escreva o ano: "))
        duracao = int(input("Escreva a duração: "))
        filme = mflix_pb2.Filme()
        filme.titulo = titulo
        filme.ano = ano
        filme.duracao = duracao
        confirmacao = stub.CreateFilm(filme)
        print("Titulo do filme criado" + confirmacao.filme.titulo)
        print("Ano do filme criado" + str(confirmacao.filme.ano))
        print("Duração do filme criado" + str(confirmacao.filme.duracao))
        id = input("Escreva o id do filme a ser lido: ")
        pedido = mflix_pb2.Pedido()
        pedido.filme.id = id
        confirmacao = stub.ReadFilm(pedido)
        print("Titulo do filme criado" + confirmacao.filme.titulo)
        print("Ano do filme criado" + str(confirmacao.filme.ano))
        print("Duração do filme criado" + str(confirmacao.filme.duracao))

if __name__ == "__main__":
    logging.basicConfig()
    run()
