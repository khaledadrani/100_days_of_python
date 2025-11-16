import logging
import logging.config #you can write dict or config file form
import traceback
make = False
if make:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('data\LOG.log')

    stream_handler.setLevel(logging.WARNING)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

else:
    logging.config.fileConfig("data\logger.conf")
    logger = logging.getLogger("sampleLogger")

ex = False

if ex:
    try:
        logger.info("This is an info")
        logger.warning("This is a warning")
        raise Exception("A mean error")
    except:
        #logger.error("This is an error",exc_info=True) #if we know the error
        logger.error("This is an error",traceback.format_exc())

from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

#roll over after 2KB
handler = RotatingFileHandler("data\LOG.log",maxBytes=2000,backupCount=5)
#timed_handler = TimedRotatingFileHandler("data\\timed_log.log",when="s",interval=5,backupCount=5)

from pythonjsonlogger import jsonlogger

formatter = jsonlogger.JsonFormatter()
from datetime import datetime

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

import time 
for i in range(1000):
    logger.info(f"Hello json number {i}")
    

