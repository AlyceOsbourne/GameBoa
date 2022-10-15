from pathlib import Path

# from components.cartridge import Cartridge
# from components.system_mappings import CartType


ROM_DIRECTORY_PATH = Path(__file__).parent.parent.parent / "ROMs"
print(ROM_DIRECTORY_PATH)


def test_cartridge_header():
    rom_file_path = ROM_DIRECTORY_PATH / "tetris.gb"
    cart = Cartridge(rom_file_path)
    assert cart.title == "Tetris"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == CartType.ROM
    assert not cart.sgb_flag
    assert not cart.cgb_flag

    rom_file_path = ROM_DIRECTORY_PATH / "pb.gb"
    cart = Cartridge(rom_file_path)
    assert cart.title == "Pokemon Blue"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == (CartType.MBC3 | CartType.RAM | CartType.BATTERY)
    assert cart.sgb_flag
    assert not cart.cgb_flag

    rom_file_path = ROM_DIRECTORY_PATH / "py.gbc"
    cart = Cartridge(rom_file_path)
    assert cart.title == "Pokemon Yellow"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == (CartType.MBC5 | CartType.RAM | CartType.BATTERY)
    assert cart.sgb_flag
    assert cart.cgb_flag
