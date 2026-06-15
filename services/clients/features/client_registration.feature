# language: pt
Funcionalidade: Cadastro de clientes (tutores)
  Como funcionário da clínica veterinária
  Quero cadastrar clientes no sistema
  Para que possam ser vinculados aos seus animais de estimação

  Cenário: Cadastrar um novo cliente com sucesso
    Dado que possuo um token JWT válido de veterinário
    Quando eu cadastrar um cliente com os dados:
      | nome_completo | Ana Paula Santos        |
      | email         | ana.santos@email.com    |
      | telefone      | 11987654321             |
      | cpf           | 123.456.789-09          |
      | endereco      | Rua Vet+, 123 - São Paulo |
    Então o cadastro deve ser realizado com sucesso
    E a resposta deve conter o nome "Ana Paula Santos"
    E a resposta deve conter o e-mail "ana.santos@email.com"

  Cenário: Falha ao cadastrar cliente com e-mail duplicado
    Dado que possuo um token JWT válido de veterinário
    E que já existe um cliente cadastrado com e-mail "duplicado@email.com"
    Quando eu cadastrar um cliente com os dados:
      | nome_completo | Outro Cliente           |
      | email         | duplicado@email.com     |
      | telefone      | 11911112222             |
      | cpf           | 987.654.321-00          |
      | endereco      | Rua Duplicada, 1        |
    Então o cadastro deve falhar com erro de validação
