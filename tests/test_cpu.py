import unittest

from hypothesis import (
    given,
    strategies as st,
    settings,
    HealthCheck,
)

from project.src.components.instruction import instructions, cb_instructions
from project.src.system import ComponentEvents, SystemEvents, set_value

set_value("developer", "debug logging", False)
SystemEvents.SettingsUpdated()


class TestCPU(unittest.TestCase):
    instruction_list = list(instructions.values()) + list(cb_instructions.values())

    @given(st.sampled_from(instruction_list))
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=len(instruction_list))
    def test_instruction(self, instruction):
        ComponentEvents.RequestReset()
        ComponentEvents.RequestExecute(instruction)

    ComponentEvents.RequestReset()
