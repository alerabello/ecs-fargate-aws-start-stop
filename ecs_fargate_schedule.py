import boto3
import datetime
import pytz
import time

def start_fargate_tasks(cluster_name, tag_key, tag_value):
    client = boto3.client('ecs')
    
    response = client.list_tasks(
        cluster=cluster_name,
        launchType='FARGATE',
        desiredStatus='STOPPED',
        startedBy='EXTERNAL',
        tags={
            tag_key: tag_value
        }
    )
    
    task_arns = response['taskArns']
    
    if task_arns:
        response = client.start_task(
            cluster=cluster_name,
            taskDefinition='your_task_definition',
            overrides={},
            containerInstances=[],
            startedBy='EXTERNAL',
            tags={
                tag_key: tag_value
            }
        )
        
        task_arn = response['tasks'][0]['taskArn']
        print(f"Started task: {task_arn}")
    else:
        print("No stopped tasks found.")

def stop_fargate_tasks(cluster_name, tag_key, tag_value):
    client = boto3.client('ecs')
    
    response = client.list_tasks(
        cluster=cluster_name,
        launchType='FARGATE',
        desiredStatus='RUNNING',
        startedBy='EXTERNAL',
        tags={
            tag_key: tag_value
        }
    )
    
    task_arns = response['taskArns']
    
    if task_arns:
        response = client.stop_task(
            cluster=cluster_name,
            task=task_arns[0],
            reason='Stopping task',
            tags={
                tag_key: tag_value
            }
        )
        
        task_arn = response['task']['taskArn']
        print(f"Stopped task: {task_arn}")
    else:
        print("No running tasks found.")

def run_schedule(schedule, cluster_name, tag_key, tag_value):
    print(f"Running schedule: {schedule['name']}")

    tz = pytz.timezone(schedule['timezone'])

    while True:
        now = datetime.datetime.now(tz)
        current_day = now.strftime("%A")
        current_time = now.strftime("%H:%M")

        if current_day in schedule['days'] and current_time == schedule['time']:
            print(f"Starting tasks for schedule: {schedule['name']}")
            start_fargate_tasks(cluster_name, tag_key, tag_value)
            time.sleep(60)  # Aguarda 1 minuto para evitar múltiplas execuções

        if current_day in schedule['days'] and current_time == schedule['end_time']:
            print(f"Stopping tasks for schedule: {schedule['name']}")
            stop_fargate_tasks(cluster_name, tag_key, tag_value)
            time.sleep(60)  # Aguarda 1 minuto para evitar múltiplas execuções

        time.sleep(10)  # Verifica a cada 10 segundos

# Exemplo de uso:
schedules = [
    {
        'name': 'Weekdays',
        'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        'time': '08:00',
        'end_time': '17:00',
        'timezone': 'America/New_York'
    },
    {
        'name': 'Weekends',
        'days': ['Saturday', 'Sunday'],
        'time': '10:00',
        'end_time': '18:00',
        'timezone': 'America/New_York'
    }
]

cluster_name = 'your_cluster_name'
tag_key = 'your_tag_key'
tag_value = 'your_tag_value'

# Executa os agendamentos
for schedule in schedules:
    run_schedule(schedule, cluster_name, tag_key, tag_value)
