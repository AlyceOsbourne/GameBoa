import array

from project.src.system.event_handler import EventHandler
from project.src.system.observer import Observer
from project.src.system.events import ComponentEvents, GuiEvents

registry = array.array('B', [0] * 12)
REGS = 'AFBCDEHLSPPC'

def set_8(reg, val):
    idx = REGS.index(reg)
    registry[idx] = val

def set_16(reg, val):
    idx = REGS.index(reg)
    registry[idx] = val & 0xff
    registry[idx + 1] = val >> 8

def get_8(reg):
    return registry[REGS.index(reg)]

def get_16(reg):
    return registry[REGS.index(reg)] | (registry[REGS.index(reg) + 1] << 8)

@EventHandler.subscriber(ComponentEvents.RequestRegisterWrite)
def set_register(register, value):
    match register:
        case 'A' | 'F' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L':
            set_8(register, value)
        case 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
            set_16(register, value)

@Observer.observable(ComponentEvents.RequestRegisterRead)
def get_register(register):
    match register:
        case 'A' | 'F' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L':
            return get_8(register)
        case 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
            return get_16(register)

@Observer.observable(GuiEvents.RequestRegistryStatus)
def get_registry_status():
    return_string = ''
    for i, reg in enumerate(['AF', 'BC', 'DE', 'HL', 'SP', 'PC']):
        left, right = registry[i * 2], registry[i * 2 + 1]
        return_string += f'{reg}: {left:02X}{right:02X} '
    return_string = return_string[:-1]
    return return_string

@EventHandler.subscriber(ComponentEvents.RequestReset)
def reset():
    for i in range(12):
        registry[i] = 0
