# Script Python para ligar e desligar tarefas do Amazon ECS Fargate através de tags com base em dias e horários

Este script Python usa a biblioteca boto3 para ligar e desligar tarefas do Amazon ECS Fargate com base em tags, considerando diferentes dias e horários. Ele se conecta à sua conta da AWS usando as credenciais configuradas localmente.

## Requisitos

- Python 3.x instalado
- Biblioteca boto3 instalada (`pip install boto3`)
- Biblioteca pytz instalada (`pip install pytz`)

## Configuração

1. Certifique-se de ter as credenciais da AWS configuradas localmente. Você pode configurar as credenciais seguindo o guia oficial da AWS: [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

2. Edite o arquivo `ecs_fargate_schedule.py` e substitua os seguintes valores:

   - `your_cluster_name`: Substitua pelo nome do seu cluster ECS Fargate.
   - `your_tag_key`: Substitua pela chave da tag que deseja usar para identificar as tarefas.
   - `your_tag_value`: Substitua pelo valor da tag que deseja usar.

3. Defina os agendamentos no início do script. Cada agendamento é definido como um dicionário contendo as seguintes informações:
   
   - `name`: Nome do agendamento.
   - `days`: Uma lista de dias da semana em que o agendamento deve ser aplicado.
   - `time`: Horário de início em que as tarefas serão iniciadas (no formato 'HH:MM').
   - `end_time`: Horário de término em que as tarefas serão interrompidas (no formato 'HH:MM').
   - `timezone`: Fuso horário em que o agendamento será aplicado (por exemplo, 'America/New_York').

## Executando as Rotinas

Para executar as rotinas de ligar e desligar as tarefas do ECS Fargate com base nos agendamentos, siga os passos abaixo:

1. No terminal, navegue até o diretório onde o arquivo `ecs_fargate_schedule.py` está localizado.

2. Execute o comando a seguir para iniciar o script:
