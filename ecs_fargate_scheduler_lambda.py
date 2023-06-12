import boto3
from datetime import datetime, time

def lambda_handler(event, context):
    current_time = datetime.now().time()
    
    # Verifique se está dentro do horário desejado
    if is_schedule_matched(event, current_time):
        # Verifique o tipo de evento
        if event['action'] == 'start':
            # Inicie as tarefas do Fargate
            start_fargate_tasks(event['start_tags'])
        elif event['action'] == 'stop':
            # Pare as tarefas do Fargate
            stop_fargate_tasks(event['stop_tags'])
        else:
            # Ação desconhecida
            raise Exception('Ação inválida')
    else:
        print('Fora do horário de execução')

def start_fargate_tasks(tags):
    # Configuração do cliente ECS
    ecs_client = boto3.client('ecs')
    
    # Obtenha os clusters e serviços do ECS com as tags fornecidas
    clusters, services = get_clusters_and_services_with_tags(tags)
    
    # Iniciar tarefas do Fargate para cada cluster e serviço
    for cluster in clusters:
        for service in services[cluster]:
            response = ecs_client.update_service(
                cluster=cluster,
                service=service,
                desiredCount=1  # Defina o número desejado de tarefas
            )
            
            # Verifique o resultado
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f'Tarefas do Fargate iniciadas com sucesso para o cluster {cluster} e serviço {service}')
            else:
                print(f'Falha ao iniciar as tarefas do Fargate para o cluster {cluster} e serviço {service}')

def stop_fargate_tasks(tags):
    # Configuração do cliente ECS
    ecs_client = boto3.client('ecs')
    
    # Obtenha os clusters e serviços do ECS com as tags fornecidas
    clusters, services = get_clusters_and_services_with_tags(tags)
    
    # Parar tarefas do Fargate para cada cluster e serviço
    for cluster in clusters:
        for service in services[cluster]:
            response = ecs_client.update_service(
                cluster=cluster,
                service=service,
                desiredCount=0  # Defina o número desejado de tarefas como 0 para parar todas as tarefas
            )
            
            # Verifique o resultado
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f'Tarefas do Fargate paradas com sucesso para o cluster {cluster} e serviço {service}')
            else:
                print(f'Falha ao parar as tarefas do Fargate para o cluster {cluster} e serviço {service}')

def get_clusters_and_services_with_tags(tags):
    # Configuração do cliente ECS
    ecs_client = boto3.client('ecs')
    
    # Obter informações sobre clusters e serviços com as tags fornecidas
    response = ecs_client.list_clusters()
    clusters = response['clusterArns']
    
    services = {}
    
    # Para cada cluster, obtenha os serviços com as tags fornecidas
    for cluster in clusters:
        response = ecs_client.list_services(cluster=cluster)
        service_arns = response['serviceArns']
        
        services[cluster] = []
        
        # Para cada serviço, verifique se tem as tags desejadas
        for service_arn in service_arns:
            response = ecs_client.describe_services(
                cluster=cluster,
                services=[service_arn]
            )
            
            service = response['services'][0]
            
            # Verifique se o serviço tem todas as tags especificadas
            if all(tag in service['tags'] for tag in tags):
                services[cluster].append(service['serviceName'])
    
    return clusters, services

def is_schedule_matched(event, current_time):
    # Verifique se o dia atual está presente nas tags de dias
    if 'days' in event:
        current_day = datetime.today().strftime('%A').lower()
        if current_day not in event['days']:
            return False
    
    # Verifique se o horário atual está dentro do intervalo de tempo
    if 'start_time' in event and 'end_time' in event:
        start_time = datetime.strptime(event['start_time'], '%H:%M').time()
        end_time = datetime.strptime(event['end_time'], '%H:%M').time()
        return start_time <= current_time <= end_time
    
    return True
