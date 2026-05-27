# Seção 8 - Análise técnica da refatoração de pagamentos

## Contexto
O legado do sistema concentrava em uma única classe responsabilidades que deveriam estar separadas em camadas distintas. A lógica de criação de pedidos, cálculo de totais, persistência em SQLite, atualização de status e processamento de pagamento estavam acopladas no arquivo `src/legacy.py`. Essa estrutura dificultava a manutenção, ampliava o risco de regressões e violava princípios centrais de projeto orientado a objetos.

## Violações identificadas
### SRP - Single Responsibility Principle
A classe legada acumulava responsabilidades de persistência, regra de negócio, pagamento e notificação. Isso tornava a alteração de qualquer fluxo um ponto de impacto para toda a classe.

### OCP - Open/Closed Principle
O método de pagamento utilizava condicionais explícitas para decidir o comportamento de cartão, PIX e boleto. A introdução de um novo método exigiria alteração direta no fluxo central.

### DIP - Dependency Inversion Principle
O código dependia de implementação concreta e de decisões internas da própria classe, sem abstrações para o processamento de pagamento ou para a persistência.

## Solução aplicada
A refatoração foi conduzida por meio de uma arquitetura em camadas. Os modelos de domínio foram separados em `Order` e `OrderItem`, o contrato de persistência foi definido em uma interface de repositório e a criação de pedidos passou a ser tratada por Factory Method. Para pagamentos, foi aplicado Strategy com injeção de dependência, permitindo variar o comportamento por tipo de pagamento sem modificar o fluxo principal.

## Extensibilidade validada
A extensão de criptomoeda foi adicionada como nova strategy, sem necessidade de alterar as estratégias existentes de cartão, PIX ou boleto. Esse resultado confirma a aplicação prática do princípio OCP. A suíte de testes valida esse comportamento tanto em nível unitário quanto em integração.

## Evidências objetivas
- Suíte de testes: 23 testes aprovados.
- Cobertura total do projeto: 96%.
- Análise estática: `ruff` sem pendências no escopo alterado, `mypy` sem erros no conjunto de arquivos de pagamento e `radon` com complexidade baixa nas classes novas.

## Justificativa de preservação do legado
O arquivo `src/legacy.py` foi preservado como Golden Master para garantir a estabilidade do comportamento histórico. Essa decisão reduz o risco de quebrar a referência esperada pela disciplina e mantém o foco da refatoração na criação da nova arquitetura correta.

## Conclusão
A refatoração da Pessoa 3 demonstra que o comportamento anterior foi preservado enquanto a arquitetura foi evoluída para uma solução mais modular, extensível e testável. As mudanças resolvem os principais problemas de acoplamento do fluxo de pagamento e criam base sólida para futuras extensões sem regressão de comportamento.
