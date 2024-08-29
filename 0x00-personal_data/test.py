#!/usr/bin/python3
import logging
import re
from filtered_logger import RedactingFormatter

"""text = "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;"
pattren = "(?<=password=).*?(?=;)|(?<=date_of_birth=).*?(?=;)"

text = re.sub(pattren, "*****", text)
print(text)"""

class sub_handel(logging.Handler):
    def __init__(self, level):
        super().__init__(level)

    def emit(self, record):
        return self.format(record)


formater = RedactingFormatter(["password", "email"])
logging.basicConfig(filename='myapp.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
print(logger.level)
handler = sub_handel(logging.INFO)
handler.setFormatter(formater)
logger.addHandler(handler)
logger.info("started")
logger.info("end")
logger.debug("debug")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
