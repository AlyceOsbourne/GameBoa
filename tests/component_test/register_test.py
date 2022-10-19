from components.register import Register


def test_register():
    register = Register()
    assert register.a == 0x01
    assert register.b == 0x00
    assert register.c == 0x13
    assert register.d == 0x00
    assert register.e == 0xD8
    assert register.h == 0x01
    assert register.l == 0x4D
    assert register.f == 0xB0
    assert register.sp == 0xFFFE
    assert register.pc == 0x0100
    assert register.af == 0x01B0
    assert register.bc == 0x0013
    assert register.de == 0x00D8
    assert register.hl == 0x014D
