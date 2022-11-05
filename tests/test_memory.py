from project.src import bus as dd, memory
from hypothesis import given, strategies as st
import unittest

from project.src.system import set_value, SystemEvents

set_value('developer', 'debug logging', False)
SystemEvents.SettingsUpdated()