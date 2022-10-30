from project.src.components import register
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

    def test_register_events(self):
        @given(value=value_8_bit_strat, register=register_b_bit_strat)
        def test_set_register_8(value, register):
            callback_called = False
            def callback(value):
                nonlocal callback_called
                callback_called = True
                self.assertEqual(value, value)
            EventHandler.publish(ComponentEvents.RequestRegisterWrite, register, value & 0xff)
            EventHandler.publish(ComponentEvents.RequestRegisterRead, register, callback)
            assert callback_called

        @given(value=value_16_bit_strat, register=register_16_bit_strat)
        def test_set_register_16(value, register):
            callback_called = False
            def callback(value):
                nonlocal callback_called
                callback_called = True
                self.assertEqual(value, value)
            EventHandler.publish(ComponentEvents.RequestRegisterWrite, register, value & 0xffff)
            EventHandler.publish(ComponentEvents.RequestRegisterRead, register, callback)
            assert callback_called


        @given(value=value_16_bit_strat, register=pc_sp_strat)
        def test_set_pc_sp(value, register):
            callback_called = False
            def callback(value):
                nonlocal callback_called
                callback_called = True
                self.assertEqual(value, value)
            EventHandler.publish(ComponentEvents.RequestRegisterWrite, register, value & 0xffff)
            EventHandler.publish(ComponentEvents.RequestRegisterRead, register, callback)
            assert callback_called

        test_set_register_8()
        test_set_register_16()
        test_set_pc_sp()





