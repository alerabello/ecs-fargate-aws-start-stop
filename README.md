### Função Lambda para iniciar/parar tarefas em diversos clusters Fargate AWS

Este é um exemplo de uma função Lambda que utiliza o AWS SDK para iniciar ou parar tarefas em diversos clusters Fargate da AWS, com agendamento externo usando tags nos serviços do cluster.

#### Pré-requisitos
- Uma conta na AWS com permissões para criar e executar funções Lambda, além de acessar o serviço ECS e CloudWatch Events.
- Python 3.7 ou superior instalado em seu ambiente de desenvolvimento.
- A biblioteca boto3 instalada. Você pode instalá-la usando o comando `pip install boto3`.

#### Configuração
1. Faça o login na AWS Management Console.
2. Crie uma nova função Lambda e atribua a ela as permissões necessárias para acessar o serviço ECS e CloudWatch Events.
3. Copie e cole o código fornecido na função Lambda.
4. Salve e implante a função Lambda.

#### Agendamento
Você pode usar um agendador externo, como o CloudWatch Events, para invocar a função Lambda nos horários e dias desejados. Neste exemplo, a função Lambda só será executada nos dias úteis das 08:00 às 20:00 para iniciar as tarefas, e nos fins de semana das 10:00 às 18:00 para parar as tarefas.

#### Uso
1. Certifique-se de ter o Python instalado em sua máquina..
2. Instale a biblioteca boto3 executando o seguinte comando em seu terminal: pip install boto3
3. Copie o código da função para um arquivo com extensão .py, por exemplo, ecs_service_scheduler.py.
4. Configure suas credenciais de acesso à AWS usando o AWS CLI executando o seguinte comando em seu terminal
5. Abra o arquivo ecs_service_scheduler.py em um editor de texto e atualize 'your_cluster_name' e 'your_service_name' com os valores corretos.
6. Adicione as tags de programação do serviço ECS desejado na variável schedule_tags, conforme mostrado no exemplo.
7. Execute o arquivo Python em seu terminal usando o seguinte comando: python ecs_service_scheduler.py

##### Exemplo de evento para iniciar as tarefas nos dias úteis das 08:00 às 20:00

```json
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
```
Certifique-se de substituir 'chamada-iniciar' e 'chamada-parar' pelas tags reais que você deseja usar para identificar os serviços que devem ser iniciados ou parados.

1. A função Lambda verificará os clusters e serviços do ECS e iniciará ou parará as tarefas nos serviços que possuem as tags especificadas, apenas durante os horários e dias úteis definidos.
Considerações finais
2. Este exemplo fornece uma base para criar uma função Lambda que inicia ou para tarefas em diversos clusters Fargate da AWS, usando o AWS SDK e agendamento externo com tags nos serviços do cluster. Certifique-se de ajustar o código de acordo com suas necessidades específicas, como lidar com erros, configurar logs e adicionar segurança adicional.

Para mais informações sobre como trabalhar com a AWS Lambda, consulte a [documentação oficial da AWS](https://docs.aws.amazon