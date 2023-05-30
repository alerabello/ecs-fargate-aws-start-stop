import boto3
import datetime
import pytz

def start_service(cluster_name, service_arn):
    client = boto3.client('ecs')
    
    response = client.update_service(
        cluster=cluster_name,
        service=service_arn,
        desiredCount=1
    )
    
    service_arn = response['service']['serviceArn']
    print(f"Started service: {service_arn}")

def stop_service(cluster_name, service_arn):
    client = boto3.client('ecs')
    
    response = client.update_service(
        cluster=cluster_name,
        service=service_arn,
        desiredCount=0
    )
    
    service_arn = response['service']['serviceArn']
    print(f"Stopped service: {service_arn}")

def run_schedule(event, context):
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
    
    tz = pytz.timezone('America/New_York')
    current_datetime = datetime.datetime.now(tz)
    current_day = current_datetime.strftime("%A")
    current_time = current_datetime.strftime("%H:%M")
    
    client = boto3.client('ecs')
    paginator = client.get_paginator('list_services')
    
    for schedule in schedules:
        if current_day in schedule['days'] and current_time == schedule['time']:
            print(f"Starting services for schedule: {schedule['name']}")
            for response in paginator.paginate(cluster=cluster_name):
                service_arns = response['serviceArns']
                for service_arn in service_arns:
                    response = client.describe_services(
                        cluster=cluster_name,
                        services=[service_arn]
                    )
                    tags = response['services'][0].get('tags', {})
                    if tags.get('schedule') == schedule['name']:
                        start_service(cluster_name, service_arn)

        if current_day in schedule['days'] and current_time == schedule['end_time']:
            print(f"Stopping services for schedule: {schedule['name']}")
            for response in paginator.paginate(cluster=cluster_name):
                service_arns = response['serviceArns']
                for service_arn in service_arns:
                    response = client.describe_services(
                        cluster=cluster_name,
                        services=[service_arn]
                    )
                    tags = response['services'][0].get('tags', {})
                    if tags.get('schedule') == schedule['name']:
                        stop_service(cluster_name, service_arn)
    
    return {
        'statusCode': 200,
        'body': 'Schedule executed successfully.'
    }
