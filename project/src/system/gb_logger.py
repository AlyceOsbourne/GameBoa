import logging.handlers
import pathlib

from.config import get_value

logger = logging.getLogger('gb_logger')
logger.setLevel(logging.DEBUG)

fh = logging.handlers.RotatingFileHandler(pathlib.Path(get_value('paths', 'logs')) / 'GameBoa.log', maxBytes=1000000, backupCount=5)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG if get_value('developer', 'debug logging (requires restart)') else logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

