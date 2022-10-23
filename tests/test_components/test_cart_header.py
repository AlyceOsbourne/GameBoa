import array
import unittest
import pathlib
from components.cartridge.cart_header import Header

rom_folder = pathlib.Path.cwd().parent.parent / 'roms'
tetris = rom_folder / 'tetris.gb'
pokemon_blue = rom_folder / 'pb.gb'
pokemon_yellow = rom_folder / 'py.gbc'


def load_rom_from_path(path: pathlib.Path):
    with open(path, 'rb') as rom_file:
        return array.array('B', rom_file.read())


class TestGameBoyCartHeader(unittest.TestCase):

    def test_pokemon_yellow(self):
        # Pokémon Yellow
        rom = load_rom_from_path(pokemon_yellow)
        header = Header.from_array(rom)
        self.assertEqual(header.title, b'POKEMON YEL'.ljust(11, b'\0'))
        self.assertNotEqual(header.title, b'TETRIS'.ljust(11, b'\0'))
        self.assertEqual(header.rom_size, 0x05)
        self.assertNotEqual(header.rom_size, 0x00)
        self.assertEqual(header.ram_size, 0x03)
        self.assertNotEqual(header.ram_size, 0x00)
        self.assertEqual(header.sgb_flag, 0x03)
        self.assertNotEqual(header.sgb_flag, 0x00)

    def test_pokemon_blue(self):
        # Pokémon Blue
        rom = load_rom_from_path(pokemon_blue)
        header = Header.from_array(rom)
        self.assertEqual(header.title, b'POKEMON BLU'.ljust(11, b'\0'))
        self.assertNotEqual(header.title, b'TETRIS'.ljust(11, b'\0'))
        self.assertEqual(header.rom_size, 0x05)
        self.assertNotEqual(header.rom_size, 0x00)
        self.assertEqual(header.ram_size, 0x03)
        self.assertNotEqual(header.ram_size, 0x00)
        self.assertEqual(header.sgb_flag, 0x03)
        self.assertNotEqual(header.sgb_flag, 0x00)
        self.assertEqual(header.cgb_flag, 0x00)
        self.assertNotEqual(header.cgb_flag, 0x80)
        self.assertTrue(header.passes_header_checksum(rom))
        rom[0x0134] = 0x00
        self.assertFalse(header.passes_header_checksum(rom))

    def test_tetris(self):
        # Tetris
        rom = load_rom_from_path(tetris)
        header = Header.from_array(rom)
        self.assertEqual(header.title, b'TETRIS'.ljust(11, b'\0'))
        self.assertNotEqual(header.title, b'POKEMON BLUE'.ljust(11, b'\0'))
        self.assertEqual(header.rom_size, 0x00)
        self.assertNotEqual(header.rom_size, 0x08)
        self.assertEqual(header.ram_size, 0x00)
        self.assertNotEqual(header.ram_size, 0x01)
        self.assertTrue(header.sgb_flag == 0x00)
        self.assertFalse(header.sgb_flag == 0x03)
        self.assertTrue(header.cgb_flag == 0x00)
        self.assertFalse(header.cgb_flag == 0x80)
        self.assertTrue(header.passes_header_checksum(rom))
        rom[0x0134] = 0x00
        self.assertFalse(header.passes_header_checksum(rom))