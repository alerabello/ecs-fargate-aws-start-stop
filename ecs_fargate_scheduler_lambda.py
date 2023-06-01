current_time = datetime.now() - timedelta(hours=3)
current_time_local = current_time.strftime("%H:%M")
print(f'Current time: {current_time_local}')

current_day = current_time.strftime("%A")
print(f'Current day: {current_day}')
	
response = ecs.list_clusters()
cluster_arns = response['clusterArns']

stop_tasks = []   
start_tasks = []

for cluster_arn in cluster_arns:
    response = ecs.list_tasks(cluster=cluster_arn)
    task_arns = response['taskArns']
    
    for task_arn in task_arns:
        response = ecs.describe_tasks(cluster=cluster_arn, tasks=[task_arn])
        task = response['tasks'][0]
        task_definition_arn = task['taskDefinitionArn']
        
        response = ecs.describe_task_definition(taskDefinition=task_definition_arn)
        task_definition = response['taskDefinition']
        tags = task_definition['tags']
        
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
                                    print(f'{task_arn} is on the time')
                                    stop_tasks.append(task_arn)
                        except ValueError:
                            print(f'{current_day} is not on Stop period-{period[j]}')
                    else:
                        if current_day == day[0]:
                            if tag['value'] == current_time_local:
                                print(f'{task_arn} is on the time')
                                stop_tasks.append(task_arn)
            
            for tag in tags:
                # Add task in array to start
                if tag['key'] == 'ScheduleStart-' + str(period[j]):
                    if len(day) > 1:
                        # Check if the current day is within the period
                        try:
                            if DAYS.index(current_day, DAYS.index(day[0]), DAYS.index(day[1]) + 1):
                                print(f'{current_day} is on Start period-{period[j]}')
                                if tag['value'] == current_time_local:
                                    print(f'{task_arn} is on the time')
                                    start_tasks.append(task_arn)
                        except ValueError:
                            print(f'{current_day} is not on Start period-{period[j]}')
                    else:
                        if current_day == day[0]:
                            if tag['value'] == current_time_local:
                                print(f'{task_arn} is on the time')
                                start_tasks.append(task_arn)
            
            j = j+1
        
# Stop all tasks tagged to stop.
if len(stop_tasks) > 0:
    for stop_task in stop_tasks:
        response = ecs.stop_task(cluster=cluster_arn, task=stop_task)
        print(f'Stopping task: {stop_task}')
else:
    print("No tasks to stop.")
    
# Start tasks tagged to start. 
if len(start_tasks) > 0:
    for start_task in start_tasks:
        response = ecs.start_task(cluster=cluster_arn, taskDefinition=task_definition_arn)
        print(f'Starting task: {start_task}')
else:
    print("No tasks to start.")