# Autores: Marcos Bezner Rampaso e Pedro Henrique de Oliveira Costa
# Data: 10/09/2024
# Descrição: cliente que se comunica com o servidor para criar, ler, atualizar e deletar filmes, além de buscar filmes por atores e gêneros.

this_dir = File.expand_path(File.dirname(__FILE__)) # Diretório atual
lib_dir = File.join(this_dir, 'lib') # Diretório da biblioteca
$LOAD_PATH.unshift(lib_dir) unless $LOAD_PATH.include?(lib_dir) # Adiciona o diretório da biblioteca ao PATH

require 'grpc' # Importa a biblioteca gRPC
require 'mflix_services_pb' # Importa o arquivo gerado pelo protoc

def main
  hostname = 'localhost:50051' # Endereço do servidor
  puts "Digite o nome do usuário:" 
  stub = Mflix::Mflix::Stub.new(hostname, :this_channel_is_insecure) # Cria um stub para se comunicar com o servidor
  conexao = 1 # Variável para manter a conexão com o servidor
  while conexao == 1
    pedido = Mflix::Pedido.new # Cria um novo pedido
    pedido.filme = Mflix::Filme.new # Cria um novo filme
    puts "Digite a opção\n Create - 1\t Read - 2\n Update - 3\t Remove - 4\n Quit - 5:  Buscar por atores - 6\n Buscar por generos - 7"
    op = gets.chomp.to_i
    case op
    when 1  # Create
      pedido.filme.id = ""  # Envia um ID vazio para o servidor
      puts "Digite o titulo do filme: "
      pedido.filme.titulo = gets.chomp
      puts "Quantidade de diretores"
      qtd_diretores = gets.chomp.to_i
      qtd_diretores.times do
        puts "Digite o nome do diretor: "
        diretor = gets.chomp
        pedido.filme.diretores.push(diretor)
      end
      puts "Digite o ano de lançamento do filme: "
      pedido.filme.ano = gets.chomp.to_i
      puts "Quantidade de atores do filme: "
      qtd_atores = gets.chomp.to_i
      qtd_atores.times do
        puts "Digite o ator do filme: "
        ator = gets.chomp
        pedido.filme.atores.push(ator)
      end
      puts "Quantidade de generos do filme: "
      qtd_generos = gets.chomp.to_i
      qtd_generos.times do
        puts "Digite o genero do filme: "
        genero = gets.chomp
        pedido.filme.generos.push(genero)
      end
      puts "Digite a duração do filme: "
      pedido.filme.duracao = gets.chomp.to_i
      confirmacao = stub.criar_filme(pedido) # Envia o pedido para o servidor

    when 2  # Read
      puts "Digite o id do filme que será lido: "
      pedido.filme.id = gets.chomp
      confirmacao = stub.read_filme(pedido) # Envia o pedido para o servidor
   
    when 3  # Update  
      # Solicita o ID do filme que será atualizado
      puts "Digite o id do filme que será atualizado: "
      pedido.filme.id = gets.chomp
    
      # Solicita o título do filme
      puts "Digite o titulo do filme: "
      pedido.filme.titulo = gets.chomp
    
      # Solicita a quantidade de diretores e seus nomes
      puts "Quantidade de diretores: "
      qtd_diretores = gets.chomp.to_i
      pedido.filme.diretores.clear  # Limpa a lista antes de adicionar novos diretores
      qtd_diretores.times do
        puts "Digite o nome do diretor: "
        diretor = gets.chomp
        pedido.filme.diretores.push(diretor)
      end
    
      # Solicita o ano de lançamento do filme
      puts "Digite o ano de lançamento do filme: "
      pedido.filme.ano = gets.chomp.to_i
    
      # Solicita a quantidade de atores e seus nomes
      puts "Quantidade de atores do filme: "
      qtd_atores = gets.chomp.to_i
      pedido.filme.atores.clear  # Limpa a lista antes de adicionar novos atores
      qtd_atores.times do
        puts "Digite o ator do filme: "
        ator = gets.chomp
        pedido.filme.atores.push(ator)
      end
    
      # Solicita a quantidade de gêneros e seus nomes
      puts "Quantidade de gêneros do filme: "
      qtd_generos = gets.chomp.to_i
      pedido.filme.generos.clear  # Limpa a lista antes de adicionar novos gêneros
      qtd_generos.times do
        puts "Digite o gênero do filme: "
        genero = gets.chomp
        pedido.filme.generos.push(genero)
      end
    
      # Solicita a duração do filme
      puts "Digite a duração do filme (em minutos): "
      pedido.filme.duracao = gets.chomp.to_i
      confirmacao = stub.update_filme(pedido)
      
    when 4  # Remove
      puts "Digite o id do filme a ser deletado: "
      pedido.filme.id = gets.chomp
      confirmacao = stub.delete_filme(pedido)
  
    when 5  # Close
      puts "Enviar mensagem para terminar conexão"
      conexao = 0
      break

  
    when 6 # Buscar por atores
      pedido.filme.id = ""  # Garantir que o ID está vazio para busca por atores
      pedido.filme.atores.clear  # Limpar a lista de atores antes de adicionar o ator
      puts "Digite o nome do ator: "
      ator = gets.chomp 
      pedido.filme.atores.push(ator)
      confirmacao = stub.lista_filmes_ator(pedido)
      
    when 7 # Buscar por generos
      pedido.filme.id = ""  # Garantir que o ID está vazio para busca por generos
      pedido.filme.generos.clear  # Limpar a lista de generos antes de adicionar o genero
      puts "Digite o nome do genero: "
      genero = gets.chomp
      pedido.filme.generos.push(genero)
      confirmacao = stub.lista_filmes_genero(pedido)
    
      if confirmacao.resultado == 7
        puts "Filmes encontrados:"
        confirmacao.filmes.each do |filme|
          puts "ID: #{filme.id}"
          puts "Título: #{filme.titulo}"
          puts "Diretores: #{filme.diretores.join(', ')}"
          puts "Atores: #{filme.atores.join(', ')}"
          puts "Gêneros: #{filme.generos.join(', ')}"
          puts "Duração: #{filme.duracao} minutos"
          puts "Ano: #{filme.ano}"
          puts "-" * 20
        end
      else
        puts "Nenhum filme encontrado ou erro na busca."
      end
    else
      puts "Opção inválida"
      pedido.op = 0
      next
    end
  
    case confirmacao.resultado
    when 1
      puts "Filme criado com sucesso!"
      puts "ID: #{confirmacao.filme.id}"
      puts "Título: #{confirmacao.filme.titulo}"
      puts "Diretores: #{confirmacao.filme.diretores.join(', ')}"
      puts "Atores: #{confirmacao.filme.atores.join(', ')}"
      puts "Gêneros: #{confirmacao.filme.generos.join(', ')}"
      puts "Duração: #{confirmacao.filme.duracao}"
      puts "Ano: #{confirmacao.filme.ano}"
    when 2
      puts "Filme lido com sucesso!"
      puts "ID: #{confirmacao.filme.id}"
      puts "Título: #{confirmacao.filme.titulo}"
      puts "Diretores: #{confirmacao.filme.diretores.join(', ')}"
      puts "Atores: #{confirmacao.filme.atores.join(', ')}"
      puts "Gêneros: #{confirmacao.filme.generos.join(', ')}"
      puts "Duração: #{confirmacao.filme.duracao} minutos"
      puts "Ano: #{confirmacao.filme.ano}"
    when 3
      puts "Filme atualizado com sucesso!"
    when 4
      puts "Filme removido com sucesso!"
      puts "ID: #{confirmacao.filme.id}"
    when 5
      puts "Conexão encerrada."
      break
    when 6
      confirmacao.filmes.each do |filme|
          puts "Filme encontrado:"
          puts "ID: #{filme.id}"
          puts "Título: #{filme.titulo}"
          puts "Diretores: #{filme.diretores.join(', ')}"
          puts "Atores: #{filme.atores.join(', ')}"
          puts "Gêneros: #{filme.generos.join(', ')}"
          puts "Duração: #{filme.duracao} minutos"
          puts "Ano: #{filme.ano}"
          puts "-" * 20
        end
    else
      case confirmacao.erro
      when 1
        puts "Campo id vazio"
      when 2
        puts "Campo titulo vazio"
      when 3
        puts "Lista de diretores vazia"
      when 4
        puts "Campo ano vazio"
      when 5
        puts "Lista de generos vazia"
      when 6
        puts "Lista de atores vazia"
      when 7
        puts "Campo duracao vazio"
      when 8
        puts "Erro ao criar filme"
      when 9
        puts "Erro ao ler filme"
      when 10
        puts "Erro ao atualizar filme"
      when 11
        puts "Erro ao remover filme"
      when 12
        puts "Campo de diretores vazio"
      when 13
        puts "Campo de generos vazio"
      when 14
        puts "Campo de atores vazio"
      end
    end 
  end
end




main
