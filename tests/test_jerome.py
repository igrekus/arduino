import pytest
from jerome import *
from pyexpect import expect


@pytest.fixture()
def setup_jerome(request):

    def jerome_teardown():
        j.close()
    request.addfinalizer(jerome_teardown)

    j = Jerome(JeromeSerialMock())
    return j


def test_jerome_open_close(setup_jerome):
    j = setup_jerome

    expect(j.is_open).to_equal(True)
    expect(j.name).to_equal('Jerome at COM1')


def test_jerome_query(setup_jerome):
    j = setup_jerome

    expect(j.query('$KE')).to_equal('#OK')


def test_jerome_ping(setup_jerome):
    j = setup_jerome

    expect(j.ping()).to_equal('#OK')


def test_jerome_write_array(setup_jerome):
    j = setup_jerome

    expect(j.write_array('0001000')).to_equal('#WRA,OK,24')
    expect(j.pin_states).to_equal({
        IO1: PIN_OFF,
        IO2: PIN_OFF,
        IO3: PIN_OFF,
        IO4: PIN_ON,
        IO5: PIN_OFF,
        IO6: PIN_OFF,
        IO7: PIN_OFF,
        IO8: PIN_OFF,
        IO9: PIN_OFF,
        IO10: PIN_OFF,
        IO11: PIN_OFF,
        IO12: PIN_OFF,
        IO13: PIN_OFF,
        IO14: PIN_OFF,
        IO15: PIN_OFF,
        IO16: PIN_OFF,
        IO17: PIN_OFF,
        IO18: PIN_OFF,
        IO19: PIN_OFF,
        IO20: PIN_OFF,
        IO21: PIN_OFF,
        IO22: PIN_OFF,
        IO23: PIN_OFF,
        IO24: PIN_OFF
    })


def test_jerome_write_line(setup_jerome):
    j = setup_jerome

    expect(j.write_line(7, 1)).to_equal('#WR,OK')
    expect(j.pin_states).to_equal({
        IO1: PIN_OFF,
        IO2: PIN_OFF,
        IO3: PIN_OFF,
        IO4: PIN_OFF,
        IO5: PIN_OFF,
        IO6: PIN_OFF,
        IO7: PIN_ON,
        IO8: PIN_OFF,
        IO9: PIN_OFF,
        IO10: PIN_OFF,
        IO11: PIN_OFF,
        IO12: PIN_OFF,
        IO13: PIN_OFF,
        IO14: PIN_OFF,
        IO15: PIN_OFF,
        IO16: PIN_OFF,
        IO17: PIN_OFF,
        IO18: PIN_OFF,
        IO19: PIN_OFF,
        IO20: PIN_OFF,
        IO21: PIN_OFF,
        IO22: PIN_OFF,
        IO23: PIN_OFF,
        IO24: PIN_OFF
    })


def test_jerome_mkr_init(setup_jerome):
    j = setup_jerome

    expect(j.mkr_init()).to_equal(['#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#WRA,OK,24'])
    expect(j.pin_io).to_equal({
        IO1: IO_OUT,
        IO2: IO_OUT,
        IO3: IO_OUT,
        IO4: IO_OUT,
        IO5: IO_OUT,
        IO6: IO_OUT,
        IO7: IO_OUT,
        IO8: IO_OUT,
        IO9: IO_OUT,
        IO10: IO_OUT,
        IO11: IO_OUT,
        IO12: IO_OUT,
        IO13: IO_OUT,
        IO14: IO_OUT,
        IO15: IO_OUT,
        IO16: IO_OUT,
        IO17: IO_OUT,
        IO18: IO_OUT,
        IO19: IO_OUT,
        IO20: IO_OUT,
        IO21: IO_OUT,
        IO22: IO_OUT,
        IO23: IO_OUT,
        IO24: IO_OUT
    })
    expect(j.pin_states).to_equal({
        IO1: PIN_OFF,
        IO2: PIN_OFF,
        IO3: PIN_OFF,
        IO4: PIN_OFF,
        IO5: PIN_OFF,
        IO6: PIN_OFF,
        IO7: PIN_OFF,
        IO8: PIN_ON,
        IO9: PIN_OFF,
        IO10: PIN_ON,
        IO11: PIN_OFF,
        IO12: PIN_ON,
        IO13: PIN_OFF,
        IO14: PIN_ON,
        IO15: PIN_OFF,
        IO16: PIN_OFF,
        IO17: PIN_OFF,
        IO18: PIN_OFF,
        IO19: PIN_OFF,
        IO20: PIN_OFF,
        IO21: PIN_OFF,
        IO22: PIN_OFF,
        IO23: PIN_OFF,
        IO24: PIN_OFF
    })


def test_jerome_mkr_set_bit(setup_jerome):
    j = setup_jerome

    expect(j.mkr_set_bit(0, 1)).to_equal(('#WR,OK', '#WR,OK'))
    expect(j.pin_states).to_equal({
        IO1: PIN_OFF,
        IO2: PIN_OFF,
        IO3: PIN_OFF,
        IO4: PIN_OFF,
        IO5: PIN_OFF,
        IO6: PIN_OFF,
        IO7: PIN_OFF,
        IO8: PIN_OFF,
        IO9: PIN_ON,
        IO10: PIN_OFF,
        IO11: PIN_OFF,
        IO12: PIN_OFF,
        IO13: PIN_OFF,
        IO14: PIN_OFF,
        IO15: PIN_OFF,
        IO16: PIN_OFF,
        IO17: PIN_OFF,
        IO18: PIN_OFF,
        IO19: PIN_OFF,
        IO20: PIN_OFF,
        IO21: PIN_OFF,
        IO22: PIN_OFF,
        IO23: PIN_OFF,
        IO24: PIN_OFF
    })
