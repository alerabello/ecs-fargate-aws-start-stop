import boto3
import datetime

def start_service(cluster_name, service_name):
    client = boto3.client('ecs')
    response = client.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=1
    )
    print(f"Started service: {service_name}")

def stop_service(cluster_name, service_name):
    client = boto3.client('ecs')
    response = client.update_service(
        cluster=cluster_name,
        service=service_name,
        desiredCount=0
    )
    print(f"Stopped service: {service_name}")

def lambda_handler(event, context):
    cluster_name = 'your_cluster_name'  # Substitua pelo nome do seu cluster ECS Fargate
    client = boto3.client('ecs')
    
    response = client.list_services(
        cluster=cluster_name
    )
    
    service_arns = response['serviceArns']
    
    for service_arn in service_arns:
        service_name = service_arn.split('/')[1]
        
        response = client.describe_services(
            cluster=cluster_name,
            services=[service_arn]
        )
        
        service_tags = response['services'][0].get('tags', {})
        
        schedule_start = service_tags.get('ScheduleStart', '')
        schedule_stop = service_tags.get('ScheduleStop', '')
        start_time = service_tags.get('StartTime', '')
        stop_time = service_tags.get('StopTime', '')
        
        current_day = datetime.datetime.now().strftime('%A')
        current_time = datetime.datetime.now().strftime('%H:%M')
        
        if current_day in schedule_start and current_time == start_time:
            start_service(cluster_name, service_name)
        
        if current_day in schedule_stop and current_time == stop_time:
            stop_service(cluster_name, service_name)
    
    return {
        'statusCode': 200,
        'body': 'Scheduled start/stop executed successfully.'
    }
