import boto3
import datetime
import pytz

def lambda_handler(event, context):
    # Configurar o cliente do ECS
    ecs_client = boto3.client('ecs')

    # Configurar as informações do cluster ECS
    cluster_name = 'nome-do-cluster'
    timezone = 'America/Sao_Paulo'

    # Obter a data e hora atual com base no fuso horário configurado
    current_time = datetime.datetime.now(pytz.timezone(timezone))

    # Obter o dia da semana atual
    current_day = current_time.strftime('%A')

    # Obter o período e horários de início/fim com base no dia da semana atual
    if current_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        period = 'Period-1'
        start_time = datetime.time(6, 0)  # 06:00
        stop_time = datetime.time(18, 0)  # 18:00
    elif current_day == 'Saturday':
        period = 'Period-2'
        start_time = datetime.time(9, 0)  # 09:00
        stop_time = None
    elif current_day == 'Sunday':
        period = 'Period-3'
        start_time = None
        stop_time = datetime.time(2, 0)  # 02:00
    else:
        # Não há programação para outros dias da semana
        return

    # Obter os ARNs dos serviços do cluster
    services = ecs_client.list_services(cluster=cluster_name)['serviceArns']

    # Atualizar a configuração dos serviços com base nos horários programados
    for service in services:
        ecs_client.update_service(
            cluster=cluster_name,
            service=service,
            schedulingStrategy='REPLICA',  # Ou 'DAEMON', dependendo da estratégia do serviço
            desiredCount=0 if stop_time else 1  # Definir 0 para parar ou 1 para iniciar o serviço
        )

    print(f'Serviços do cluster {cluster_name} atualizados com sucesso para o período {period}')

