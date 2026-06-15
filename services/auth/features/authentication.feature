# language: pt
Funcionalidade: Autenticação de usuários
  Como administrador da clínica
  Eu quero registrar e autenticar usuários
  Para controlar o acesso ao sistema

  Cenário: Registrar usuário com sucesso
    Dado que o serviço de autenticação está disponível
    Quando eu registro um usuário com email "tutor@vet.com" e senha "senha1234"
    Então o registro deve ser realizado com sucesso
    E um token JWT deve ser retornado

  Cenário: Login com credenciais válidas
    Dado que existe um usuário "vet@vet.com" com senha "senha1234"
    Quando eu faço login com email "vet@vet.com" e senha "senha1234"
    Então o login deve ser realizado com sucesso
    E um token Bearer deve ser retornado
