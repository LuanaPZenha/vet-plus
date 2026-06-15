# language: pt
Funcionalidade: Agendamento de consulta
  Como tutor ou veterinário da clínica Vet Plus+
  Quero agendar consultas veterinárias
  Para que os animais recebam atendimento adequado

  Cenário: Agendar consulta com sucesso
    Dado que estou autenticado como veterinário
    E existe um veterinário cadastrado no sistema
    Quando eu agendo uma consulta com os dados:
      | animal_id | scheduled_at           | type    | notes          |
      | 1         | 2026-07-10T10:00:00Z   | regular | Check-up anual |
    Então a consulta deve ser agendada com sucesso
    E o status da consulta deve ser "scheduled"
    E o tipo da consulta deve ser "regular"

  Cenário: Agendar consulta sem autenticação
    Dado que não estou autenticado
    E existe um veterinário cadastrado no sistema
    Quando eu tento agendar uma consulta com os dados:
      | animal_id | scheduled_at           | type    |
      | 1         | 2026-07-10T10:00:00Z   | regular |
    Então devo receber erro de autenticação

  Cenário: Consultar consulta agendada
    Dado que estou autenticado como veterinário
    E existe um veterinário cadastrado no sistema
    E existe uma consulta agendada para o animal 2
    Quando eu consulto os detalhes da consulta
    Então devo ver o animal_id 2
    E devo ver o status "scheduled"
