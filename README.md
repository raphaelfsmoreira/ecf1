# ECF1 - Refatoração de Pedidos e Pagamentos

Projeto de refatoração para a disciplina de Padrões e Arquitetura de Software.

## Requisitos

- Python 3.11 ou superior

## Instalação

```bash
python -m pip install -r requirements.txt
```

Para instalar também as ferramentas que ajudam a revisar o código:

```bash
python -m pip install -r requirements-dev.txt
```

## Execução dos testes

```bash
python -m pytest -q
```

## Revisões do código

Esses comandos servem para conferir se o projeto está em boas condições antes de entregar:

```bash
python -m ruff check src tests
python -m mypy --ignore-missing-imports src/models/order.py src/models/order_item.py src/models/enums.py src/services/payment_processor.py src/services/payment_strategies.py src/services/payment_processor_factory.py src/services/order_service.py src/repositories/order_repository_interface.py src/repositories/sqlite_order_repository.py src/factories/order_factory.py
python -m radon cc src -s
python -m radon mi src
python -m coverage run -m pytest -q
python -m coverage report -m
```

## Estrutura

- `src/legacy.py`: comportamento legado usado como Golden Master
- `src/factories`: factories para criação de pedidos
- `src/models`: modelos de domínio
- `src/repositories`: contrato e implementação SQLite do repositório
- `src/services`: serviço de pedidos e estratégia de pagamentos
- `tests/golden_master`: testes de comportamento legado
- `tests/unit`: testes unitários da arquitetura nova
- `tests/integration`: testes de integração de pagamento

## Observações

- O arquivo `loja.db` é criado localmente quando o sistema é executado e está ignorado no Git.
- O projeto mantém o legado como referência de comportamento e testa a nova arquitetura separadamente.
# ECF1: Refatoração Guiada por SOLID, Clean Code e GoF.
--
