from project.src.system.event_handler import EventHandler
from project.src.system.events import ComponentEvents
from project.src.components.instruction import Instruction


def execute( instruction: Instruction):

    match instruction.mnemonic:
        case "LD" | "LDH" | "LDHL" | "LDI" | "LDD":
            load(instruction)
        case "PUSH" | "POP":
            push_pop(instruction)
        case "ADD" | "ADC" | "SUB" | "SBC" | "AND" | "XOR" | "OR" | "CP":
            add_sub(instruction)
        case "INC" | "DEC":
            inc_dec(instruction)
        case "RLC" | "RRC" | "RL" | "RR" | "SLA" | "SRA" | "SWAP" | "SRL":
            rotate(instruction)
        case "BIT" | "SET" | "RES":
            bit(instruction)
        case "JP" | "JR":
            jump(instruction)
        case "CALL" | "RST":
            call(instruction)
        case "RET" | "RETI":
            ret(instruction)
        case "STOP" | "HALT" | "DI" | "EI":
            misc(instruction)
        case _:
            raise ValueError(f"Invalid instruction: {instruction}")

def load(instruction: Instruction):
    ...

def push_pop(instruction: Instruction):
    ...

def add_sub(instruction: Instruction):
    ...

def inc_dec(instruction: Instruction):
    ...

def rotate(instruction: Instruction):
    ...

def bit(instruction: Instruction):
    ...

def jump(instruction: Instruction):
    ...

def call(instruction: Instruction):
    ...

def ret(instruction: Instruction):
    ...

def misc(instruction: Instruction):
    ...
