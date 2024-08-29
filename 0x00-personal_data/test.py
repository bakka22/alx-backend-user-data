#!/usr/bin/python3

import re

text = "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;"
pattren = "(?<=password=).*?(?=;)|(?<=date_of_birth=).*?(?=;)"

text = re.sub(pattren, "*****", text)
print(text)
