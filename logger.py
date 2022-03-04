import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
	'%(log_color)s%(message)s'))

logger = logging.getLogger('example')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
