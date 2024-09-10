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

## Como executar

Para executar a aplicação abra o terminal e aplique os seguintes comandos:

``` bash

    python server.py
    ruby cliente.rb
    
```

Selecione as opções que estão disponíveis no terminal cliente.

## Funcionamento

A aplicação é dividida em duas partes principais de execução: o servidor e o cliente.

### Servidor

O servidor é desenvolvido em Python e utiliza gRPC para fornecer uma interface para as operações de CRUD no banco de dados MongoDB. Ele é responsável por:

- **Receber e Processar Solicitações**: O servidor escuta requisições do cliente e processa operações como criação, leitura, atualização e deleção de filmes no banco;de dados;
- **Comunicação via gRPC**: Utiliza o protocolo gRPC para comunicação com o cliente, o que permite uma comunicação eficiente e estruturada entre o servidor e o cliente;

### Cliente

O cliente é desenvolvido em Ruby e interage com o servidor para realizar as operações desejadas. Ele realiza as seguintes tarefas:

- **Solicitação de Operações**: O cliente apresenta ao usuário uma interface para selecionar uma das operações disponíveis, como criar, ler, atualizar ou deletar um filme;
- **Comunicação via gRPC**: Envia solicitações para o servidor usando gRPC e recebe respostas.


## Tecnologias utilizadas

- **gRPC**: Framework para chamadas de procedimentos remotos (RPC) que utiliza Protocol Buffers para definição e troca de mensagens;
- **Ruby**: Linguagem de programação utilizada para implementar o cliente;
- **Python**: Linguagem de programação utilizada para implementar o servidor;
- **MongoDB**: Banco de dados NoSQL utilizado para armazenar as informações dos filmes.
- 