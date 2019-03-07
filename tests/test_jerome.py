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


def test_jerome_mkr_init(setup_jerome):
    j = setup_jerome

    expect(j.mkr_init()).to_equal(['#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#IO,SET,OK', '#WRA,OK,24'])



