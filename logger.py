import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
_fh = logging.FileHandler("components/bus/debug.log")
_fh.setLevel(logging.DEBUG)
_ch = logging.StreamHandler()
_ch.setLevel(logging.DEBUG)
_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_fh.setFormatter(_formatter)
_ch.setFormatter(_formatter)
LOGGER.addHandler(_fh)
LOGGER.addHandler(_ch)
