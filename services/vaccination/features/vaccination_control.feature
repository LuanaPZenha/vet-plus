# language: pt
Funcionalidade: Controle de Vacinação
  Como veterinário da clínica Vet+
  Quero registrar vacinas aplicadas nos animais
  Para controlar o calendário de vacinação e lembretes

  Cenário: Registrar vacina
    Dado que estou autenticado como veterinário
    Quando eu registro uma vacina com os dados:
      | animal_id | vaccine_name | application_date | next_dose_date | veterinarian_id | batch_number |
      | 1         | V10          | 2026-01-10       | 2026-07-10     | 1               | LOTE123      |
    Então a vacina deve ser registrada com sucesso
    E o nome da vacina deve ser "V10"
    E o animal da vacina deve ser 1

  Cenário: Registrar vacina sem autenticação
    Dado que não estou autenticado
    Quando eu tento registrar uma vacina com os dados:
      | animal_id | vaccine_name | application_date | veterinarian_id |
      | 1         | V10          | 2026-01-10       | 1               |
    Então devo receber erro de autenticação

  Cenário: Consultar histórico de vacinação do animal
    Dado que estou autenticado como veterinário
    E existe uma vacina "Antirrábica" para o animal 2
    Quando eu consulto o histórico de vacinação do animal 2
    Então devo ver a vacina "Antirrábica" no histórico
