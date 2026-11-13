# Regular regexes

The goal of this repo is avoid having to look up commonly used regexes, but have them all bundled in a single place.
The focus is on identifiers useful in investigations: identity documents, bank and company numbers, payment cards,
phones and SIMs, crypto addresses and seed phrases, vehicles, aircraft, ships, containers and parcels, locations,
messaging and file-share links, keys and tokens.

[![Docs](https://img.shields.io/badge/docs-regexes.upshift.be-blue)](https://regexes.upshift.be/)
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

`rre.ios_system_path` and `rre.android_system_path` take a path on the device and match
it when it lies in a folder the OS keeps for itself (read-only, the same on every phone of a version, nothing the user
made): iOS's system volume (`/System/`, `/Library/`, `/Applications/`, `/Developer/`, `/usr/`, `/bin/`, `/sbin/`) and
`/private/preboot/Cryptexes/`; Android's `/system/`, `/system_ext/`, `/system_root/`, `/product/`, `/vendor/`, `/odm/`,
`/oem/`, `/apex/`, `/bin/`, `/sbin/`. Only at the start of the path, case-sensitive: `/data/system/...` or
`/private/var/mobile/Library/...` (user data) do not match. `rre.ios_app_bundle_path` does the same for the folder where
iOS installs apps, `/private/var/containers/Bundle/`: what the app ships, not what the user made in it (that is in
`/private/var/mobile/Containers/Data/Application/...`, which does not match).

Three more match folders in the user's data where the audio is not the user's own: `rre.speech_synthesis_path` (text-to-speech
caches and voices: `Library/Caches/tts/` in an iOS app's data, Android's `com.google.android.tts`, a navigation app's
`tts/` or `voice/` folder), `rre.app_sound_path` (an app's notification and effect sounds: `Library/Sounds/` in an iOS
app's data, a navigation app's `sound/` folder) and `rre.ios_voice_trigger_path` (`/private/var/mobile/Library/VoiceTrigger/`,
the owner's recordings of the assistant's wake phrase). Exact folders only: an app's cache as such does not match.

Two more match files an app keeps for itself, by a layout exact enough to tell them from the user's own: `rre.cocos_asset_path`
(a Cocos game's artwork and sounds, `assets/<bundle>/native/<two hex digits>/<uuid>.<extension>`) and `rre.gurd_cache_path`
(`Library/Application Support/gurd_cache/` in an iOS app's data: downloaded animation frames, effects and stickers).

```python
rre.ios_system_path("/System/Library/PrivateFrameworks/x.caf")  # ['/System/Library/PrivateFrameworks/x.caf']
rre.android_system_path("/data/system/usagestats/0")            # []
```
Universal regexes are on `rre` directly, country specific ones under their two letter country code: `be`, `de`, `es`,
`fr`, `gb` (United Kingdom), `it`, `lu`, `nl`, `pl` and `ro`. National formats overlap (a Belgian 0495 12 34 56 is
also a valid Dutch number), so run the countries that fit the case.

Where an identifier has a checksum (IBAN, national number, Luhn, crypto addresses, MRZ, ...) the match is also
validated, so random numbers of the right shape are dropped. Phone numbers are checked against libphonenumber's
numbering plans (the `phonenumbers` package, installed along). Numbers whose bare shape is too common to tell apart are
only matched next to their keyword, which is part of the match:

```python
rre.nl.bsn("BSN: 999999990, bare 999999990")  # ['BSN: 999999990']
```

## Available regexes

All regexes, their patterns and checksum validators, with search:
**[regexes.upshift.be](https://regexes.upshift.be/)**.
The site is generated from the `regexes.json` files and their descriptions in `docs/descriptions/`, and Netlify
publishes it on every push to `main`; to preview it locally:

```bash
pip install -r docs/requirements.txt
mkdocs serve
```

## Adding regexes

Universal regexes go in `regular_regexes/intl/regexes.json`. Country specific ones go in `regular_regexes/<country code>/regexes.json`
(e.g. `regular_regexes/be/regexes.json`). A new country folder is picked up automatically. For the documentation
site, a regex also needs a one-line description in `docs/descriptions/<country code>.json` and a category in
`docs/categories.json`; the docs build fails without them.

A regex can be paired with a checksum validator from `regular_regexes/validators.py`; matches that fail it are dropped:

```json
"iban": {"regex": "...", "validator": "iban"}
```

A validator returns whether the match is valid, or the valid part of it as a string (how a seed phrase is cut out of a
longer run of words), and never raises. Any other key in the entry is passed on to the validator
(`"validator": "phone", "regions": "BE", "kind": "mobile"`). A data file it needs (like the BIP39 word list) also goes
in `package_data` in `setup.cfg`.

Tests live in the same layout: `tests/<country code>/test_regexes.py` and `tests/intl/test_regexes.py`.
Run them with `pytest`, after `pip install -e .` (which also installs `phonenumbers`).
Every regex has at least six matching and six non-matching cases. The suite also runs every match through every
other regex: when two regexes match the same text, `tests/overlaps.json` must say why that is inherent, or the run
fails. After a deliberate change, `pytest --overlaps-update` rewrites that file; fill in the reason of new pairs.
