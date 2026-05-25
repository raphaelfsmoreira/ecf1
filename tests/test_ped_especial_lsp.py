import pytest

from src.legacy import PedEspecial, Sis


def test_ped_especial_behaves_like_sis_for_add_and_update(tmp_path, monkeypatch, capsys) -> None:
    legacy_dir = tmp_path / "legacy"
    special_dir = tmp_path / "special"
    legacy_dir.mkdir()
    special_dir.mkdir()

    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'},
    ]

    monkeypatch.chdir(legacy_dir)
    sis = Sis()
    sis_id = sis.add_ped('Cliente Base', itens, 'normal')
    sis.upd_st(sis_id, 'entregue')
    sis_output = capsys.readouterr().out
    sis_pedido = sis.get_ped(sis_id)
    sis.close()

    monkeypatch.chdir(special_dir)
    ped_especial = PedEspecial()
    especial_id = ped_especial.add_ped('Cliente Base', itens, 'normal')
    ped_especial.upd_st(especial_id, 'entregue')
    especial_output = capsys.readouterr().out
    especial_pedido = ped_especial.get_ped(especial_id)
    ped_especial.close()

    assert sis_pedido is not None
    assert especial_pedido is not None
    assert sis_pedido['tot'] == pytest.approx(especial_pedido['tot'])
    assert sis_pedido['st'] == especial_pedido['st']
    assert 'Pedido especial' not in especial_output
    assert 'Pedido especial' not in sis_output