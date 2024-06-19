# Projeto de Cadastro em Python com Flask

Este é um projeto simples de cadastro de usuários desenvolvido em Python utilizando o framework Flask. O projeto inclui operações básicas de CRUD (Create, Read, Update, Delete) para gerenciar informações de clientes.

### Endpoints da API

- **GET ALL USERS**
  Endpoint para obter todos os usuários cadastrados.
  GET http://localhost:3033/cadastros

![Exemplo GET ALL USERS](https://github.com/maaicondgl/CadastroPython/assets/87240984/90fdaac7-010d-4d4d-a374-ebe7fd373900)

- **GET USERS BY USERID**
Endpoint para obter um usuário específico pelo ID.



![Exemplo GET ALL USERS](https://github.com/maaicondgl/CadastroPython/assets/87240984/90fdaac7-010d-4d4d-a374-ebe7fd373900)

- **GET USER BY USERID**
Endpoint para obter um usuário específico pelo ID.

GET http://localhost:3033/cadastros/search/{userId}

![Exemplo GET USERS BY USERID](https://github.com/maaicondgl/CadastroPython/assets/87240984/41e7cad1-1b40-4c8d-af57-7cf3161bdb21)

- **REGISTER**
Endpoint para cadastrar um novo usuário.
POST http://localhost:3033/cadastros/create

![Exemplo REGISTER](https://github.com/maaicondgl/CadastroPython/assets/87240984/b422fe59-9832-474e-84e9-70eba5d7d412)

- **UPDATE**
Endpoint para atualizar informações de um usuário pelo ID.
PUT http://localhost:3033/cadastros/update/{userId}

![Exemplo UPDATE](https://github.com/maaicondgl/CadastroPython/assets/87240984/d062aaca-212d-40d9-862e-66ff63ebdfa8)

- **DELETE**
Endpoint para excluir um usuário pelo ID.
DELETE http://localhost:3033/cadastros/delete/{userId}

![Exemplo DELETE](https://github.com/maaicondgl/CadastroPython/assets/87240984/fa57f2da-32ed-4540-9c09-68195bca088e)

- **LOGIN**
Endpoint para autenticar um usuário.
POST http://localhost:3033/login

![Exemplo LOGIN](https://github.com/maaicondgl/CadastroPython/assets/87240984/05a7ba71-7185-4131-9703-ceb75591409f)

