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
            
            period = []
            i = 0
            j = 0

            for tag in tags:
                if 'Period' in tag['key']:
                    period.append(tag['key'].split('-')[1])
                    i = i+1
                
            while j < i:
                for tag in tags:
                    # Get Period tag value
                    if tag['key'] == 'Period-' + str(period[j]):
                        numPeriod = tag['value']
                        print(f'Period: {numPeriod}')
                        day = numPeriod.split('-')
                        print(f'Days: {day}')

                for tag in tags:
                    # Add task in array to stop
                    if tag['key'] == 'ScheduleStop-' + str(period[j]):
                        if len(day) > 1:
                            # Check if the current day is within the period
                            try:
                                if DAYS.index(current_day, DAYS.index(day[0]), DAYS.index(day[1]) + 1):
                                    print(f'{current_day} is on Stop period-{period[j]}')
                                    
                                    if tag['value'] == current_time_local:
                                        print(f'{task_definition} is on the time')
                                        stop_tasks.append(task)
                                        
                            except ValueError:
                                print(f'{current_day} is not on Stop period-{period[j]}')
                        else:
                            if current_day == day[0]:
                                if tag['value'] == current_time_local:
                                    print(f'{task_definition} is on the time')
                                    stop_tasks.append(task)
            
                for tag in tags:
                    # Add task in array to start
                    if tag['key'] == 'ScheduleStart-' + str(period[j]):
                        if len(day) > 1:
                            # Check if the current day is within the period
                            try:
                                if DAYS.index(current_day, DAYS.index(day[0]), DAYS.index(day[1]) + 1):
                                    print(f'{current_day} is on Start period-{period[j]}')
                                    
                                    if tag['value'] == current_time_local:
                                        print(f'{task_definition} is on the time')
                                        start_tasks.append(task)
                                            
                            except ValueError:
                                print(f'{current_day} is not on Start period-{period[j]}')
                        else:
                            if current_day == day[0]:
                                if tag['value'] == current_time_local:
                                    print(f'{task_definition} is on the time')
                                    start_tasks.append(task)
            
                j = j+1
            
    # Stop all tasks tagged to stop.
    if len(stop_tasks) > 0:
        for stop_task in stop_tasks:
            response = ecs.stop_task(cluster=cluster, task=stop_task)
            print(f'Stopping task: {stop_task}')
    else:
        print("No tasks to stop.")
        
    # Start tasks tagged to start. 
    if len(start_tasks) > 0:
        for start_task in start_tasks:
            response = ecs.start_task(cluster=cluster, task=start_task)
            print(f'Starting task: {start_task}')
    else:
        print("No tasks to start.")
