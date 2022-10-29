from project.src.components.register import Register
from project.src.system.event_handler import EventHandler
from project.src.system.events import ComponentEvents

from hypothesis import given, strategies as st
from unittest import TestCase

register_b_bit_strat = st.sampled_from(['A', 'F', 'B', 'C', 'D', 'E', 'H', 'L'])
register_16_bit_strat = st.sampled_from(['AF', 'BC', 'DE', 'HL'])
pc_sp_strat = st.sampled_from(['PC', 'SP'])
flag_strat = st.sampled_from(['FZ', 'FN', 'FH', 'FC'])

value_8_bit_strat = st.integers(min_value=0, max_value=255)
value_16_bit_strat = st.integers(min_value=0, max_value=65535)
flag_value_strat = st.sampled_from([0, 1])

class TestRegister(TestCase):
    def test_register(self):
        @given(value=value_8_bit_strat, register=register_b_bit_strat)
        def test_set_register_8(value, register):
            reg = Register()
            reg[register] = value & 0xff

            assert reg[register] == value & 0xff

        @given(value=value_16_bit_strat, register=register_16_bit_strat)
        def test_set_register_16(value, register):
            reg = Register()
            reg[register] = value & 0xffff

            assert reg[register] == value & 0xffff
            left, right = register
            assert reg[left] == (value >> 8) & 0xff
            assert reg[right] == value & 0xff

        @given(value=value_16_bit_strat, register=pc_sp_strat)
        def test_set_pc_sp(value, register):
            reg = Register()
            reg[register] = value & 0xffff

            assert reg[register] == value & 0xffff

        @given(value=flag_value_strat, flag=flag_strat)
        def test_set_flag(value, flag):
            reg = Register()
            reg[flag] = value

            assert reg[flag] == value

        test_set_register_8()
        test_set_register_16()
        test_set_pc_sp()
        test_set_flag()

    def test_register_events(self):
        @given(value=value_8_bit_strat, register=register_b_bit_strat)
        def test_set_register_8(value, register):
            reg = Register()
            callback_called = False
            def callback(value):
                nonlocal callback_called
                callback_called = True
            EventHandler.publish(ComponentEvents.RequestRegisterWrite, register, value & 0xff)
            EventHandler.publish(ComponentEvents.RequestRegisterRead, register, callback)
            assert reg[register] == value & 0xff
            assert callback_called

        @given(value=value_16_bit_strat, register=register_16_bit_strat)
        def test_set_register_16(value, register):
            reg = Register()
            callback_called = False
            def callback(value):
                nonlocal callback_called
                callback_called = True
            EventHandler.publish(ComponentEvents.RequestRegisterWrite, register, value & 0xffff)
            EventHandler.publish(ComponentEvents.RequestRegisterRead, register, callback)
            assert reg[register] == value & 0xffff
            left, right = register
            assert reg[left] == (value >> 8) & 0xff
            assert reg[right] == value & 0xff
            assert callback_called


        @given(value=value_16_bit_strat, register=pc_sp_strat)
        def test_set_pc_sp(value, register):
            reg = Register()
            callback_called = False
            def callback(value):
                nonlocal callback_called
                callback_called = True
            EventHandler.publish(ComponentEvents.RequestRegisterWrite, register, value & 0xffff)
            EventHandler.publish(ComponentEvents.RequestRegisterRead, register, callback)
            assert reg[register] == value & 0xffff
            assert callback_called

        @given(value=flag_value_strat, flag=flag_strat)
        def test_set_flag(value, flag):
            reg = Register()
            callback_called = False
            def callback(value):
                nonlocal callback_called
                callback_called = True
            EventHandler.publish(ComponentEvents.RequestRegisterWrite, flag, value)
            EventHandler.publish(ComponentEvents.RequestRegisterRead, flag, callback)
            assert reg[flag] == value
            assert callback_called

        test_set_register_8()
        test_set_register_16()
        test_set_pc_sp()
        test_set_flag()





