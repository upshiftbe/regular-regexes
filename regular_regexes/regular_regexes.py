import re


class rre():
    def email(input):
        email_regex = "[^@]+@[^@]+\.[^@]+"
        result = re.findall(email_regex, input)
        return result
