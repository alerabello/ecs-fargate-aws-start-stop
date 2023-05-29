import boto3
import datetime
import pytz

def start_cluster(cluster_name, tag_key, tag_value):
    client = boto3.client('ecs')
    
    response = client.list_services(
        cluster=cluster_name,
        launchType='FARGATE',
        desiredStatus='STOPPED',
        tags={
            tag_key: tag_value
        }
    )
    
    service_arns = response['serviceArns']
    
    if service_arns:
        response = client.update_service(
            cluster=cluster_name,
            service=service_arns[0],
            desiredCount=1,
            tags={
                tag_key: tag_value
            }
        )
        
        service_arn = response['service']['serviceArn']
        print(f"Started service: {service_arn}")
    else:
        print("No stopped services found.")

def stop_cluster(cluster_name, tag_key, tag_value):
    client = boto3.client('ecs')
    
    response = client.list_services(
        cluster=cluster_name,
        launchType='FARGATE',
        desiredStatus='ACTIVE',
        tags={
            tag_key: tag_value
        }
    )
    
    service_arns = response['serviceArns']
    
    if service_arns:
        response = client.update_service(
            cluster=cluster_name,
            service=service_arns[0],
            desiredCount=0,
            tags={
                tag_key: tag_value
            }
        )
        
        service_arn = response['service']['serviceArn']
        print(f"Stopped service: {service_arn}")
    else:
        print("No active services found.")

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
    tag_key = 'your_tag_key'
    tag_value = 'your_tag_value'
    
    tz = pytz.timezone('America/New_York')
    current_datetime = datetime.datetime.now(tz)
    current_day = current_datetime.strftime("%A")
    current_time = current_datetime.strftime("%H:%M")
    
    for schedule in schedules:
        if current_day in schedule['days'] and current_time == schedule['time']:
            print(f"Starting cluster and services for schedule: {schedule['name']}")
            start_cluster(cluster_name, tag_key, tag_value)

        if current_day in schedule['days'] and current_time == schedule['end_time']:
            print(f"Stopping cluster and services for schedule: {schedule['name']}")
            stop_cluster(cluster_name, tag_key, tag_value)
    
    return {
        'statusCode': 200,
        'body': 'Schedule executed successfully.'
    }
