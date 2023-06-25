import boto3
from datetime import datetime, timedelta

def update_ecs_services(cluster_name, services, desired_count):
    ecs_client = boto3.client('ecs')

    for service in services:
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service,
            desiredCount=desired_count
        )
        print(f"Updated service '{service}': {response}")

def lambda_handler(event, context):
    cluster_name = 'nome-do-cluster'  # Substitua pelo nome do seu cluster ECS
    services = ['service1', 'service2', 'service3', 'service4']  # Substitua pelos nomes dos seus serviços ECS
    
    current_day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')

    # Mapeamento dos períodos e horários de início/parada
    schedule = { 
        'Period-1': {
            'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'start': '08:00',
            'stop': '20:00'
        },
        'Period-2': { 
            'days': ['Saturday'],
            'start': '18:30',
            'stop': '18:35'
        },
        'Period-3': {
            'days': ['Sunday'],
            'start': '18:30',
            'stop': '18:35'
        }
    }
    
    desired_count = 0  # Valor padrão para parar o serviço

    # Verifica os períodos e horários de início/parada
    for period, data in schedule.items():
        if current_day in data['days']:
            if data['start'] and current_time >= data['start']:
                desired_count = 1
            elif data['stop'] and current_time <= data['stop']:
                desired_count = 0
    
    # Atualiza os serviços do ECS com a contagem desejada
    update_ecs_services(cluster_name, services, desired_count)
