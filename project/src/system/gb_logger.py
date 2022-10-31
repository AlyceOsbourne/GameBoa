from pathlib import Path
from logging.handlers import RotatingFileHandler
from logging import DEBUG, Formatter, getLogger, INFO, StreamHandler
from .config import get_value

logger = getLogger("gb_logger")
logger.setLevel(DEBUG)

file_handler = RotatingFileHandler(
    Path(get_value("paths", "logs")) / "GameBoa.log", maxBytes=1_000_000, backupCount=5
)
file_handler.setLevel(DEBUG)

stream_handler = StreamHandler()
stream_handler.setLevel(
    DEBUG if get_value("developer", "debug logging") else INFO
)

formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

