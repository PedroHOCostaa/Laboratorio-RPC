# Projeto de Desenvolvimento em Representação Externa de Dados utilizando gRPC

## Instalação dos Pacotes

Para instalar os pacotes necessários, execute os seguintes comandos:

1. **Python**:

``` bash
   pip install grpcio

   pip install grpcio-tools

```

2. **Ruby**:

``` bash
    gem install grpc
    gem install grpc-tools
```

### Executando a aplicação

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./mflix.proto

grpc_tools_ruby_protoc -I. --ruby_out=. --grpc_out=. ./estrutura/mflix.proto

utilize o seguinte comando:
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./mflix.proto

Explicação do comando :
depois de -I coloque o caminho relativo para o para o codigo .proto que você quer compilar : ./estrutura
depois de --python_out= coloque o caminho para a estrutura protoc ser criada :  ./
depois de grpc_python_out= coloque o caminho para a estrutura grpc ser criada :  ./
Após isto caminho .proto com o codigo no final : ./estrutura/mflix.proto

Para ruby com gRPC siga os seguintes passos:

utilize o seguinte comando:
grpc_tools_ruby_protoc -I. --ruby_out=. --grpc_out=. ./mflix.proto
depois de -I coloque o caminho relativo para o para o codigo .proto que você quer compilar : ./estrutura
depois de --ruby_out= coloque o caminho para a estrutura protoc ser criada :  ./
depois de grpc_out= coloque o caminho para a estrutura grpc ser criada :  ./
Após isto caminho .proto com o codigo no final : ./estrutura/mflix.proto

para utiizar o codigo sera necessarios os seguintes pacote python: grpcio e grpcio-tools
para utiizar o codigo sera necessarios os seguintes pacote ruby: grpc e grpc-tools