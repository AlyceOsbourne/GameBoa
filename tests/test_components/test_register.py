import functools
import itertools
import unittest
from core.system_mappings import DMGModelRegisterDefaults, CGBModelRegisterDefaults
from components.cpu.register import Register


class TestRegister(unittest.TestCase):

    def _test_reg_8(self, key, register, value):
        self.assertEqual(
            register[f"reg_8_{key}"],
            value,
            f"Key {key} does not match expected value {value}."
        )

    def _test_reg_8_from_16(self, key, register, value):
        self.assertEqual(
            register[f"reg_8_{key[0]}"],
            value >> 8,
            f"Key {key[0]} does not match expected value {value >> 8}."
        )
        self.assertEqual(
            register[f"reg_8_{key[1]}"],
            value & 0xff,
            f"Key {key[1]} does not match expected value {value & 0xff}."
        )

    def _test_reg_16(self, key, register, value):
        self.assertEqual(
            register[f"reg_16_{key}"],
            value,
            f"Key {key} does not match expected value {value}."
        )


    def test_dmg_defaults(self):
        for defaults in DMGModelRegisterDefaults:
            register = Register.from_default(defaults)
            for key, value in defaults._asdict().items():
                self._test_reg_16(key, register, value)

                if key not in ['pc', 'sp']:
                    self._test_reg_8_from_16(key, register, value)

    def test_cgb_defaults(self):
        for defaults in CGBModelRegisterDefaults:
            register = Register.from_default(defaults)
            for key, value in defaults._asdict().items():
                self._test_reg_16(key, register, value)

                if key not in ['pc', 'sp']:
                    self._test_reg_8_from_16(key, register, value)

    def test_value_setting_getting(self):
        register = Register()
        for reg_16 in ['af', 'bc', 'de', 'hl', 'sp', 'pc']: self.assertEqual(register[f"reg_16_{reg_16}"], 0)
        for reg_8 in ['a', 'b', 'c', 'd', 'e', 'h', 'l']: self.assertEqual(register[f"reg_8_{reg_8}"], 0)
        for flag in ['z', 'n', 'h', 'c']: self.assertEqual(register[f"flag_{flag}"], 0)

        for reg in ['af', 'bc', 'de', 'hl']:
            register[f"reg_16_{reg}"] = 0x1234
            self._test_reg_16(reg, register, 0x1234)
            self._test_reg_8_from_16(reg, register, 0x1234)
            register[f"reg_8_{reg[0]}"] = 0x56
            self._test_reg_16(reg, register, 0x5634)
            self._test_reg_8_from_16(reg, register, 0x5634)
            register[f"reg_8_{reg[1]}"] = 0x78
            self._test_reg_16(reg, register, 0x5678)
            self._test_reg_8_from_16(reg, register, 0x5678)


        for reg in ['sp','pc'
        ]:
            register[f"reg_16_{reg}"] = 0x1234
            self._test_reg_16(reg, register, 0x1234)

        for reg in ['a','b','c','d','e','h','l'
        ]:
            register[f"reg_8_{reg}"] = 0x12
            self._test_reg_8(reg, register, 0x12)
            register[f"reg_8_{reg}"] = 0x00
            self._test_reg_8(reg, register, 0x00)

    def test_raises(self):
        register = Register()
        for reg_16 in ['af', 'bc', 'de', 'hl', 'sp', 'pc']:
            with self.assertRaises(ValueError):
                register[f"reg_16_{reg_16}"] = 0x10000

        for reg_8 in ['a', 'b', 'c', 'd', 'e', 'h', 'l']:
            with self.assertRaises(ValueError):
                register[f"reg_8_{reg_8}"] = 0x100

        for flag in ['z','n','h','c']:
            with self.assertRaises(ValueError):
                register[f"flag_{flag}"] = 0x2

    def test_flags(self):
        register = Register()
        self.assertEqual(register.flag_z, 0)
        self.assertEqual(register.flag_n, 0)
        self.assertEqual(register.flag_h, 0)
        self.assertEqual(register.flag_c, 0)

        mappings = {
            "flag_z": 0b10000000,
            "flag_n": 0b01000000,
            "flag_h": 0b00100000,
            "flag_c": 0b00010000,
        }

        for num_permutations in range(1, len(mappings) + 1):
            for permutation in itertools.permutations(mappings, num_permutations):
                expected_value = functools.reduce(lambda x, y: x | y, [mappings[flag] for flag in permutation])
                for flag in mappings:
                    if flag in permutation:
                        register[flag] = 1
                    else:
                        register[flag] = 0
                self.assertEqual(register.reg_8_f, expected_value, "Failed on permutation: {}".format(permutation))
                register.reg_8_f = expected_value
                for flag in mappings:
                    if flag in permutation:
                        self.assertEqual(register[flag], 1, "Failed on permutation: {}".format(permutation))
                    else:
                        self.assertEqual(register[flag], 0, "Failed on permutation: {}".format(permutation))