import struct
import array
from collections import namedtuple

HEADER_FORMAT = (
    ('entrypoint', '4s'),
    ('logo', '48s'),
    ('title', '11s'),
    ('manufacturer_code', '4s'),
    ('cgb_flag', 'B'),
    ('new_licensee_code', '2s'),
    ('sgb_flag', 'B'),
    ('cartridge_type', 'B'),
    ('rom_size', 'B'),
    ('ram_size', 'B'),
    ('destination_code', 'B'),
    ('old_licensee_code', 'B'),
    ('mask_rom_version', 'B'),
    ('header_checksum', 'B'),
    ('global_checksum', 'H'),
)
HEADER_SIZE = sum(struct.calcsize(f[1]) for f in HEADER_FORMAT)
HEADER_START = 0x100
HEADER_END = HEADER_START + HEADER_SIZE

HeaderData = namedtuple('header_struct', [f[0] for f in HEADER_FORMAT])

class Header(HeaderData):
    """The Game Boy cartridge header, is just one part of the cartridge."""
    def __str__(self):
        return 'Header(title={}, rom_size={}, ram_size={}, cgb={}, sgb={}, cartridge_type={}, destination={})'.format(
            getattr(self, 'title').decode('ascii').strip('\0').title(), # the backslash is why the .format
            getattr(self, 'rom_size'),
            getattr(self, 'ram_size'),
            getattr(self, 'cgb_flag'),
            getattr(self, 'sgb_flag'),
            getattr(self, 'cartridge_type'),
            getattr(self, 'destination_code')
        )

    @classmethod
    def from_array(cls, rom: array.array):
        return Header(*struct.unpack_from('<' + ''.join(f[1] for f in HEADER_FORMAT), rom[HEADER_START:HEADER_END]))

    def to_array(self, *keys):
        # will be used for the serialization of save files, namely the title, etc etc
        if keys is None:
            keys = HEADER_FORMAT.keys()
        else:
            for key in keys:
                if key not in HEADER_FORMAT.keys():
                    raise ValueError('Invalid key: {}'.format(key))
        return array.array('B', struct.pack('<' + ''.join(HEADER_FORMAT[key][1] for key in keys), *[getattr(self, key) for key in keys]))


    def passes_header_checksum(self, rom: array.array):
        checksum = 0
        for i in range(0x0134, 0x014D):
            checksum += ~rom[i]
        return checksum & 0xFF == getattr(self, 'header_checksum')

