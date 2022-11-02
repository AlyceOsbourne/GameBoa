from project.src import bus as dd
from hypothesis import given, strategies as st
import unittest

from project.src.system import ComponentEvents


class TestRegister(unittest.TestCase):
    READ_EVENT = ComponentEvents.RequestRegisterRead
    WRITE_EVENT = ComponentEvents.RequestRegisterWrite

    value_strat_8_bit = st.integers(min_value=0, max_value=255)
    value_strat_16_bit = st.integers(min_value=0, max_value=65535)

    register_strat_8_bit = st.sampled_from(["A", "F", "B", "C", "D", "E", "H", "L"])
    register_strat_16_bit = st.sampled_from(["AF", "BC", "DE", "HL"])
    stack_pointer_program_counter = st.sampled_from(["SP", "PC"])

    def _test(self, register, value):
        self.WRITE_EVENT(register, value)
        self.assertEqual(self.READ_EVENT.request_data(register), value)

    @given(register_strat_8_bit, value_strat_8_bit)
    def test_8_bit(self, register, value):
        self._test(register, value)

    @given(register_strat_16_bit, value_strat_16_bit)
    def test_16_bit(self, register, value):
        self._test(register, value)

    @given(stack_pointer_program_counter, value_strat_16_bit)
    def test_stack_pointer_program_counter(self, register, value):
        self._test(register, value)