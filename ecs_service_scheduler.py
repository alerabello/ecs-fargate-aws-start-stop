import boto3
import datetime
import pytz

def update_ecs_service_schedule(service_name, schedule_tags):
    ecs_client = boto3.client('ecs')

    # Obter a lista de serviços ECS com base no nome do serviço
    response = ecs_client.list_services(
        cluster='your_cluster_name',
        launchType='FARGATE',
        serviceName=service_name
    )

    # Verificar se o serviço existe
    if 'serviceArns' not in response or len(response['serviceArns']) == 0:
        print(f"O serviço '{service_name}' não foi encontrado.")
        return

    service_arn = response['serviceArns'][0]

    # Obter o estado atual do serviço
    describe_response = ecs_client.describe_services(
        cluster='your_cluster_name',
        services=[service_arn]
    )

    if 'services' not in describe_response or len(describe_response['services']) == 0:
        print(f"O serviço '{service_name}' não foi encontrado.")
        return

    service = describe_response['services'][0]

    # Obter a data e hora atual
    current_time = datetime.datetime.now(pytz.utc)

    # Verificar os horários de início/parada programados com base nas tags
    for tag_key, tag_value in schedule_tags.items():
        if tag_key.lower().startswith('period-') and tag_value.lower() == 'active':
            period_number = tag_key.lower().replace('period-', '')
            schedule_start_key = f"ScheduleStart-{period_number}"
            schedule_stop_key = f"ScheduleStop-{period_number}"

            if schedule_start_key in schedule_tags and schedule_stop_key in schedule_tags:
                schedule_start = datetime.datetime.strptime(schedule_tags[schedule_start_key], '%H:%M').time()
                schedule_stop = datetime.datetime.strptime(schedule_tags[schedule_stop_key], '%H:%M').time()

                if schedule_start <= current_time.time() <= schedule_stop:
                    # Atualizar o número de tarefas desejado para 1 para iniciar o serviço
                    ecs_client.update_service(
                        cluster='your_cluster_name',
                        service=service_arn,
                        desiredCount=1
                    )
                else:
                    # Atualizar o número de tarefas desejado para 0 para parar o serviço
                    ecs_client.update_service(
                        cluster='your_cluster_name',
                        service=service_arn,
                        desiredCount=0
                    )

# Exemplo de uso
schedule_tags = {
    'Scheduled': 'Active',
    'Period-1': 'Monday-Friday',
    'ScheduleStart-1': '06:00',
    'ScheduleStop-1': '18:00',
    'Period-2': 'Saturday',
    'ScheduleStart-2': '09:00',
    'Period-3': 'Sunday',
    'ScheduleStop-3': '02:00'
}

service_name = 'your_service_name'
update_ecs_service_schedule(service_name, schedule_tags)
