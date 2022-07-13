# Magalu Challenge
API REST para gerenciar Clientes, Produtos, Reviews e Lista de Desejos.

***
## Indice
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Testes](#testes)
- [Documentação](#documentação)
- [Tutorial](#tutorial)
- [Dependências Utilizadas](#dependências-utilizadas)
- [Contato](#contato)

***
## Requisitos
- Python
- Pip
- PostgreSQL
- Docker
- docker-compose

[Voltar para o topo](#indice)

***
## Instalação
Faça o clone do repositório
```
git clone https://github.com/gabrielebonfim/luizalabs-challenge.git
```

Execute o comando abaixo
```
docker compose up
```

[Voltar para o topo](#indice)
***

## Testes
Os testes estão inclusos na pasta ```api > tests``` e podem ser executados com o comando abaixo:
```
python manage.py test
```

[Voltar para o topo](#indice)
***

## Documentação
A documentação completa está disponível no Postman. [Clique aqui para acessar](https://documenter.getpostman.com/view/14110900/UzJQrEz3).

[Voltar para o topo](#indice)
***

## Tutorial
Para cadastro de lista de desejos, antes é necessário ter um cadastro prévio do cliente e dos produtos que poderão integrar essa lista.

Como primeiro passo, vamos cadastrar uma cliente nova:

- Request
```
POST /api/client/ HTTP/1.1
Host: http://localhost:8000/
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "name": "Beatriz Ribeiro Lima",
    "email":"beatrizribeirolima@email.com"
}
```
- Response
```
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Beatriz Ribeiro",
    "email": "beatriz@email.com"
  }
}
```

Após cadastrar a cliente com sucesso, vamos cadastrar o produto a ser integrado.
- Request
```
POST /api/product/ HTTP/1.1
Host: http://localhost:8000/
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "title": "Jogo de Cama Casal Queen Size 4 Peças Microfibra 150 fios Sultan", 
    "image": "https://bit.ly/3axU0Nm",
    "price": 87.91,
    "brand": "Admirare"
}
```
- Response
```
{
  "success": true,
  "data": {
    "id": 3,
    "title": "Jogo de Cama Casal Queen Size 4 Peças Microfibra 150 fios Sultan",
    "price": "87.91",
    "image": "https://bit.ly/3axU0Nm",
    "brand": "Admirare",
    "review_score": 0
  }
}
```

Com os responses, identificamos que o ID da cliente é de número 1, e o ID do produto é de número 3. Precisamos dessas informações para criação de uma Wishlist.
- Request
```
POST /api/wishlist/ HTTP/1.1
Host: http://localhost:8000/
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "client": 1,
    "products": [3]
}
```

- Response
```
{
  "success": true,
  "data": {
    "id": 1,
    "client": {
      "id": 1,
      "name": "Beatriz Ribeiro",
      "email": "beatriz@email.com"
    },
    "products": [
        {
            "id": 3,
            "title": "Jogo de Cama Casal Queen Size 4 Peças Microfibra 150 fios Sultan",
            "price": "87.91",
            "image": "https://bit.ly/3axU0Nm",
            "brand": "Admirare",
            "review_score": 0
        }
    ]
  }
}
```

[Voltar para o topo](#indice)
***

## Dependências Utilizadas
```
Django==4.0.6
djangorestframework==3.13.1
psycopg2-binary==2.8.5
pillow==9.2.0
faker==13.15.0
djangorestframework-simplejwt==5.2.0
python-dotenv==0.20.0
```

[Voltar para o topo](#indice)
***

## Contato
Em caso de dúvidas ou informações, estou à disposição.

- [Linkedin](https://linkedin.com/in/gabrielealvesbonfim)
- [E-mail](gabriele_bonfim@outlook.com)

[Voltar para o topo](#indice)

