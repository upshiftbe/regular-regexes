import re
import json
import os

basedir = os.path.dirname(os.path.abspath(__file__))
regexes_file = os.path.join(basedir,'regexes.json')

regexes = open(regexes_file)
regexes_dict = json.load(regexes)


class rre:
    pass

for item in regexes_dict:
    @staticmethod
    def func(search, item=item):
        regex = regexes_dict[item]
        result = re.findall(regex, search)
        return result
    func_name = item
    setattr(rre, func_name, func)