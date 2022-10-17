import logging


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

_file_handler = logging.FileHandler("debug.log")
_file_handler.setLevel(logging.DEBUG)

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.DEBUG)

_logging_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

_file_handler.setFormatter(_logging_formatter)
_stream_handler.setFormatter(_logging_formatter)

LOGGER.addHandler(_file_handler)
LOGGER.addHandler(_stream_handler)
