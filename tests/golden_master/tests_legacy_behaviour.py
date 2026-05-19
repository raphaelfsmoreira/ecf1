# Código sugerido extraído da documentação do trabalho

# Lembrando que o Golden Master Test são os testes de referência do código legado.
# Eles servirão como referência póestuma para quando a refatoração for concluída.
# A partir do código refatorado, consulta-se os Golden Masters e pergunta... Essa funcionalidade está funcionando como antes?

import pytest
from src.legacy import Sis

@pytest.fixture
def sis(tmp_path, monkeypatch):
    """ Isola o banco em diretorio temporario por teste"""
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()

# Iniciando os casos de happy paths (caminhos felizes, em que o fluxo das atividades é o normal e esperado).
#>>>>>>>>>>>>>>>>>>>>> HAPPY PATHS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# FLUXO DE COMPRA PARA UM PEDIDO NORMAL
# Caracteriza o comportamento atual do código legado ao criar um pedido normal.
#
# Cenário:
# - 2 unidades de produto1, tipo normal: 100 * 2 = 200
# - 1 unidade de produto2, tipo desc10: 50 * 1 * 0.9 = 45
# - Total esperado: 245
#
# O teste verifica:
# - se o pedido foi salvo corretamente;
# - se o total foi calculado conforme a regra atual;
# - se o status inicial é "pendente";
# - se os itens foram persistidos e recuperados;
# - se a mensagem de email foi impressa.
def test_pedido_normal_calcula_total_status_e_saida(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')
    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['cli'] == 'Joao Silva'
    assert pedido['tot'] == pytest.approx(245.0)
    assert pedido['st'] == 'pendente'
    assert pedido['tp'] == 'normal'
    assert pedido['itens'] == itens
    assert "Email enviado para Joao Silva: Pedido recebido!" in saida

# FLUXO DE COMPRA PARA UM PEDIDO VIP
#
# Cenário:
# - 1 unidade de produto3, tipo desc20: 200 * 1 * 0.8 = 160
# - Cliente VIP recebe 5% de desconto global: 160 * 0.95 = 152
# - Total esperado: 152
#
# O teste verifica:
# - cálculo do desconto do item;
# - cálculo do desconto VIP;
# - status inicial;
# - persistência dos dados;
# - notificações específicas do cliente VIP.
def test_pedido_vip_calcula_total_status_e_saida(sis, capsys):
    itens = [
        {'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}
    ]

    id_ped = sis.add_ped('Maria Santos', itens, 'vip')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['cli'] == 'Maria Santos'
    assert pedido['tot'] == pytest.approx(152.0)
    assert pedido['st'] == 'pendente'
    assert pedido['tp'] == 'vip'
    assert pedido['itens'] == itens

    assert "Email enviado para Maria Santos: Pedido recebido!" in saida
    assert "SMS enviado para Maria Santos: Pedido VIP recebido!" in saida


# FLUXO DE COMPRA PARA UM PEDIDO CORPORATIVO
#
# Cenário:
# - 5 unidades de produto1: 100 * 5 = 500
# - Cliente corporativo recebe 10% de desconto global
# - Total esperado: 450
#
# O teste verifica:
# - cálculo do desconto corporativo;
# - status inicial;
# - persistência dos dados;
# - notificações específicas do tipo corporativo.
def test_pedido_corporativo_calcula_total_status_e_saida(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 5, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Empresa XYZ', itens, 'corporativo')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['cli'] == 'Empresa XYZ'
    assert pedido['tot'] == pytest.approx(450.0)
    assert pedido['st'] == 'pendente'
    assert pedido['tp'] == 'corporativo'
    assert pedido['itens'] == itens

    assert "Email enviado para Empresa XYZ: Pedido recebido!" in saida
    assert "Notificação enviada ao gerente de conta de Empresa XYZ" in saida



#>>>>>>>>>>>>>>>>>>>>>>>> TESTES DE PAGAMENTOS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# FLUXOS DE TESTE PARA PAGAMENTOS

# FLUXO DE PAGAMENTO VIA BOLETO
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O pagamento é realizado via boleto
#
# O teste verifica:
# - se o metodo retorna True;
# - se o boleto é gerado;
# - se o status do pedido permanece "pendente";
# - se as mensagens corretas são exibidas.
#
# OBS:
# No comportamento atual do legado, pagamentos via boleto
# NÃO aprovam automaticamente o pedido.
def test_pagamento_boleto_gera_boleto_mas_nao_aprova_pedido(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    resultado = sis.proc_pag(id_ped, 'boleto', 100)

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert resultado is True
    assert pedido['st'] == 'pendente'

    assert "Gerando boleto..." in saida
    assert "Boleto gerado!" in saida

# Lembrando que apenas o boleto tem o estado intermediario de pedido pendente.
# Pedidos via pix e cartão aprovam imediatamente.

# FLUXO DE PAGAMENTO VIA PIX
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O pagamento é realizado via PIX
#
# O teste verifica:
# - se o metodo retorna True;
# - se o QR Code PIX é gerado;
# - se o pagamento é confirmado;
# - se o status do pedido muda para "aprovado";
# - se as mensagens corretas são exibidas.
def test_pagamento_pix_aprova_pedido(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    resultado = sis.proc_pag(id_ped, 'pix', 100)

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert resultado is True
    assert pedido['st'] == 'aprovado'

    assert "Gerando QR Code PIX..." in saida
    assert "PIX recebido!" in saida
    assert "Pedido aprovado!" in saida

# FLUXO DE PAGAMENTO VIA CARTAO
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O pagamento é realizado via cartão
#
# O teste verifica:
# - se o metodo retorna True;
# - se o cartão é validado;
# - se o pedido é aprovado;
# - se o status muda para "aprovado";
# - se as mensagens corretas são exibidas.
def test_pagamento_cartao_aprova_pedido(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    resultado = sis.proc_pag(id_ped, 'cartao', 100)

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert resultado is True
    assert pedido['st'] == 'aprovado'

    assert "Processando pagamento com cartao..." in saida
    assert "Cartao validado!" in saida
    assert "Pedido aprovado!" in saida


# EXCEÇÃO: TESTE PARA VALOR INSUFICIENTE NA TRANSAÇÃO DE UMA COMPRA.
# Ele cria o pedido add_ped e o deixa como pendente.
# Porém, ao processar o pagamento, o valor passado como parâmetro (99) é menor do que o subtotal da compra (100).
# Isso deve retornar False do metdo proc_pag (em resultado) e o print de Valor Insuficiente.
# Além disso, o status do pedido deve continuar como pendente.
def test_pagamento_insuficiente_nao_aprova(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')
    resultado = sis.proc_pag(id_ped, 'cartao', 99)

    pedido = sis.get_ped(id_ped)
    saida = capsys.readouterr().out

    assert resultado is False
    assert pedido['st'] == 'pendente'
    assert "Valor insuficiente!" in saida

# EXCEÇÃO: FLUXO DE PAGAMENTO COM METODO INVALIDO
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O usuário tenta pagar utilizando um metodo inexistente
#
# O teste verifica:
# - se o pagamento falha;
# - se o metodo retorna False;
# - se o status do pedido permanece "pendente";
# - se a mensagem de erro correta é exibida.
def test_pagamento_com_metodo_invalido_nao_aprova_pedido(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    resultado = sis.proc_pag(id_ped, 'bitcoin', 100)

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert resultado is False
    assert pedido['st'] == 'pendente' # Pedido permanece com status pendente
    assert "Metodo de pagamento invalido!" in saida # Retorno do print como inválido

#>>>>>>>>>>>>>>>>>>>>>> TESTES DE ESTOQUE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# VALIDAÇÃO DE ESTOQUE COM SUCESSO
#
# Cenário:
# - Todos os produtos existem no estoque
# - As quantidades solicitadas estão disponíveis
#
# O teste verifica:
# - se o metodo retorna True.
def test_validar_estoque_com_sucesso(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'}
    ]

    resultado = sis.validar_estoque(itens)

    assert resultado is True

# VALIDAÇÃO DE ESTOQUE COM PRODUTO INEXISTENTE
#
# Cenário:
# - Um item possui nome que não existe no estoque interno
#
# O teste verifica:
# - se o metodo retorna False;
# - se a mensagem correta é exibida.
def test_validar_estoque_produto_inexistente(sis, capsys):
    itens = [
        {'nome': 'produto999', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    resultado = sis.validar_estoque(itens)

    saida = capsys.readouterr().out

    assert resultado is False
    assert "Produto produto999 nao encontrado!" in saida


# VALIDAÇÃO DE ESTOQUE INSUFICIENTE
#
# Cenário:
# - O produto existe no estoque
# - Mas a quantidade solicitada é maior do que a disponível
#
# Estoque legado:
# - produto1: 100 unidades
#
# O teste verifica:
# - se o metodo retorna False;
# - se a mensagem correta é exibida.
def test_validar_estoque_quantidade_insuficiente(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 101, 'tipo': 'normal'}
    ]

    resultado = sis.validar_estoque(itens)

    saida = capsys.readouterr().out

    assert resultado is False
    assert "Estoque insuficiente para produto1!" in saida

#>>>>>>>>>>>>>>>>>>>>>> TESTES DE ATUALIZAÇÃO DE STATUS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# ATUALIZAÇÃO DE STATUS PARA APROVADO
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O status do pedido é atualizado manualmente para "aprovado"
#
# O teste verifica:
# - se o status foi atualizado no banco;
# - se o email de aprovação foi enviado;
# - se o comportamento atual do legado permanece consistente.
def test_atualizar_status_para_aprovado(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    # Limpa a saída anterior do add_ped()
    capsys.readouterr()

    sis.upd_st(id_ped, 'aprovado')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'aprovado'
    assert "Email enviado para Joao Silva: Pedido aprovado!" in saida


# ATUALIZAÇÃO DE STATUS PARA ENVIADO
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O status do pedido é atualizado para "enviado"
#
# O teste verifica:
# - se o status foi atualizado;
# - se o email de envio foi exibido corretamente.
def test_atualizar_status_para_enviado(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    # Limpa prints anteriores do fluxo de criação
    capsys.readouterr()

    sis.upd_st(id_ped, 'enviado')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'enviado'
    assert "Email enviado para Joao Silva: Pedido enviado!" in saida


# ATUALIZAÇÃO DE STATUS PARA ENTREGUE (CLIENTE NORMAL)
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O status do pedido é atualizado para "entregue"
#
# O teste verifica:
# - se o status foi atualizado;
# - se o email de entrega foi exibido;
# - se clientes normais NÃO recebem pontuação especial.
def test_atualizar_status_para_entregue_cliente_normal(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    # Remove saída anterior do add_ped()
    capsys.readouterr()

    sis.upd_st(id_ped, 'entregue')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'entregue'
    assert "Email enviado para Joao Silva: Pedido entregue!" in saida

# ATUALIZAÇÃO DE STATUS PARA ENTREGUE (CLIENTE VIP)
#
# Cenário:
# - Um pedido VIP é criado corretamente
# - O status é atualizado para "entregue"
#
# Regras atuais do legado:
# - Clientes VIP recebem o dobro de pontos do total do pedido
# - Total esperado do pedido: 152
# - Pontos esperados: int(152 * 2) = 304
#
# O teste verifica:
# - se o status foi atualizado;
# - se o email de entrega foi exibido;
# - se a pontuação VIP foi calculada corretamente.
def test_atualizar_status_entregue_vip_gera_pontos_dobrados(sis, capsys):
    itens = [
        {'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}
    ]

    id_ped = sis.add_ped('Maria Santos', itens, 'vip')

    # Limpa prints anteriores
    capsys.readouterr()

    sis.upd_st(id_ped, 'entregue')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'entregue'
    assert "Email enviado para Maria Santos: Pedido entregue!" in saida
    assert "Cliente VIP ganhou 304 pontos!" in saida

# ATUALIZAÇÃO DE STATUS PARA ENTREGUE (CLIENTE CORPORATIVO)
#
# Cenário:
# - Um pedido corporativo é criado corretamente
# - O status é atualizado para "entregue"
#
# Regras atuais do legado:
# - Clientes corporativos recebem 1.5x pontos
# - Total esperado do pedido: 450
# - Pontos esperados: int(450 * 1.5) = 675
#
# O teste verifica:
# - se o status foi atualizado;
# - se o email de entrega foi exibido;
# - se a pontuação corporativa foi calculada corretamente.
def test_atualizar_status_entregue_corporativo_gera_pontos_um_e_meio(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 5, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Empresa XYZ', itens, 'corporativo')

    # Remove prints anteriores
    capsys.readouterr()

    sis.upd_st(id_ped, 'entregue')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'entregue'
    assert "Email enviado para Empresa XYZ: Pedido entregue!" in saida
    assert "Cliente corporativo ganhou 675 pontos!" in saida

# ATUALIZAÇÃO PARA STATUS DESCONHECIDO
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O sistema recebe um status não previsto nas regras de negócio
#
# Comportamento atual do legado:
# - O status é salvo mesmo sendo inválido/desconhecido
# - O fluxo cai no bloco "else"
# - O cliente recebe pontos equivalentes ao total do pedido
#
# O teste verifica:
# - se o status arbitrário foi salvo;
# - se a pontuação padrão foi aplicada;
# - se o comportamento atual do legado foi preservado.
def test_atualizar_status_desconhecido_gera_pontos_normais(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    # Limpa saída do fluxo de criação
    capsys.readouterr()

    sis.upd_st(id_ped, 'qualquer_status')

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'qualquer_status'
    assert "Cliente ganhou 100 pontos!" in saida


#>>>>>>>>>>>>>>>>>>>>>> TESTES DE EXCEÇÕES NO PEDIDO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# O código legado não valida se existe um pedido previamente para ser cancelado.
# Não hÁ validação nas regras de negócio, como comentando no legacy.
# Logo, já se subentende que cancelar um pedido que não existe funcionaria (mas há perigo)
# Ele faria um UPDATE na tabela em uma linha inexistente. Isso não afetaria nenhuma linha. Seria uma ação inócua.
# Talvez isso seja algo que precisa ser refeito no código refatorado?
# CANCELAMENTO DE PEDIDO
#
# Cenário:
# - Um pedido normal é criado corretamente
# - O pedido é cancelado
#
# O teste verifica:
# - se o status muda para "cancelado";
# - se a mensagem correta é exibida.
def test_cancelamento_de_pedido_altera_status_para_cancelado(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    sis.cancelar_pedido(id_ped)

    saida = capsys.readouterr().out
    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'cancelado'
    assert f"Pedido {id_ped} cancelado" in saida

# BUSCA DE PEDIDO INEXISTENTE
#
# Cenário:
# - O sistema recebe um ID que não existe no banco.
#
# O teste verifica:
# - se o metodo retorna None para pedidos inexistentes.
def test_busca_pedido_inexistente_retorna_none(sis):

    pedido = sis.get_ped(999)

    assert pedido is None

#>>>>>>>>>>>>>>>>>>>>>> TESTES DE RELATÓRIOS <<<<<<<<<<<<<<<<<<<<<<<<<<

# RELATÓRIO DE VENDAS
#
# Cenário:
# - Dois pedidos são criados
# - O relatório de vendas é gerado
#
# O teste verifica:
# - se o relatório imprime os pedidos;
# - se calcula o total geral;
# - se cria o arquivo rel_vendas.txt.
def test_gerar_relatorio_de_vendas(sis, capsys):
    itens1 = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    itens2 = [
        {'nome': 'produto2', 'p': 50, 'q': 2, 'tipo': 'desc10'}
    ]

    id1 = sis.add_ped('Joao Silva', itens1, 'normal')
    id2 = sis.add_ped('Maria Santos', itens2, 'vip')

    capsys.readouterr()

    sis.gerar_rel('vendas')

    saida = capsys.readouterr().out

    assert "=== RELATORIO DE VENDAS ===" in saida
    assert f"Pedido #{id1} - Cliente: Joao Silva - Total: R$100.00 - Status: pendente" in saida
    assert f"Pedido #{id2} - Cliente: Maria Santos - Total: R$85.50 - Status: pendente" in saida
    assert "Total Geral: R$185.50" in saida

    with open('rel_vendas.txt', 'r') as f:
        conteudo = f.read()

    assert "Total de vendas: 185.5" in conteudo

# RELATÓRIO DE CLIENTES
#
# Cenário:
# - Pedidos de clientes diferentes são criados
# - O relatório de clientes é gerado
#
# O teste verifica:
# - se os clientes aparecem no relatório;
# - se o total gasto por cliente é calculado;
# - se o arquivo rel_clientes.txt é criado.
def test_gerar_relatorio_de_clientes(sis, capsys):
    itens1 = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    itens2 = [
        {'nome': 'produto2', 'p': 50, 'q': 2, 'tipo': 'desc10'}
    ]

    sis.add_ped('Joao Silva', itens1, 'normal')
    sis.add_ped('Maria Santos', itens2, 'vip')

    capsys.readouterr()

    sis.gerar_rel('clientes')

    saida = capsys.readouterr().out

    assert "=== RELATORIO DE CLIENTES ===" in saida
    assert "Cliente: Joao Silva (normal) - Total gasto: R$100.00" in saida
    assert "Cliente: Maria Santos (vip) - Total gasto: R$85.50" in saida

    with open('rel_clientes.txt', 'r') as f:
        conteudo = f.read()

    assert "Joao Silva,normal" in conteudo
    assert "Maria Santos,vip" in conteudo