# language: pt
Funcionalidade: Registro de Animais
  Como veterinário da clínica Vet Plus+
  Quero registrar animais no sistema
  Para gerenciar o prontuário dos pacientes

  Cenário: Registrar um novo animal com sucesso
    Dado que estou autenticado como veterinário
    Quando eu registro um animal com os dados:
      | name | species | breed    | birth_date | weight | client_id |
      | Rex  | Cão     | Labrador | 2020-05-10 | 25.5   | 1         |
    Então o animal deve ser criado com sucesso
    E o nome do animal deve ser "Rex"
    E a espécie do animal deve ser "Cão"

  Cenário: Registrar animal sem autenticação
    Dado que não estou autenticado
    Quando eu tento registrar um animal com os dados:
      | name | species | breed | client_id |
      | Bob  | Cão     | Poodle| 1         |
    Então devo receber erro de autenticação

  Cenário: Consultar animal registrado
    Dado que estou autenticado como veterinário
    E existe um animal "Mimi" do tipo "Gato" para o cliente 2
    Quando eu consulto os detalhes do animal
    Então devo ver o nome "Mimi"
    E devo ver a espécie "Gato"
