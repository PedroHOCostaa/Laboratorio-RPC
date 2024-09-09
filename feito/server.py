from concurrent import futures
import logging

import grpc
import mflix_pb2
import mflix_pb2_grpc

class BancoDeDados:
    def create(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True, filme
        else:
            return False

    def read(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False

    def update(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False

    def delete(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False

    def read_by_actors(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False

    def read_by_genre(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False


banco_de_dados = BancoDeDados()

class Mflix(mflix_pb2_grpc.MflixServicer):
    def CriarFilme(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()
        if not request.filme.titulo:
            confirmacao.erro = 2  # Campo Título vazio
            confirmacao.resultado = 0
        elif not request.filme.diretores:
            confirmacao.erro = 3  # Campo Diretor vazio
            confirmacao.resultado = 0
        elif not request.filme.ano:
            confirmacao.erro = 4  # Campo Ano vazio
            confirmacao.resultado = 0
        elif not request.filme.generos:
            confirmacao.erro = 5  # Campo Gêneros vazio
            confirmacao.resultado = 0
        elif not request.filme.atores:
            confirmacao.erro = 6  # Campo Atores vazio
            confirmacao.resultado = 0
        elif not request.filme.duracao:
            confirmacao.erro = 7  # Campo Duração vazio
            confirmacao.resultado = 0
        else:
            resultado = banco_de_dados.create(request.filme)
            if resultado[0]:  # Se a criação foi bem-sucedida
                confirmacao.resultado = 1
                confirmacao.filme.id = str(resultado[1]['id'])
                confirmacao.filme.titulo = resultado[1]['titulo']
                confirmacao.filme.diretores.extend(resultado[1]['diretores'])
                confirmacao.filme.ano = resultado[1]['ano']
                confirmacao.filme.atores.extend(resultado[1]['atores'])
                confirmacao.filme.generos.extend(resultado[1]['generos'])
                confirmacao.filme.duracao = resultado[1]['duracao']
            else:
                confirmacao.resultado = 0
                confirmacao.erro = 8  # Erro ao criar o filme

        return confirmacao
    

    def ReadFilme(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()
        if not request.filme.id:
            confirmacao.erro = 1  # Campo ID vazio
            confirmacao.resultado = 0
        else:
            filme_lido = banco_de_dados.read(request.filme)
            if filme_lido is None:
                confirmacao.resultado = 0
                confirmacao.erro = 9  # Erro ao ler o filme 
            else:   
                confirmacao.filme.CopyFrom(filme_lido)
                confirmacao.resultado = 2

        return confirmacao
    

    def UpdateFilme(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()
        if not request.filme.id:
            confirmacao.erro = 1  # Campo ID vazio
            confirmacao.resultado = 0
        elif not request.filme.titulo:
            confirmacao.erro = 2  # Campo Título vazio
            confirmacao.resultado = 0
        elif not request.filme.diretores:
            confirmacao.erro = 3  # Campo Diretor vazio
            confirmacao.resultado = 0
        elif not request.filme.ano:
            confirmacao.erro = 4  # Campo Ano vazio
            confirmacao.resultado = 0
        elif not request.filme.generos:
            confirmacao.erro = 5  # Campo Gêneros vazio
            confirmacao.resultado = 0
        elif not request.filme.atores:
            confirmacao.erro = 6  # Campo Atores vazio
            confirmacao.resultado = 0
        elif not request.filme.duracao:
            confirmacao.erro = 7  # Campo Duração vazio
            confirmacao.resultado = 0
        elif any(diretor == "" for diretor in request.filme.diretores):
            confirmacao.erro = 12  # Campo Diretor vazio
            confirmacao.resultado = 0
        elif any(genero == "" for genero in request.filme.generos):
            confirmacao.erro = 13  # Campo Gêneros vazio
            confirmacao.resultado = 0
        elif any(ator == "" for ator in request.filme.atores):
            confirmacao.erro = 14  # Campo Atores vazio
            confirmacao.resultado = 0
        else:
            resultado = banco_de_dados.update(request.filme)
            if resultado == False:
                confirmacao.resultado = 0
                confirmacao.erro = 10  # Erro ao atualizar o filme
            else:
                confirmacao.resultado = 3


        return confirmacao
    def DeleteFilme(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()

        if not request.filme.id:
            confirmacao.erro = 1  # Campo ID vazio
            confirmacao.resultado = 0
        else:
            resultado = banco_de_dados.delete(request.filme)
            if resultado == False:
                confirmacao.resultado = 0
                confirmacao.erro = 11  # Erro ao deletar o filme
            else:
                confirmacao.filme.CopyFrom(request.filme)
                confirmacao.resultado = 4

        return confirmacao
    def ListarFilmesAtor(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()
        if not request.filme.atores:
            confirmacao.erro = 1  # Campo Atores vazio
            confirmacao.resultado = 0
        else:
            filmes_lidos = banco_de_dados.read_by_actors(request.filme)
            print(filmes_lidos)
            if filmes_lidos is None:
                confirmacao.resultado = 0
                confirmacao.erro = 9  # Erro ao ler o filme 
            else:
                confirmacao.resultado = 6
                # Adiciona todos os filmes lidos ao campo `filmes`
                confirmacao.filmes.extend(filmes_lidos.filmes)

        return confirmacao
    def ListarFilmesPorGenero(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()
        if not request.filme.generos:
            confirmacao.erro = 1  # Campo genero vazio
            confirmacao.resultado = 0
        else:
            filmes_lidos = banco_de_dados.read_by_genre(request.filme)
            print(filmes_lidos)
            if filmes_lidos is None:
                confirmacao.resultado = 0
                confirmacao.erro = 9  # Erro ao ler o filme 
            else:
                confirmacao.resultado = 6
                # Adiciona todos os filmes lidos ao campo `filmes`
                confirmacao.filmes.extend(filmes_lidos.filmes)

        return confirmacao
    

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mflix_pb2_grpc.add_MflixServicer_to_server(Mflix(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()