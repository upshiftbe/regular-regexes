import re
import json

regexes_file = open('../regexes/regexes.json')
regexes_dict = json.load(regexes_file)


class rre():
    for item in regexes_dict:
        def f(item=item):
            regex = regexes_dict[item]
            result = re.findall(regex, input)
            return result
