from pathlib import Path

from components.cartridge import Cartridge
from components.system_mappings import CartType


ROMS_DIRECTORY_PATH = Path(__file__).parent.parent.parent / "roms"
print(ROMS_DIRECTORY_PATH)


def test_cartridge_header():
    tetris_file_path = ROMS_DIRECTORY_PATH / "tetris.gb"
    cart = Cartridge(rom_file_path)
    assert not cart.cgb_flag
    assert not cart.sgb_flag
    assert cart.title == "Tetris"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == CartType.ROM

    pb_file_path = ROMS_DIRECTORY_PATH / "pb.gb"
    cart = Cartridge(rom_file_path)
    assert cart.sgb_flag
    assert not cart.cgb_flag
    assert cart.passes_header_checksum
    assert cart.title == "Pokemon Blue"
    assert cart.cartridge_type == (CartType.MBC3 | CartType.RAM | CartType.BATTERY)

    py_file_path = ROMS_DIRECTORY_PATH / "py.gbc"
    cart = Cartridge(rom_file_path)
    assert cart.cgb_flag
    assert cart.sgb_flag
    assert cart.passes_header_checksum
    assert cart.title == "Pokemon Yellow"
    assert cart.cartridge_type == (CartType.MBC5 | CartType.RAM | CartType.BATTERY)
