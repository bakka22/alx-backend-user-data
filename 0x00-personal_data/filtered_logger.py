#!/usr/bin/env python3
""" obfuscate log message """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ replace occurrences of certain field values """
    pattren = ""
    for field in fields:
        pattren += f"(?<={field}=).*?(?={separator})|"
    return re.sub(pattren[:-1], redaction, message)
