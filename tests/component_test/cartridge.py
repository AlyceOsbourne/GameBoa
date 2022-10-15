import pathlib

from components import cartridge, system_mappings


ROM_DIRECTORY_PATH = pathlib.Path(__file__).parent.parent.parent / "roms"


def test_cartridge_header():
    rom_file_path = ROM_DIRECTORY_PATH / "tetris.gb"
    cart = cartridge.Cartridge(rom_file_path)
    assert cart.title == "Tetris"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == system_mappings.CartType.ROM
    assert not cart.sgb_flag
    assert not cart.cgb_flag

    rom_file_path = ROM_DIRECTORY_PATH / "pb.gb"
    cart = cartridge.Cartridge(rom_file_path)
    assert cart.title == "Pokemon Blue"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == (
        system_mappings.CartType.MBC3
        | system_mappings.CartType.RAM
        | system_mappings.CartType.BATTERY
    )
    assert cart.sgb_flag
    assert not cart.cgb_flag

    rom_file_path = ROM_DIRECTORY_PATH / "py.gbc"
    cart = cartridge.Cartridge(rom_file_path)
    assert cart.title == "Pokemon Yellow"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == (
        system_mappings.CartType.MBC5
        | system_mappings.CartType.RAM
        | system_mappings.CartType.BATTERY
    )
    assert cart.sgb_flag
    assert cart.cgb_flag
