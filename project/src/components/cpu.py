from project.src.system import LogEvent, ComponentEvents, GuiEvents; LogEvent.LogInfo('Initializing CPU')
from .instruction import Instruction, instructions, cb_instructions

#Todo remove this temp event, is stand in for memory read
ComponentEvents.RequestMemoryRead.allow_requests(lambda addr: 0)


_read_mem = ComponentEvents.RequestMemoryRead.request_data
_write_mem = ComponentEvents.RequestMemoryWrite
_read_reg = ComponentEvents.RequestRegisterRead.request_data
_write_reg = ComponentEvents.RequestRegisterWrite

def read_operand(operand) -> int:
    match operand:
        case 'A' | 'F' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L':
            return _read_reg(operand)
        case 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
            return _read_reg(operand)
        case 'd8' | 'a8':
            return _read_mem(_read_reg('PC'))
        case 'd16' | 'a16':
            return _read_mem(_read_reg('PC')) | _read_mem(_read_reg('PC') + 1) << 8
        case _ if operand.startswith('(') and operand.endswith(')'):
            return _read_mem(read_operand(operand[1:-1]))
        case _:
            LogEvent.LogDebug(f'Unknown operand {operand} for read')
            return 0

def write_operand(operand, value):
    match operand:
        case _ if operand.startswith('(') and operand.endswith(')'):
            _write_mem(read_operand(operand[1:-1]), value)
        case _:
            LogEvent.LogDebug(f'Unknown operand {operand} for write')

def fetch_op_code():
    val = _read_mem(_read_reg('PC'))
    _write_reg('PC', _read_reg('PC') + 1)
    return val

def decode_op_code(op_code, is_cb=False):
    if is_cb:
        return cb_instructions[op_code]
    return instructions[op_code]

@ComponentEvents.RequestExecute
def execute(instruction: Instruction):
    match instruction.mnemonic:
        case "NOP":
            pass
        case "PREFIX":
            execute(decode_op_code(fetch_op_code(), is_cb=True))
        case "HALT":
            ComponentEvents.RequestHalt()

        case _:
            LogEvent.LogDebug(f"Instruction {instruction.mnemonic} not implemented yet.")


