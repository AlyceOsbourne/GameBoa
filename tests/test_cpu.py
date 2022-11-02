from hypothesis import given, strategies as st
import unittest
from project.src.system import ComponentEvents
from project.src.components.instruction import instructions, cb_instructions
from project.src.components.cpu import execute

class TestCPU(unittest.TestCase):
    instruction_strat = st.sampled_from(list(instructions.values() and cb_instructions.values()))

    @given(instruction_strat)
    def test_execute(self, instruction):
        try:
            self.assertEqual(execute(instruction), True)
        except NotImplementedError as e:
            print(f"Instruction {instruction} not implemented.")
            self.assertEqual(execute(instruction), False)
