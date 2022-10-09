from bus import Cartridge
import pytest


def test_cartridge_is_tetris():
    rom_path = '../roms/tetris.gb'
    cart = Cartridge(rom_path)
    assert cart.title == 'Tetris'
    assert cart.rom_size == 0x8000
    assert cart.ram_size == 0x00
    assert cart.cartridge_type == 'ROM'
    assert cart.cgb_flag == False
    assert cart.sgb_flag == False
    assert cart.new_licensee_code == 'None'
    assert cart.old_licensee_code == 'Nintendo R&D'
    assert cart.passes_header_checksum == True

    rom_path = '../roms/pb.gb'
    cart = Cartridge(rom_path)
    assert cart.title != 'Tetris'
    assert cart.rom_size != 0x8000
    assert cart.ram_size != 0x00
    assert cart.cartridge_type != 'ROM'
    assert cart.cgb_flag != True
    assert cart.sgb_flag != False
    assert cart.new_licensee_code != 'None'
    assert cart.old_licensee_code != 'Nintendo R&D'
    assert cart.passes_header_checksum != False


if __name__ == "__main__":
    pytest.main()
