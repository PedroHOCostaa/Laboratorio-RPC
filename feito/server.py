# Autores: Marcos Bezner Rampaso e Pedro Henrique de Oliveira Costa
# Data: 10/09/2024
# Descrição: Servidor que recebe requisições de um cliente e executa operações CRUD em um banco de dados MongoDB.
# O servidor é capaz de criar, ler, atualizar e deletar filmes, além de realizar uma busca por atores e generos.
# O servidor é capaz de lidar com múltiplos clientes simultaneamente.

from concurrent import futures
import logging
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import grpc
import mflix_pb2
import mflix_pb2_grpc

# Classe para manipulação do banco de dados
class BancoDeDados:

# Método para criar um filme no banco de dados
    def create(self, filme):
        erro = 0
        if erro == 0:
            return True, filme
        else:
            return False
        
# Método para ler um filme no banco de dados
    def read(self, filme_id):
        try:
            # Procura o filme na coleção usando o ObjectId
            filme_documento = self.collection.find_one({"_id": filme_id})
            if filme_documento:
                return True, filme_documento
            else:
                return False, None
        except Exception as e:
            print(f"Erro ao ler filme: {e}")
            return False, None
        
# Método para atualizar um filme no banco de dados
    def update(self, filme):
        erro = 0
        print("Atualizando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False
        
# Método para deletar um filme no banco de dados
    def delete(self, filme):
        erro = 0
        print("Deletando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False
        
# Método para listar filmes por ator
    def read_by_actors(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False

# Método para listar filmes por gênero
    def read_by_genre(self, filme):
        erro = 0
        print("Criando filme" + filme.titulo)
        if erro == 0:
            return True
        else:
            return False

# Classe do servidor gRPC
class Mflix(mflix_pb2_grpc.MflixServicer):
    def __init__(self):
        # Conecta-se ao MongoDB e seleciona a coleção de filmes
        uri = "mongodb+srv://admin:admin@mflix-db.e3wrt.mongodb.net/?retryWrites=true&w=majority&appName=mflix-db"
        self.client = MongoClient(uri, server_api=ServerApi('1')) # Conecta-se ao MongoDB
        self.db = self.client['sample_mflix']   # Seleciona o banco de dados
        self.collection = self.db['movies']     # Seleciona a coleção de filmes
        self.banco_de_dados = BancoDeDados()    # Instancia a classe de manipulação do banco de dados
    
    # Método para criar um filme dentro do banco de dados
    def CriarFilme(self, request,filme):
        confirmacao = mflix_pb2.Confirmacao()

        # Verificações dos campos do filme
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
            # Cria o documento do filme para inserção, sem o campo '_id' para que seja gerado automaticamente
            filme_documento = {
                "title": request.filme.titulo,
                "directors": list(request.filme.diretores),  # Converter para lista 
                "year": request.filme.ano,
                "cast": list(request.filme.atores),  # Converter para lista
                "genres": list(request.filme.generos),  # Converter para lista
                "runtime": request.filme.duracao 
            }

            # Insere o filme na coleção do MongoDB
            try:
                result = self.collection.insert_one(filme_documento)  # O MongoDB gera o ID automaticamente
                print(f"Filme '{request.filme.titulo}' criado com ID: {result.inserted_id}")

                # Cria uma nova instância de filme com o ID gerado pelo MongoDB
                filme_criado = mflix_pb2.Filme(
                    id=str(result.inserted_id),  # Pega o ObjectId gerado e converte para string
                    titulo=request.filme.titulo,
                    diretores=request.filme.diretores,
                    ano=request.filme.ano,
                    atores=request.filme.atores,
                    generos=request.filme.generos,
                    duracao=request.filme.duracao
                )
                confirmacao.resultado = 1 # Sucesso
                confirmacao.filme.CopyFrom(filme_criado)  # Usa o método CopyFrom para preencher o campo 'filme'
            except Exception as e:
                print(f"Erro ao criar filme: {e}")
                confirmacao.erro = 8  # Erro ao criar o filme
                confirmacao.resultado = 0
        
        return confirmacao

# Método para ler um filme no banco de dados
    def ReadFilme(self, request,filme):
        print("Lendo o filme com ID:", request.filme.id) # Log para depuração
        confirmacao = mflix_pb2.Confirmacao() # Cria a mensagem de confirmação

        try:
            # Converte o ID para ObjectId
            object_id = ObjectId(request.filme.id) # Converte o ID para ObjectId
            
            # Busca o filme no MongoDB pelo ID
            mongo_filme = self.collection.find_one({"_id": object_id})
            
            if mongo_filme is None: # Se o filme não for encontrado
                print("Filme não encontrado")
                confirmacao.erro = 9  # Código de erro para filme não encontrado
                confirmacao.resultado = 0
            else:
                # Cria um novo objeto Filme do Protocol Buffer
                filme_lido = mflix_pb2.Filme()

                # Popula o objeto com os dados retornados do MongoDB
                filme_lido.id = str(mongo_filme["_id"])  # O ID no MongoDB é um ObjectId
                filme_lido.titulo = mongo_filme.get("title", "")
                filme_lido.diretores.extend(mongo_filme.get("directors", []))
                filme_lido.ano = mongo_filme.get("year", 0)
                filme_lido.atores.extend(mongo_filme.get("cast", []))
                filme_lido.generos.extend(mongo_filme.get("genres", []))
                filme_lido.duracao = mongo_filme.get("runtime", 0)

                confirmacao.resultado = 2
                confirmacao.filme.CopyFrom(filme_lido)  # Usa o método CopyFrom para preencher o campo 'filme'
        except Exception as e:
            print(f"Erro ao ler filme: {e}")
            confirmacao.erro = 9  # Código de erro genérico
            confirmacao.resultado = 0
        
        return confirmacao  # Retorna a resposta para o cliente

# Método para atualizar um filme no banco de dados
    def UpdateFilme(self, request,filme):
        print("Atualizando o filme com ID:", request.filme.id)
        confirmacao = mflix_pb2.Confirmacao()

        if not request.filme.titulo:
            print("Título não fornecido")
            return False

        # Converte o ID para ObjectId se necessário
        try:
            object_id = ObjectId(request.filme.id)
        except Exception as e:
            print(f"Erro ao converter ID para ObjectId: {e}")
            return False

        # Prepara o documento para atualização
        update_doc = {
            "title": request.filme.titulo,
            "directors": list(request.filme.diretores),  # Converte para lista padrão
            "year": request.filme.ano,
            "cast": list(request.filme.atores),           # Converte para lista padrão
            "genres": list(request.filme.generos),       # Converte para lista padrão
            "runtime": request.filme.duracao
        }

        # Atualiza o filme na coleção
        result = self.collection.update_one({"_id": object_id}, {"$set": update_doc})
        
        if result.modified_count > 0:
            print("Filme atualizado com sucesso!")
            confirmacao.resultado = 3  # Código de sucesso
        else:
            print("Erro ao atualizar o filme")
            confirmacao.erro = 4  # Código de erro para falha na atualização
            confirmacao.resultado = 0
        
        return confirmacao      

# Método para deletar um filme no banco de dados
    def DeleteFilme(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()

        try:
            object_id = ObjectId(request.filme.id) # Converte o ID para ObjectId
            
            # Remove o filme da coleção pelo ID
            result = self.collection.delete_one({"_id": object_id})
            
            if result.deleted_count > 0:
                print("Filme deletado com sucesso!")
                confirmacao.resultado = 4
                confirmacao.filme.id = request.filme.id
            else:
                print("Filme não encontrado.")
                confirmacao.erro = 11  # Define o código de erro apropriado
                confirmacao.resultado = 0
                
        except Exception as e:
            print(f"Erro ao deletar filme: {e}")
            confirmacao.erro = 11  # Define o código de erro apropriado
            confirmacao.resultado = 0 # Define o código de resultado apropriado

        return confirmacao
    
# Método para listar filmes por ator
    def ListaFilmesAtor(self, request, context):
        confirmacao = mflix_pb2.Confirmacao()
        print("Lendo o filme com atores:", request.filme.atores) # Log para depuração

        try:
            atores = list(request.filme.atores) # Converte a lista de atores para uma lista padrão
            mongo_filmes = self.collection.find({"cast": {"$in": atores}}) # Busca filmes com atores na lista

            filmes_lidos = mflix_pb2.Filmes() # Cria a mensagem de resposta
            for mongo_filme in mongo_filmes: # Itera sobre os filmes encontrados
                filme_lido = mflix_pb2.Filme()
                filme_lido.id = str(mongo_filme["_id"])
                filme_lido.titulo = mongo_filme.get("title", "")

                diretores = mongo_filme.get("directors", [])
                if isinstance(diretores, list): # Verifica se é uma lista
                    filme_lido.diretores.extend(diretores)
                else:
                    print(f"Tipo inesperado para diretores: {type(diretores)}")

                # Validação e conversão de ano
                ano = mongo_filme.get("year", 0)
                try:
                    filme_lido.ano = int(ano)
                except ValueError:
                    print(f"Valor de ano inválido: {ano}")
                    filme_lido.ano = 0

                atores = mongo_filme.get("cast", []) # Pega a lista de atores
                if isinstance(atores, list):
                    filme_lido.atores.extend(atores)
                else:
                    print(f"Tipo inesperado para atores: {type(atores)}")

                generos = mongo_filme.get("genres", []) # Pega a lista de gêneros
                if isinstance(generos, list):
                    filme_lido.generos.extend(generos)
                else:
                    print(f"Tipo inesperado para generos: {type(generos)}")

                duracao = mongo_filme.get("runtime", 0)
                try:
                    filme_lido.duracao = int(duracao)
                except ValueError:
                    print(f"Valor de duração inválido: {duracao}")
                    filme_lido.duracao = 0
                filmes_lidos.filmes.append(filme_lido)

            if not filmes_lidos.filmes:
                print("Nenhum filme encontrado")
            confirmacao.filmes.extend(filmes_lidos.filmes) # Adiciona os filmes à mensagem de resposta
            confirmacao.resultado = 6 if filmes_lidos.filmes else 9 # Define o código de resultado
            return confirmacao 
        except Exception as e:
            print(f"Erro ao ler filmes: {e}")
            confirmacao.erro = 15  # Defina um código de erro apropriado
            return confirmacao
    
# Método para listar filmes por gênero
    def ListaFilmesGenero(self, request, context): 
        confirmacao = mflix_pb2.Confirmacao()# Cria a mensagem de confirmação
        print("Lendo o filme com genero:", request.filme.generos) # Log para depuração

        try:
            genero = list(request.filme.generos)
            mongo_filmes = self.collection.find({"genres": {"$in": genero}}) # Busca filmes com gêneros na lista

            filmes_lidos = mflix_pb2.Filmes() # Cria a mensagem de resposta
            for mongo_filme in mongo_filmes: # Itera sobre os filmes encontrados
                filme_lido = mflix_pb2.Filme()
                filme_lido.id = str(mongo_filme["_id"]) # Converte o ID para string
                filme_lido.titulo = mongo_filme.get("title", "") # Pega o título do filme
 
                diretores = mongo_filme.get("directors", [])
                if isinstance(diretores, list):
                    filme_lido.diretores.extend(diretores)
                else:
                    print(f"Tipo inesperado para diretores: {type(diretores)}")

                # Validação e conversão de ano
                ano = mongo_filme.get("year", 0)
                try:
                    filme_lido.ano = int(ano)
                except ValueError:
                    print(f"Valor de ano inválido: {ano}")
                    filme_lido.ano = 0

                atores = mongo_filme.get("cast", [])
                if isinstance(atores, list):
                    filme_lido.atores.extend(atores)
                else:
                    print(f"Tipo inesperado para atores: {type(atores)}")

                generos = mongo_filme.get("genres", [])
                if isinstance(generos, list):
                    filme_lido.generos.extend(generos)
                else:
                    print(f"Tipo inesperado para generos: {type(generos)}")

                duracao = mongo_filme.get("runtime", 0)
                try:
                    filme_lido.duracao = int(duracao)
                except ValueError:
                    print(f"Valor de duração inválido: {duracao}")
                    filme_lido.duracao = 0
                filmes_lidos.filmes.append(filme_lido)
            
            if not filmes_lidos.filmes:
                print("Nenhum filme encontrado")
            confirmacao.filmes.extend(filmes_lidos.filmes) # Adiciona os filmes à mensagem de resposta
            confirmacao.resultado = 7 if filmes_lidos.filmes else 8 # Define o código de resultado
            return confirmacao 
        except Exception as e:
            print(f"Erro ao ler filmes: {e}")
            confirmacao.erro = 15  # Defina um código de erro apropriado
            return confirmacao

# Método do servidor para iniciar o serviço
def serve():
    # Cria a conexão com o MongoDB
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # Cria o servidor gRPC com 10 threads
    mflix_pb2_grpc.add_MflixServicer_to_server(Mflix(), server) # Adiciona o serviço ao servidor
    server.add_insecure_port("[::]:" + port) # Define a porta do servidor
    server.start()  # Inicia o servidor
    print("Server started, listening on " + port)
    server.wait_for_termination()

# Inicializa o servidor
if __name__ == "__main__":
    logging.basicConfig()
    serve()