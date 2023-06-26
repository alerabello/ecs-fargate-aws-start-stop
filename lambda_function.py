import boto3
import logging
from datetime import datetime, timedelta

# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def update_ecs_services(cluster_name, services, desired_count):
    ecs_client = boto3.client('ecs')

    for service in services:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service,
            desiredCount=desired_count
        )
        logger.info(f"Updated service '{service}': {response}")

def lambda_handler(event, context):
    cluster_name = 'seu-cluster'  # Substitua pelo nome do seu cluster ECS
    services = ['services 1', 'services 2', 'services 3', 'services 4']  # Substitua pelos nomes dos seus serviços ECS
    
    current_time = datetime.now() - timedelta(hours=3)
    current_time_local = current_time.strftime("%H:%M")
    logger.info(f'Current time: {current_time_local}')
    
    current_day = current_time.strftime("%A")
    logger.info(f'Current day: {current_day}')
    
    # Mapeamento dos períodos e horários de início/parada
    schedule = { 
        'Period-1': {
            'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'start': '08:00',
            'stop': '20:00'
        }
    }
    
    desired_count = 0  # Valor padrão para parar o serviço
    logger.info(f"Desired count: {desired_count}")

    # Verifica os períodos e horários de início/parada
    for period, data in schedule.items():
        if current_day in data['days']:
            if data['start'] and current_time_local >= data['start'] and current_time_local < data['stop']:
                desired_count = 1
                logger.info(f"Routine: {period} - Services configured: {services}")
            else:
                desired_count = 0
                logger.info(f"Routine: {period} - Services configured: []")
    
    # Atualiza os serviços do ECS com a contagem desejada
    update_ecs_services(cluster_name, services, desired_count)
    logger.info("Lambda function completed.")
