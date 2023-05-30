# Script Python para ligar e desligar serviços do Amazon ECS Fargate através de tags com base em dias e horários - AWS Lambda

Este script Python pode ser executado no AWS Lambda para ligar e desligar serviços do Amazon ECS Fargate com base em tags, considerando diferentes dias e horários. Ele usa a biblioteca boto3 para se comunicar com a AWS e executar as operações no ECS.

## Requisitos

- Uma conta da AWS configurada com permissões para executar operações no Amazon ECS
- Configuração de função e política adequadas para o AWS Lambda
- Python 3.x

## Configuração

1. Crie uma função Lambda na AWS e atribua uma política que forneça as permissões necessárias para acessar e modificar os serviços do Amazon ECS. Para obter mais informações, consulte a documentação oficial da AWS sobre como criar funções Lambda e atribuir políticas.

2. Faça o upload do código do script Python (`ecs_fargate_scheduler_lambda.py`) para a função Lambda. Você pode fazer isso por meio da interface da AWS ou usando a AWS CLI.

3. Edite o arquivo `ecs_fargate_scheduler_lambda.py` e substitua os seguintes valores:

   - `your_cluster_name`: Substitua pelo nome do seu cluster ECS Fargate.

4. Defina os agendamentos no script, na variável `schedules`. Cada agendamento é definido como um dicionário contendo as seguintes informações:
   
   - `name`: Nome do agendamento.
   - `days`: Uma lista de dias da semana em que o agendamento deve ser aplicado.
   - `time`: Horário de início em que os serviços serão iniciados (no formato 'HH:MM').
   - `end_time`: Horário de término em que os serviços serão interrompidos (no formato 'HH:MM').
   - `timezone`: Fuso horário em que o agendamento será aplicado (por exemplo, 'America/New_York').

5. Certifique-se de que as tags `schedule` estejam atribuídas corretamente aos serviços que deseja controlar. Por exemplo, você pode adicionar uma tag com a chave `schedule` e o valor correspondente ao nome do agendamento que deseja aplicar.

## Executando as Rotinas

1. Configure um evento de agendamento para a função Lambda no AWS CloudWatch Events. O evento de agendamento deve ser definido para acionar a função Lambda em intervalos regulares, de acordo com a frequência desejada (por exemplo, a cada minuto, hora ou dia).

2. Salve as configurações e aguarde o acionamento do evento de agendamento. A função Lambda executará as rotinas de ligar e desligar os serviços do Amazon ECS Fargate com base nos agendamentos definidos.

3. Os logs da função Lambda podem ser visualizados no Console de Gerenciamento da AWS ou por meio da AWS CLI.

Observação: Certifique-se de que as tags e o cluster estejam configurados corretamente antes de executar o script. Certifique-se também de ter as permissões necessárias para acessar e modificar os serviços do ECS Fargate em sua conta da AWS.

Lembre-se de substituir 'your_cluster_name' pelo nome correto do seu cluster ECS Fargate. Além disso, certifique-se de que as tags schedule estejam atribuídas corretamente aos serviços que deseja controlar.