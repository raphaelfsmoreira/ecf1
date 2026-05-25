import sqlite3
import json
from datetime import datetime
from typing import Any, Optional, List, Dict, cast


class Sis:
    def __init__(self) -> None:
        self.db = sqlite3.connect('loja.db')
        self.c = self.db.cursor()
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS ped(
                id INTEGER PRIMARY KEY, 
                cli TEXT, 
                itens TEXT,
                tot REAL,
                st TEXT,
                dt TEXT,
                tp TEXT)        
            ''')
        self.db.commit()

    def add_ped(self, n: str, its: List[Dict[str, Any]], t: str) -> int:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        tot: float = 0.0
        for i in its:
            if i['tipo'] == 'normal':
                tot += i['p'] * i['q']
            elif i['tipo'] == 'desc10':
                tot += i['p'] * i['q'] * 0.9
            elif i['tipo'] == 'desc20':
                tot += i['p'] * i['q'] * 0.8
            elif i['tipo'] == 'frete_gratis':
                tot += i['p'] * i['q']
        
        if t == 'vip':
            tot = tot * 0.95
        elif t == 'corporativo':
            tot = tot * 0.90
        
        its_str = json.dumps(its)
        
        self.c.execute(
            '''INSERT INTO ped (cli, itens, tot, st, dt, tp)
                    VALUES(?, ?, ?, ?, ?, ?)    
            ''',
            (n, its_str, tot, 'pendente', dt, t)
        )
        self.db.commit()

        # Canal de notificaçao depende do tipo de cliente

        if t == 'normal':
            print(f"Email enviado para {n}: Pedido recebido!")
        elif t == 'vip':
            print(f"Email enviado para {n}: Pedido recebido!")
            print(f"SMS enviado para {n}: Pedido VIP recebido!")
        elif t == 'corporativo':
            print(f"Email enviado para {n}: Pedido recebido!")
            print(f"Notificação enviada ao gerente de conta de {n}")
        
        return int(self.c.lastrowid or 0)

    def get_ped(self, id: int) -> Optional[Dict[str, Any]]:
        self.c.execute("SELECT * FROM ped WHERE id=?", (id,))
        r = self.c.fetchone()
        if r:
            return {
            'id': r[0],
            'cli': r[1],
            'itens': json.loads(r[2]),
            'tot': r[3],
            'st': r[4],
            'dt': r[5],
            'tp': r[6]
        }
        return None
    
    def upd_st(self, id: int, s: str) -> None:
        p = self.get_ped(id)

        if p:
            self.c.execute(
                "UPDATE ped SET st=? WHERE id=?",
                (s, id)
            )   
            self.db.commit()

            if s == 'aprovado':
                print(f"Email enviado para {p['cli']}: Pedido aprovado!")

                if p['tp'] == 'vip':
                    print(f"SMS enviado para {p['cli']}: Pedido aprovado!")

            elif s == 'enviado':
                print(f"Email enviado para {p['cli']}: Pedido enviado!")

            elif s == 'entregue':
                print(f"Email enviado para {p['cli']}: Pedido entregue!")

                if p['tp'] == 'vip':
                    pts = int(p['tot'] * 2)
                    print(f"Cliente VIP ganhou {pts} pontos!")

                elif p['tp'] == 'corporativo':
                    pts = int(p['tot'] * 1.5)
                    print(f"Cliente corporativo ganhou {pts} pontos!")

            else:
                pts = int(p['tot'])
                print(f"Cliente ganhou {pts} pontos!")

    # Por incrivel que pareça, o código legado busca o total dos pedidos de um cliente pelo
    # NOME DO CLIENTE. No caso n é o nome, não um ID...
    def calc_tot_cli(self, n: str) -> float:
        self.c.execute("SELECT * FROM ped WHERE cli=?", (n,))
        rs = self.c.fetchall()

        t: float = 0.0

        for r in rs:
            t += r[3]

        return t

    def gerar_rel(self, tipo: str) -> None:

        if tipo == 'vendas':

            self.c.execute("SELECT * FROM ped")
            rs = self.c.fetchall()

            print("=== RELATORIO DE VENDAS === ")

            tot_g = 0

            for r in rs:
                print(
                    f"Pedido #{r[0]} - Cliente: {r[1]} - "
                    f"Total: R${r[3]:.2f} - Status: {r[4]}"
                )

                tot_g += r[3]

            print(f"Total Geral: R${tot_g:.2f}")

            with open('rel_vendas.txt', 'w') as f:
                f.write(f"Total de vendas: {tot_g}")

        elif tipo == 'clientes':

            self.c.execute("SELECT DISTINCT cli, tp FROM ped")
            rs = self.c.fetchall()

            print("=== RELATORIO DE CLIENTES === ")

            for r in rs:
                n = r[0]
                tp = r[1]
                tot = self.calc_tot_cli(n)
                print(
                    f"Cliente: {n} ({tp}) - "
                    f"Total gasto: R${tot:.2f}"
                )

            with open('rel_clientes.txt', 'w') as f:
                for r in rs:
                    f.write(f"{r[0]},{r[1]}\n")

    def proc_pag(self, id: int, m: str, vl: float) -> bool:

        p = self.get_ped(id)

        if not p:
            return False
        
        if vl < p['tot']:
            print("Valor insuficiente!")

            return False

        # Map legacy method strings to PaymentType where possible and use
        # the strategy implementations to decide acceptance. We create a
        # minimal order-like adapter with `total_amount` to satisfy the
        # strategy interface without importing the full domain model here.
        from src.models.enums import PaymentType
        from src.strategies.payment_strategy import strategy_for_payment_type

        class _OrderLike:
            def __init__(self, total_amount: float) -> None:
                self.total_amount = total_amount

        method_map = {
            'cartao': PaymentType.CreditCard,
            'pix': PaymentType.Pix,
            'boleto': PaymentType.Boleto,
            'crypto': PaymentType.Crypto,
        }

        payment_type = method_map.get(m)
        if payment_type is None:
            print("Metodo de pagamento invalido!")
            return False

        strategy = strategy_for_payment_type(payment_type)
        order_like = _OrderLike(p['tot'])

        # Preserve legacy prints for UX parity
        if m == 'cartao':
            print("Processando pagamento com cartao...")
            print("Cartao validado!")
        elif m == 'pix':
            print("Gerando QR Code PIX...")
            print("PIX recebido!")
        elif m == 'boleto':
            print("Gerando boleto...")
            print("Boleto gerado!")
        elif m == 'crypto':
            print("Processando pagamento em criptomoeda...")

        # strategy.process_payment expects the domain Order type; cast to Any
        accepted = strategy.process_payment(cast(Any, order_like), vl)

        # Legacy semantics: cartao and pix auto-approve; boleto does not.
        if accepted and m in ('cartao', 'pix'):
            self.upd_st(id, 'aprovado')

        return accepted
        

    def validar_estoque(self, its: List[Dict[str, Any]]) -> bool:

        # integrar com sistema de estoque externo
        est = {
            'produto1': 100,
            'produto2': 50,
            'produto3': 75
            }

        for i in its:

            if i['nome'] not in est:
                print(f"Produto {i['nome']} nao encontrado!")

                return False

            if est[i['nome']] < i['q']:
                print(f"Estoque insuficiente para {i['nome']}!")
                return False

        return True
    

    def cancelar_pedido(self, id: int) -> None:

        # cancela sem validar regras de negocio
        self.c.execute(
            "UPDATE ped SET st=? WHERE id=?",
            ('cancelado', id)
        )   

        self.db.commit()

        print(f"Pedido {id} cancelado")

    
    def close(self) -> None:
        self.db.close()


class PedEspecial(Sis):
    pass
    

def main() -> None:
    s = Sis()

    its1 = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo':'desc10'}
    ]

    if s.validar_estoque(its1):
        id1 = s.add_ped('Joao Silva', its1, 'normal')
        print(f"Pedido {id1} criado!")
        s.proc_pag(id1, 'cartao', 250)
        s.upd_st(id1, 'enviado')
        s.upd_st(id1, 'entregue')
    
    its2 = [
        {'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}
    ]

    if s.validar_estoque(its2):
        id2 = s.add_ped('Maria Santos', its2, 'vip')
        s.proc_pag(id2, 'pix', 160)
    
    its3 = [
        {'nome': 'produto1', 'p': 100, 'q': 5, 'tipo': 'normal'}
    ]

    if s.validar_estoque(its3):
        id3 = s.add_ped('Empresa XYZ', its3, 'corporativo')
        s.proc_pag(id3, 'boleto', 500)

    s.gerar_rel('vendas')
    print()
    s.gerar_rel('clientes')
    s.close()


if __name__ == '__main__':
    main()