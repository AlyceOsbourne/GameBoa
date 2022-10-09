class Flags:
    Z, N, H, C = 0, 0, 0, 0

    def read_flag(self, flag: str):
        if not hasattr(self, flag):
            raise Exception(f'Invalid flag {flag}')
        return getattr(self, flag.lower())

    def read_flags(self, flags: str):
        return [self.read_flag(flag) for flag in flags]

    def write_flag(self, flag: str, value: int):
        if not hasattr(self, flag):
            raise Exception(f'Invalid flag {flag}')
        setattr(self, flag.lower(), value)

    def write_flags(self, flags: str, values: list):
        for flag, value in zip(flags, values):
            self.write_flag(flag, value)

    def __str__(self):
        out = ''
        for key, value in {
            'Z': self.Z,
            'N': self.N,
            'H': self.H,
            'C': self.C,
        }.items():
            out += f'{key}: {value} '
        return out