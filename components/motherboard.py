from typing import Optional

from components.cartridge import Cartridge
from components.cpu import CPU

class Motherboard:
    def __init__(self, cpu:CPU, cartridge: Optional[Cartridge] = None):
        self.cpu = cpu
        self.cartridge = cartridge