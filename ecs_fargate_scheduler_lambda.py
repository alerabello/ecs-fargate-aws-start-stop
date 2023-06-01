import boto3
import time
from datetime import datetime, timedelta

# Define Fargate client connection
ecs = boto3.client('ecs')

DAYS = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday'
]

def lambda_handler(event, context):

    current_time = datetime.now() - timedelta(hours=3)
    current_time_local = current_time.strftime("%H:%M")
    print(f'Current time: {current_time_local}')
    
    current_day = current_time.strftime("%A")
    print(f'Current day: {current_day}')
    	
    response = ecs.list_clusters()
    clusters = response['clusterArns']
    
    stop_tasks = []   
    start_tasks = []

    for cluster in clusters:
        response = ecs.list_tasks(cluster=cluster)
        tasks = response['taskArns']
        
        for task in tasks:
            task_details = ecs.describe_tasks(cluster=cluster, tasks=[task])
            task_definition = task_details['tasks'][0]['taskDefinitionArn']
            
            tags_response = ecs.list_tags_for_resource(resourceArn=task_definition)
            tags = tags_response['tags']
            
            periods = []
            
            for key in tags:
                if key.startswith('Period-'):
                    periods.append(key.split('-')[1])
            
            for period in periods:
                schedule_start = tags.get(f'ScheduleStart-{period}', '')
                schedule_stop = tags.get(f'ScheduleStop-{period}', '')
                
                if current_day == 'Monday' or current_day == 'Tuesday' or current_day == 'Wednesday' or current_day == 'Thursday' or current_day == 'Friday':
                    if current_time_local == schedule_start:
                        start_tasks.append(task)
                    elif current_time_local == schedule_stop:
                        stop_tasks.append(task)
                elif current_day == 'Saturday':
                    if period == '2' and current_time_local == schedule_start:
                        start_tasks.append(task)
                elif current_day == 'Sunday':
                    if period == '3' and current_time_local == schedule_stop:
                        stop_tasks.append(task)
            
    # Stop all tasks tagged to stop.
    if len(stop_tasks) > 0:
        for task in stop_tasks:
            response = ecs.stop_task(cluster=cluster, task=task)
            print(f'Stopping task: {task}')
    else:
        print("No tasks to stop.")
        
    # Start tasks tagged to start. 
    if len(start_tasks) > 0:
        for task in start_tasks:
            response = ecs.start_task(cluster=cluster, task=task)
            print(f'Starting task: {task}')
    else:
        print("No tasks to start.")
