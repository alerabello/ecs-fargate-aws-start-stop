# Script Python para ligar e desligar tarefas do Amazon ECS Fargate através de tags

Este script Python usa a biblioteca boto3 para ligar e desligar tarefas do Amazon ECS Fargate com base em tags. Ele se conecta à sua conta da AWS usando as credenciais configuradas localmente.

## Requisitos

- Python 3.x instalado
- Biblioteca boto3 instalada (`pip install boto3`)

## Configuração

1. Certifique-se de ter as credenciais da AWS configuradas localmente. Você pode configurar as credenciais seguindo o guia oficial da AWS: [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

2. Edite o arquivo `ecs_fargate_control.py` e substitua os seguintes valores:

   - `your_cluster_name`: Substitua pelo nome do seu cluster ECS Fargate.
   - `your_tag_key`: Substitua pela chave da tag que deseja usar para identificar as tarefas.
   - `your_tag_value`: Substitua pelo valor da tag que deseja usar
   
## OTIMIZADO E CORRIGIDO PELO CHAT GPT
