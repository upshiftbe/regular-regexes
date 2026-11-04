# Regular regexes

Commonly used regexes, bundled in one place, for Python. The focus is on identifiers useful in
investigations: identity documents, bank and company numbers, phones and SIMs, crypto addresses,
vehicles, ships and containers, locations, messaging links and paths on a phone.

Use the search box at the top to find a regex by name or by part of its pattern.

## Install

```bash
pip install regular-regexes
```

## Usage

```python
from regular_regexes import rre

rre.email("mail me at jan@test.com or piet@test.be")  # ['jan@test.com', 'piet@test.be']
rre.be.license_plate("car 1-ABC-123")                 # ['1-ABC-123']
rre.be.iban("BE68 5390 0754 7035")                    # [] (checksum fails)
rre.ios_system_path("/System/Library/PrivateFrameworks/x.caf")  # ['/System/Library/PrivateFrameworks/x.caf']
```

Every function takes a string and returns the list of matched strings. Universal regexes are on
`rre` directly ([International](regexes/intl.md)), country specific ones under their two letter
country code ([Belgium](regexes/be.md): `rre.be.*`).

Where an identifier has a checksum (IBAN, national number, Luhn, crypto addresses, MRZ, ...) a
match is also [validated](validators.md), so random numbers of the right shape are dropped.

## Adding regexes

Universal regexes go in `regular_regexes/intl/regexes.json`, country specific ones in
`regular_regexes/<country code>/regexes.json`. A new country folder is picked up automatically,
here too. A regex can be paired with a checksum validator from `regular_regexes/validators.py`:

```json
"iban": {"regex": "...", "validator": "iban"}
```

Tests live in the same layout (`tests/<country code>/test_regexes.py`); run them with `pytest`.
