#!/usr/bin/env python3
""" obfuscate log message """
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ replace occurrences of certain field values """
    pattren = ""
    for field in fields:
        pattren += f"(?<={field}=).*?(?={separator})|"
    return re.sub(pattren[:-1], redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records """
        new = record
        new.msg = filter_datum(self.fields, self.REDACTION,
                               record.msg, self.SEPARATOR)
        return super().format(new)
