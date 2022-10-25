from pprint import pprint
from typing import Callable

from components.instruction import Instruction, Decoder, load_decoder
from functools import singledispatchmethod, cache



