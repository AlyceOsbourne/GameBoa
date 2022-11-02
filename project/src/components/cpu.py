from functools import partial
from pprint import pprint, pformat

from .instruction import Instruction, instructions, cb_instructions
from project.src.system import LogEvent, ComponentEvents, GuiEvents

mappings = locals()

_read_mapped_memory = ComponentEvents.RequestMemoryRead
_write_mapped_memory = ComponentEvents.RequestMemoryWrite

def _get_operator(operator):
    match operator:
        case _ if operator.startswith("(") and operator.endswith(")"):
            return _read_mapped_memory(_get_operator(operator[1:-1]))
        case 'NZ' | 'Z' | 'NC' | 'C':
            return mappings.get(f"get_flag_{operator[-1]}") ^ (operator[0] == 'N')
        case 'a16':
            return mappings.get("_read_mapped_memory")(mappings.get("_get_16_bit_register_PC")()) + (
                        mappings.get("_read_mapped_memory")(mappings.get("_get_16_bit_register_PC")() + 1) << 8)
        case 'A' | 'F' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L':
            return mappings.get(f"get_register_{operator}")
        case 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
            return mappings.get(f"get_16_bit_register_{operator}")


def _set_operator(operator, value):
    match operator:
        case _ if operator.startswith("(") and operator.endswith(")"):
            _write_mapped_memory(_get_operator(operator[1:-1]), value)
        case 'NZ' | 'Z' | 'NC' | 'C':
            mappings.get(f"set_flag_{operator[-1]}")(value) ^ (operator[0] == 'N')
        case 'a16':
            _write_mapped_memory(_get_operator("a16"), value)
        case 'A' | 'F' | 'B' | 'C' | 'D' | 'E' | 'H' | 'L':
            mappings.get(f"_set_8_bit_register_{operator}")(value)
        case 'AF' | 'BC' | 'DE' | 'HL' | 'SP' | 'PC':
            mappings.get(f"_set_16_bit_register_{operator}")(value)


mappings.update(
    {
        **{
            f"_get_8_bit_register_{_8_bit_register}": partial(_get_operator, _8_bit_register)
            for _8_bit_register in ("A", "F", "B", "C", "D", "E", "H", "L")
        },
        **{
            f"_set_8_bit_register_{_8_bit_register}": partial(_set_operator, _8_bit_register)
            for _8_bit_register in ("A", "F", "B", "C", "D", "E", "H", "L")
        },
        **{
            f"_get_16_bit_register_{_16_bit_register}": partial(_get_operator, _16_bit_register)
            for _16_bit_register in ("AF", "BC", "DE", "HL", "SP", "PC")
        },
        **{
            f"_set_16_bit_register_{_16_bit_register}": partial(_set_operator, _16_bit_register)
            for _16_bit_register in ("AF", "BC", "DE", "HL", "SP", "PC")
        },
    })

mappings.update({

    '_get_flags_register': partial(mappings.get('_get_8_bit_register_F'), ),
    '_set_flags_register': partial(mappings.get('_set_8_bit_register_F'), ),

    **{
        f"_get_flag_{flag}": partial(lambda: mappings.get("_get_flags_register")() >> 'ZNC'.index(flag) & 1)
        for flag in ("Z", "N", "H", "C")
    },
    **{
        f"_set_flag_{flag}": partial(lambda value: mappings.get("_set_flags_register")(
            mappings.get("_get_flags_register")() & ~(1 << 'ZNC'.index(flag)) | (value << 'ZNC'.index(flag))
        ))
        for flag in ("Z", "N", "H", "C")
    },
})


def execute(instruction: Instruction):
    if instruction.op_code == 0xCB:
        instruction = cb_instructions[_read_mapped_memory(mappings.get("_get_16_bit_register_PC")())]
        mappings.get("_set_16_bit_register_PC")(mappings.get("_get_16_bit_register_PC")() + 1)
    mappings.get(f"_execute_{instruction.mnemonic}")(instruction)


mappings.update({
    **{
        f"_execute_{instruction.mnemonic}": partial(
            lambda instruction: LogEvent.LogDebug(f"Instruction {instruction.mnemonic} not implemented"))
        for instruction in instructions.values() and cb_instructions.values()
        if instruction.mnemonic not in mappings
    },
})


LogEvent.LogDebug.emit(f"Mapped CPU Instructions\n{pformat({k:v for k,v in mappings.items() if k.startswith(('_execute_', '_get_', '_set_'))})}")

LogEvent.LogInfo.emit("CPU initialized")
