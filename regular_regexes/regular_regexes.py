import re
import json

regexes_file = open('../regexes/regexes.json')
regexes_dict = json.load(regexes_file)


class rre():
    def email(input):
        email_regex = regexes_dict['email']
        result = re.findall(email_regex, input)
        return result
