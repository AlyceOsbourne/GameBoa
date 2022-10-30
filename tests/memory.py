from unittest import TestCase

from hypothesis import given, strategies

from project.src.system.events import ComponentEvents
from project.src.system.event_handler import EventHandler
from project.src.components.memory import Memory, MemoryManagementUnit, MemoryRange


class TestMemory(TestCase):
    @given(strategies.integers(min_value=0, max_value=0xFFFF))
    def test_memory(self, address):
        memory = Memory(0xFFFF)
        memory.write_address(address, b"\x01")
        self.assertEqual(memory.read_address(address, 1), b"\x01")

    @given(
        strategies.sampled_from(MemoryRange),
        strategies.integers(min_value=0, max_value=0xFF),
    )
    def test_mmu(self, memory_range, memory_values):
        mmu = MemoryManagementUnit()
        memory_address = strategies.integers(
            min_value=memory_range.start,
            max_value=memory_range.end,
        )

        @given(memory_values, memory_address)
        def test_write_read(value, address):
            value = value.to_bytes(1, "little")
            mmu.write_memory_address(address, value)
            self.assertEqual(mmu.read_memory_address(address, 1), value)

    @given(
        strategies.sampled_from(MemoryRange),
        strategies.integers(min_value=0, max_value=0xFF),
    )
    def test_mmu_events(self, memory_range, memory_values):
        mmu = MemoryManagementUnit()
        memory_address = strategies.integers(
            min_value=memory_range.start,
            max_value=memory_range.end,
        )

        @given(memory_values, memory_address)
        def test_write_read(value, address):
            value = value.to_bytes(1, "little")
            called_back = False

            def callback(callback_value):
                nonlocal called_back
                called_back = True
                self.assertEqual(callback_value, value)

            EventHandler.publish(
                ComponentEvents.RequestMemoryWrite,
                address,
                value,
            )
            EventHandler.publish(
                ComponentEvents.RequestMemoryRead,
                address,
                1,
                callback,
            )
            self.assertTrue(mmu.read_memory_address(address, 1), value)
            self.assertTrue(called_back)
