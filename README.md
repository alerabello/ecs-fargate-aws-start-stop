## AWS ECS Task Scheduler

- Este é um script em Python que permite agendar a inicialização e paralisação de tarefas (tasks) do Amazon Elastic Container Service (ECS) com base em tags configuradas. Ele utiliza a biblioteca Boto3 para interagir com a API do ECS.

- Pré-requisitos
   - Certifique-se de ter o Python instalado em sua máquina.
   - Configure as credenciais de acesso da AWS localmente usando o AWS CLI ou definindo as variáveis de ambiente AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY.
1. Configuração
   - Instale a biblioteca Boto3 executando o seguinte comando:
      - pip install boto3
2. Faça o download do arquivo ecs_task_scheduler.py e salve-o em seu diretório de trabalho.

3. Abra o arquivo ecs_task_scheduler.py em um editor de texto.

4. No código, substitua 'your_cluster_arn' pela ARN (Amazon Resource Name) do cluster ECS que contém as tarefas que você deseja agendar.

5. Personalize as listas DAYS e current_time_local conforme necessário para definir a programação dos dias da semana e o fuso horário local.

6. Configure as tags nas definições das tarefas do ECS para definir os períodos de paralisação e início. Por exemplo:
   - Para paralisação: ScheduleStop-<period_number>, onde <period_number> é o número do período.
   - Para início: ScheduleStart-<period_number>, onde <period_number> é o número do período.
   - Para definir o período: Period-<period_number>, onde <period_number> é o número do período. O valor do período deve ser especificado como <start_time>-<end_time>, por exemplo, 08:00-17:00.

# Uso
1. Execute o script Python executando o seguinte comando:
      - python ecs_task_scheduler.py
2. O script verificará as tarefas no cluster ECS e executará ações com base nas tags configuradas. As tarefas que correspondem aos períodos de paralisação serão paralisadas, e as tarefas que correspondem aos períodos de início serão iniciadas.
3. Verifique o terminal para obter informações sobre as ações executadas.

# Limitações
1. O script considera apenas tarefas individuais no cluster ECS. Tarefas em serviços, tarefas em execução por serviços do ECS ou tarefas em execução em instâncias EC2 não são suportadas.
2. Certifique-se de que o script esteja em execução continuamente ou agendado para ser executado nos horários desejados.

# Considerações Finais
Este script fornece uma maneira simples de agendar a inicialização e paralisação de tarefas no ECS com base em tags configuradas. Certifique-se de revisar e personalizar o código de acordo com suas necessidades específicas antes de executá-lo em um ambiente de produção.

Lembre-se de que a responsabilidade por agendar e gerenciar as tarefas do ECS recai sobre o usuário, e este script é apenas uma ferramenta para auxiliar nesse processo.