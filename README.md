### Função Lambda para iniciar/parar tarefas em diversos clusters Fargate AWS

Este é um exemplo de função AWS Lambda escrita em Python que atualiza os serviços do Amazon ECS com base em um cronograma predefinido. Os serviços podem ser iniciados e parados em determinados períodos do dia e dias da semana, permitindo um controle automatizado das tarefas em execução.

#### Pré-requisitos
- Uma conta da AWS com acesso ao serviço Amazon ECS.
- O nome do seu cluster Amazon ECS.
- Os nomes dos serviços Amazon ECS que deseja atualizar.
- As credenciais adequadas configuradas para acessar os serviços da AWS.

#### Configuração
1. Crie uma nova função AWS Lambda.
2. Selecione a linguagem Python como o ambiente de execução.
3. Copie o código fornecido e cole-o no editor de código da função Lambda.
4. Substitua 'nome-do-cluster' pelo nome do seu cluster Amazon ECS.
5. Substitua ['service1', 'service2', 'service3', 'service4'] pelos nomes dos seus serviços Amazon ECS.
6. Personalize o mapeamento dos períodos e horários de início/parada de acordo com suas necessidades. Você pode adicionar, remover ou ajustar os períodos e os horários definidos no dicionário schedule.
7. Salve a função Lambda.

#### Uso
A função Lambda pode ser acionada de várias maneiras, mas uma opção comum é agendá-la com o Amazon CloudWatch Events para executar em intervalos regulares.

1. Crie uma nova regra de evento no Amazon CloudWatch Events.
2. Configure a regra de evento para acionar a função Lambda em um cronograma desejado (por exemplo, a cada 5 minutos, a cada hora, etc.).
3. Salve a regra de evento.

A função Lambda será executada de acordo com o cronograma definido e atualizará os serviços do Amazon ECS com base no estado atual do tempo.

##### Observações

1. Certifique-se de ter as permissões adequadas atribuídas à função Lambda para acessar e atualizar os serviços do Amazon ECS.
2. Monitore os registros da função Lambda para obter informações sobre as atualizações dos serviços.
3. Realize testes e validações adequados antes de implantar a função Lambda em um ambiente de produção.

##### Contribuição
Sinta-se à vontade para contribuir com melhorias para este exemplo de função Lambda. Abra um problema ou envie uma solicitação de pull para discutir e propor suas alterações.

##### Licença
Este exemplo de código é fornecido sob a licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.

##### ESTE É UM SCRITP TESTE, TENHA CUIDADO, EXECUTE SEMPRE NO AMBIENTE DEV / HML, VALIDE SEMPRE.
