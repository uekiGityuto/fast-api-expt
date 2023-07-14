import datetime
import logging

import pytz
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        jst_timezone = pytz.timezone("Asia/Tokyo")
        log_record["timestamp"] = datetime.datetime.now(
            jst_timezone).isoformat()
        log_record["level"] = record.levelname.lower()


def setup_logger():
    logger = logging.getLogger()

    logHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        "%(timestamp)s %(level)s %(message)s")
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    return logger
