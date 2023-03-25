import logging
import sys
from datetime import datetime, timedelta, timezone

from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    def parse(self):
        return [
            "process",
            "timestamp",
            "levelname",
            "module",
            "name",
            "funcName",
            "message",
            "stack_info",
        ]

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            tz = timezone(timedelta(hours=+9), "Asia/Tokyo")
            now = datetime.now(tz)
            log_record["timestamp"] = now


def get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
