# Regular regexes

The goal of this repo is avoid having to look up commonly used regexes, but have them all bundled in a single place.
The focus is on identifiers useful in investigations: identity documents, bank and company numbers, phones and SIMs,
crypto addresses, vehicles, ships and containers, locations and messaging links.

[![Docs](https://img.shields.io/badge/docs-regexes-blue)](https://upshiftbe.github.io/regular-regexes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage

Install the package using `pip install regular-regexes`

```python
from regular_regexes import rre

rre.email("mail me at jan@test.com or piet@test.be")  # ['jan@test.com', 'piet@test.be']
rre.be.license_plate("car 1-ABC-123")                 # ['1-ABC-123']
rre.be.iban("BE68 5390 0754 7035")                    # [] (checksum fails)
```

Every function takes a string and returns the list of matched strings.

`rre.ios_system_path` and `rre.android_system_path` take a path on the device, as forensic tools report it, and match
it when it lies in a folder the OS keeps for itself (read-only, the same on every phone of a version, nothing the user
made): iOS's system volume (`/System/`, `/Library/`, `/Applications/`, `/Developer/`, `/usr/`, `/bin/`, `/sbin/`) and
`/private/preboot/Cryptexes/`; Android's `/system/`, `/system_ext/`, `/system_root/`, `/product/`, `/vendor/`, `/odm/`,
`/oem/`, `/apex/`, `/bin/`, `/sbin/`. Only at the start of the path, case-sensitive: `/data/system/...` or
`/private/var/mobile/Library/...` (user data) do not match.

```python
rre.ios_system_path("/System/Library/PrivateFrameworks/x.caf")  # ['/System/Library/PrivateFrameworks/x.caf']
rre.android_system_path("/data/system/usagestats/0")            # []
```
Universal regexes are on `rre` directly, country specific ones under their two letter country code.

Where an identifier has a checksum (IBAN, national number, Luhn, crypto addresses, MRZ, ...) the match is also
validated, so random numbers of the right shape are dropped.

## Available regexes

All regexes, their patterns and checksum validators, with search:
**[upshiftbe.github.io/regular-regexes](https://upshiftbe.github.io/regular-regexes/)**.
The site is generated from the `regexes.json` files on every push to `main`; to preview it locally:

```bash
pip install -r docs/requirements.txt
mkdocs serve
```

## Adding regexes

Universal regexes go in `regular_regexes/intl/regexes.json`. Country specific ones go in `regular_regexes/<country code>/regexes.json`
(e.g. `regular_regexes/be/regexes.json`). A new country folder is picked up automatically.

A regex can be paired with a checksum validator from `regular_regexes/validators.py`; matches that fail it are dropped:

```json
"iban": {"regex": "...", "validator": "iban"}
```

Tests live in the same layout: `tests/<country code>/test_regexes.py` and `tests/intl/test_regexes.py`.
Run them with `pytest`.
