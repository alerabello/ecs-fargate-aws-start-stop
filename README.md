# Automatização de Start/Stop de serviços ECS Fargate no AWS Lambda

Este é um script em Python que pode ser executado no AWS Lambda para automatizar as operações de start e stop em serviços do ECS Fargate com base em tags definidas nos serviços.

## Requisitos

- Pré-requisitos:

- Uma conta na AWS com acesso ao serviço ECS e permissões para criar e executar funções Lambda.
- Um cluster ECS Fargate configurado com os serviços que deseja controlar.
- Tags corretamente configuradas nos serviços do ECS Fargate, conforme descrito abaixo.

## Configuração

1. Passos para configurar a rotina de start/stop:

2. Abra o Console de Gerenciamento da AWS e acesse o serviço ECS (Amazon Elastic Container Service).

3. Crie um cluster ECS Fargate, caso ainda não tenha um. Siga as instruções fornecidas na documentação oficial da AWS para criar um cluster ECS Fargate.

4. Crie ou selecione os serviços ECS Fargate que deseja controlar com a rotina de start/stop. Certifique-se de que os serviços estejam associados ao cluster ECS Fargate.

5. Para cada serviço que deseja controlar, adicione as seguintes tags:

Chave: ScheduleStart
Valor: Especifique os dias da semana em que o serviço deve ser iniciado, separados por vírgulas. Por exemplo: Monday,Tuesday,Wednesday.
Chave: ScheduleStop
Valor: Especifique os dias da semana em que o serviço deve ser interrompido, separados por vírgulas. Por exemplo: Thursday,Friday.
Chave: StartTime
Valor: Especifique o horário de início no formato HH:MM. Por exemplo: 08:00.
Chave: StopTime
Valor: Especifique o horário de término no formato HH:MM. Por exemplo: 18:00.
Crie uma função Lambda no Console de Gerenciamento da AWS:

6. Selecione a linguagem de programação Python e escolha um nome para a função Lambda.
7. Cole o código fornecido neste repositório na função Lambda.
8. Configure as permissões adequadas para a função Lambda, garantindo que ela tenha acesso ao cluster ECS Fargate e permissões para modificar os serviços. Recomenda-se criar uma função de execução do IAM com as permissões necessárias e associá-la à função Lambda.
9. Crie um evento no CloudWatch para acionar a função Lambda de acordo com o cronograma desejado:

10. No Console de Gerenciamento da AWS, acesse o serviço CloudWatch.
11. Crie uma regra de evento para acionar a função Lambda com base no cronograma desejado. Por exemplo, a cada hora ou de acordo com um cronograma específico.
12. Após configurar a função Lambda e o evento no CloudWatch, a rotina de start/stop será executada automaticamente com base nas tags e no cronograma definidos nos serviços do ECS Fargate.

13. Certifique-se de que o código foi atualizado com o nome correto do seu cluster ECS Fargate, substituindo 'your_cluster_name' pelo nome correto.

14. Observação: Este script considera o uso do AWS SDK para Python (boto3) e assume que você já configurou as credenciais adequadas no ambiente onde a função Lambda será executada.

15. Espero que este guia seja útil para configurar a rotina de start/stop automatizada para serviços ECS Fargate no AWS Lambda!