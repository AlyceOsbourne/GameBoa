from components import cartridge, system_mappings

import pathlib
import pytest

rom_folder_path = pathlib.Path(__file__).parent.parent.parent / "roms"


def test_cartridge_header():
    # TODO: Expand these tests, mainly for things like read and write, but we need known values first

    rom_path = rom_folder_path / "Tetris.gb"
    cart = cartridge.Cartridge(rom_path)
    assert cart.title == "Tetris"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == system_mappings.CartType.ROM
    assert not cart.sgb_flag
    assert not cart.cgb_flag

    rom_path = rom_folder_path / "pb.gb"
    cart = cartridge.Cartridge(rom_path)
    assert cart.title == "Pokemon Blue"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == (
        system_mappings.CartType.MBC3
        | system_mappings.CartType.RAM
        | system_mappings.CartType.BATTERY
    )
    assert cart.sgb_flag
    assert not cart.cgb_flag

    rom_path = rom_folder_path / "py.gbc"
    cart = cartridge.Cartridge(rom_path)
    assert cart.title == "Pokemon Yellow"
    assert cart.passes_header_checksum
    assert cart.cartridge_type == (
        system_mappings.CartType.MBC5
        | system_mappings.CartType.RAM
        | system_mappings.CartType.BATTERY
    )
    assert cart.sgb_flag
    assert cart.cgb_flag
