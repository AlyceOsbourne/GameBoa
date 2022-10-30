from project.src import EventHandler, Observer, ComponentEvents, register
from hypothesis import given, strategies as st
import unittest


class TestRegister(unittest.TestCase):
    READ_EVENT = ComponentEvents.RequestRegisterRead
    WRITE_EVENT = ComponentEvents.RequestRegisterWrite

    value_strat_8_bit = st.integers(min_value=0, max_value=255)
    value_strat_16_bit = st.integers(min_value=0, max_value=65535)

    register_strat_8_bit = st.sampled_from(["A", "F", "B", "C", "D", "E", "H", "L"])
    register_strat_16_bit = st.sampled_from(["AF", "BC", "DE", "HL"])
    stack_pointer_program_counter = st.sampled_from(["SP", "PC"])

    @given(register_strat_8_bit, value_strat_8_bit)
    def test_set_8_bit_register(self, register, value):
        EventHandler.publish(self.WRITE_EVENT, register, value)
        self.assertEqual(Observer.peep(self.READ_EVENT, register), value)

    @given(register_strat_16_bit, value_strat_16_bit)
    def test_set_16_bit_register(self, register, value):
        EventHandler.publish(self.WRITE_EVENT, register, value)
        self.assertEqual(Observer.peep(self.READ_EVENT, register), value)

    @given(stack_pointer_program_counter, value_strat_16_bit)
    def test_set_16_bit_register(self, register, value):
        EventHandler.publish(self.WRITE_EVENT, register, value)
        self.assertEqual(Observer.peep(self.READ_EVENT, register), value)
