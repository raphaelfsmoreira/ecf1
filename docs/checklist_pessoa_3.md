# Checklist final - Pessoa 3 (Pagamentos)

## Implementação
- [x] Criar Strategy para pagamento.
- [x] Implementar cartão, PIX, boleto e criptomoeda.
- [x] Aplicar injeção de dependência no serviço de pagamento.
- [x] Implementar repositório SQLite concreto.
- [x] Manter o Golden Master do legado como referência.

## Testes
- [x] Testes unitários para cartão, PIX, boleto e crypto.
- [x] Teste de integração para crypto com repositório real.
- [x] Suíte completa executada com sucesso.
- [x] Cobertura total registrada em 96%.

## Qualidade
- [x] `ruff` executado e corrigido no escopo alterado.
- [x] `mypy` executado sem erros no escopo de pagamento.
- [x] `radon` executado e registrado no log.
- [x] Log técnico atualizado com decisões e evidências.

## Documentação para o PDF
- [x] Registrar violações encontradas no legado.
- [x] Registrar solução arquitetural adotada.
- [x] Registrar evidência de extensibilidade com crypto.
- [x] Registrar métricas de testes, cobertura e análise estática.
- [x] Explicar a decisão de preservar `legacy.py` como baseline.