# meeting-room-manager

### Requisitos:

- Docker: https://docs.docker.com/install/

### Iniciar o projeto:

Após clonar/baixar o repositório, dentro do diretório raiz do projeto rode no terminal

make build && make run && make up

### Para utilizar o Browsable API acesse no seu browser as seguintes URIs:

**Recurso das salas**

URI :: http://127.0.0.1:8000/meeting-room/

Métodos permitidos:

- GET
- POST :: Exemplo de dados de envio:
{
    "name": "Torre Stark"
}

URI :: http://127.0.0.1:8000/meeting-room/{int}/

Métodos permitidos:

- GET
- DELETE
- PUT :: Exemplo de dados de envio:
{
    "name": "Sala da Justiça"
}


**Recurso de agendamento**

URI :: http://127.0.0.1:8000/meeting-room/schedule/

Métodos permitidos:

- GET
- POST :: Exemplo de dados de envio:
{
    "title": "Reunião da Liga da Justiça",
    "room": 3,
    "start": "2018-10-06T00:00:00Z",
    "end": "2018-10-06T00:50:00Z"
}

URI :: http://127.0.0.1:8000/meeting-room/schedule/{int}/

Métodos permitidos:

- GET
- DELETE
- PUT :: Exemplo de dados de envio:
{
    "title": "Reunião da Liga da Justiça",
    "room": 3,
    "start": "2018-10-06T00:00:00Z",
    "end": "2018-10-06T00:50:00Z"
}

### Testes e utilidades:

Rodar testes:

make test

Rodar testes usando o coverage:

make coverage

Gerar relatório de cobertura:

make report

Reiniciar (ou iniciar) o container:

make restart

Acessar bash dentro do container:

make cmd

Mais opções:

make help
