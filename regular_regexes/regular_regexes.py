import functools
import json
import re
from pathlib import Path
from types import SimpleNamespace

from . import validators


def _valid_prefix(text, pattern, validator):
    # a greedy match can swallow a trailing word ("BE68 5390 0754 7034 BIC"): drop words from the right,
    # as long as what is left still matches the regex on its own
    while text and pattern.fullmatch(text):
        valid = validator(text)
        # a validator can also return the valid part itself ('' for none): a seed phrase inside a run of words
        if isinstance(valid, str):
            return valid
        if valid:
            return text
        text = text.rpartition(' ')[0]


def _matcher(entry):
    # an entry is a regex string, or {"regex": ..., "validator": <function name in validators.py>}
    if isinstance(entry, str):
        entry = {'regex': entry}
    pattern = re.compile(entry['regex'])
    validator = None
    if 'validator' in entry:
        # any other key is passed on to the validator: {"validator": "phone", "regions": "BE", "kind": "mobile"}
        args = {k: v for k, v in entry.items() if k not in ('regex', 'validator')}
        validator = functools.partial(getattr(validators, entry['validator']), **args)

    def match(text):
        # finditer + group(0): findall would return capture groups instead of the match
        found = (m.group(0) for m in pattern.finditer(text))
        if validator:
            found = (_valid_prefix(f, pattern, validator) for f in found)
        return [f for f in found if f]

    return match


def _load(folder):
    regexes = json.loads((folder / 'regexes.json').read_text(encoding='utf-8'))
    return SimpleNamespace(**{name: _matcher(entry) for name, entry in regexes.items()})


_root = Path(__file__).parent

# intl regexes live on rre itself, country ones under their code: rre.be.license_plate
rre = _load(_root / 'intl')
for _folder in _root.iterdir():
    if _folder.name != 'intl' and (_folder / 'regexes.json').exists():
        setattr(rre, _folder.name, _load(_folder))
