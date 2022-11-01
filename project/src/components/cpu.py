from .instruction import Instruction
from project.src.system import bus as dd

def write_operand(operand, value):
    match operand:
        case _:
            raise ValueError(f"Invalid operand {operand}.")


def read_operand(operand):
    match operand:
        case _:
            raise ValueError(f"Invalid operand {operand}.")


def execute(instruction: Instruction):
    match instruction.mnemonic:
        case "LD" | "LDH" | "LDHL" | "LDI" | "LDD":
            load(instruction)
        case "PUSH" | "POP":
            "push_pop(instruction)"
        case "ADD" | "ADC" | "SUB" | "SBC" | "AND" | "XOR" | "OR" | "CP":
            "add_sub(instruction)"
        case "INC" | "DEC":
            "inc_dec(instruction)"
        case "RLC" | "RRC" | "RL" | "RR" | "SLA" | "SRA" | "SWAP" | "SRL":
            "rotate(instruction)"
        case "BIT" | "SET" | "RES":
            "bit(instruction)"
        case "JP" | "JR":
            "jump(instruction)"
        case "CALL" | "RST":
            "call(instruction)"
        case "RET" | "RETI":
            "ret(instruction)"
        case "STOP" | "HALT" | "DI" | "EI":
            "misc(instruction)"
        case _:
            raise ValueError(f"Invalid instruction {instruction}.")


def load(instruction: Instruction):
    raise NotImplementedError


def push_pop(instruction: Instruction):
    raise NotImplementedError


def add_sub(instruction: Instruction):
    raise NotImplementedError


def inc_dec(instruction: Instruction):
    raise NotImplementedError


def rotate(instruction: Instruction):
    raise NotImplementedError


def bit(instruction: Instruction):
    raise NotImplementedError


def jump(instruction: Instruction):
    raise NotImplementedError


def call(instruction: Instruction):
    raise NotImplementedError


def ret(instruction: Instruction):
    raise NotImplementedError


def misc(instruction: Instruction):
    raise NotImplementedError
