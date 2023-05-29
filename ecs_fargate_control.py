import boto3

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

# Exemplo de uso:
cluster_name = 'your_cluster_name'
tag_key = 'your_tag_key'
tag_value = 'your_tag_value'

# Iniciando as tarefas do Fargate com base nas tags
start_fargate_tasks(cluster_name, tag_key, tag_value)

# Parando as tarefas do Fargate com base nas tags
stop_fargate_tasks(cluster_name, tag_key, tag_value)
