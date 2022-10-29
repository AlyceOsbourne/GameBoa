from project.src.components.memory import MemoryManagementUnit, MemoryRange, Memory
from project.src.system.event_handler import EventHandler
from project.src.system.events import ComponentEvents
from hypothesis import given, strategies as st
from unittest import TestCase


class TestMemory(TestCase):

    @given(st.integers(min_value=0, max_value=0xFFFF))
    def test_memory(self, addr):
        mem = Memory(0xFFFF)
        mem.write_addr(addr, b"\x01")
        self.assertEqual(mem.read_addr(addr, 1), b"\x01")


    @given(st.sampled_from(MemoryRange), st.integers(min_value=0, max_value=0xFF))
    def test_mmu(self, memory_range, mem_values):
        mmu = MemoryManagementUnit()
        mem_addr = st.integers(min_value=memory_range.start, max_value=memory_range.end)
        @given(mem_values, mem_addr)
        def test_write_read(value, addr):
            value = value.to_bytes(1, "little")
            mmu.write_memory_address(addr, value)
            self.assertEqual(mmu.read_memory_address(addr, 1), value)

    @given(st.sampled_from(MemoryRange), st.integers(min_value=0, max_value=0xFF))
    def test_mmu_events(self, memory_range, mem_values):
        mmu = MemoryManagementUnit()
        mem_addr = st.integers(min_value=memory_range.start, max_value=memory_range.end)
        @given(mem_values, mem_addr)
        def test_write_read(value, addr):
            value = value.to_bytes(1, "little")
            called_back = False
            def callback(val):
                nonlocal called_back
                called_back = True
                self.assertEqual(val, value)
            EventHandler.publish(ComponentEvents.RequestMemoryWrite, addr, value)
            EventHandler.publish(ComponentEvents.RequestMemoryRead, addr, 1, callback)
            self.assertTrue(mmu.read_memory_address(addr, 1), value)
            self.assertTrue(called_back)






