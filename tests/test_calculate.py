from app.routers.orders import order_summ_calculate


def test_calculation():
    assert order_summ_calculate(500, -500, 1000) == -1000
    assert order_summ_calculate(500, -200, 1000) == -700
    assert order_summ_calculate(1264, 0, 560) == 704
    assert order_summ_calculate(430, 0, 760.5) == -330.5
    assert order_summ_calculate(1340, -500, 1000) == -160
    assert order_summ_calculate(1500, -1500, 800) == -800
    assert order_summ_calculate(300, -100, 1050) == -850
    assert order_summ_calculate(300, -100, 300) == -100
