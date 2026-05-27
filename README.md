# Loja Verde — Refatoração Guiada por SOLID, Clean Code e Padrões GoF

Projeto desenvolvido para a disciplina de **Padrões e Arquitetura de Software** da PUC-Campinas.

O objetivo deste trabalho foi realizar a refatoração de um sistema legado monolítico aplicando princípios SOLID, práticas de Clean Code e padrões GoF, preservando o comportamento original através de testes automatizados (Golden Master Tests).

---

# Objetivos da Refatoração

O sistema legado original apresentava:

- Forte acoplamento;
- Violação dos princípios SOLID;
- Regras de negócio misturadas com persistência;
- Uso excessivo de condicionais (`if/elif`);
- Duplicação de código;
- Strings mágicas;
- Ausência de separação em camadas;
- Baixa extensibilidade.

A refatoração teve como objetivo transformar o sistema em uma arquitetura modular, extensível e testável.

---

# Arquitetura do Projeto

O projeto foi organizado em camadas explícitas:

```text
src/
├── database/
├── factories/
├── models/
├── observers/
├── repositories/
├── services/
├── strategies/
└── tests/
```

## Responsabilidades das Camadas

| Camada | Responsabilidade |
|---|---|
| `models` | Objetos de domínio e enums |
| `repositories` | Persistência e acesso ao banco |
| `services` | Regras de negócio |
| `strategies` | Algoritmos intercambiáveis |
| `factories` | Criação de objetos |
| `observers` | Sistema de notificações |
| `database` | Infraestrutura SQLite |

---

# Padrões GoF Aplicados

## Strategy

Aplicado para:

- Métodos de pagamento;
- Regras de desconto;
- Desconto progressivo por volume.

Exemplos:

- `CardPaymentProcessor`
- `PixPaymentProcessor`
- `CryptoPaymentProcessor`
- `VolumeDiscountStrategy`

---

## Repository

Aplicado para desacoplar a persistência SQLite das regras de negócio.

Exemplo:

- `OrderRepository`

---

## Observer

Aplicado no sistema de notificações.

Exemplos:

- `EmailNotificationObserver`
- `SmsNotificationObserver`
- `WhatsAppNotificationObserver`

---

## Factory Method

Aplicado para criação de pedidos e composição de notificações.

Exemplos:

- `NormalOrderFactory`
- `VipOrderFactory`
- `CorporateOrderFactory`
- `NotificationFactory`

---

# Extensões Implementadas

## Pagamento em Criptomoeda

Novo método de pagamento com taxa adicional de 2%.

---

## Notificações via WhatsApp

Novo canal de comunicação utilizando Observer.

---

## Desconto Progressivo por Volume

Pedidos com 3 ou mais unidades recebem 15% de desconto adicional.

---

# Tecnologias Utilizadas

- Python 3.12+
- SQLite
- pytest
- mypy
- ruff
- radon

---

# Configuração do Ambiente

## 1. Criar ambiente virtual

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

## 2. Instalar dependências

```bash
pip install -r requirements-dev.txt
```

---

# Execução da Aplicação

```bash
python -m src.main
```

---

# Execução dos Testes

## Executar testes

```bash
pytest
```

---

## Cobertura de testes

```bash
pytest --cov=src --cov-report=term-missing --cov-omit="src/legacy.py,src/main.py"
```

---

## Verificação estática (ruff)

```bash
ruff check .
```

---

## Verificação de tipos (mypy)

```bash
mypy --strict src
```

---

## Complexidade ciclomática (radon)

```bash
radon cc src -s -a
```

---

# Métricas Obtidas

| Métrica | Ferramenta |
|---|---|
| Testes automatizados | pytest |
| Cobertura | coverage.py |
| Lint | ruff |
| Type Checking | mypy |
| Complexidade | radon |

---

# Estrutura de Testes

O projeto utiliza:

- Golden Master Tests;
- Testes unitários;
- Testes de integração;
- Mocking com `unittest.mock`.

---

# Observações

- O arquivo `legacy.py` foi preservado como referência histórica do sistema original.
- A validação principal do projeto ocorre através da suíte automatizada de testes.
- A `main.py` possui caráter demonstrativo, exibindo o fluxo principal da aplicação refatorada.

---

# Autores

Augusto Fidélis dos Santos Custódio
Caio Ribeiro Abrahão
João Pedro Pires de Andrade
Raphael Fernandes de Sellos Moreira  
PUC-Campinas — Engenharia de Software