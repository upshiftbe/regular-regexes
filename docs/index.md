---
seo_title: "Regular regexes: Python regexes for IDs, IBAN, phones and crypto"
---

# Regular regexes

Ready-made regexes for Python, bundled in one place. The focus is on identifiers useful in
investigations: identity documents, bank and company numbers, payment cards, phones and SIMs,
crypto addresses and seed phrases, vehicles, aircraft, ships, containers and parcels, locations,
messaging and file-share links, keys and tokens, and paths on a phone.

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
`rre` directly, country specific ones under their two letter country code (`rre.be.*`).

Where an identifier has a checksum (IBAN, national number, Luhn, crypto addresses, MRZ, ...) a
match is also [validated](validators.md), so random numbers of the right shape are dropped, and
phone numbers are checked against libphonenumber's numbering plans. Numbers whose bare shape is
too common to tell apart are only matched next to their keyword, which is part of the match:
`rre.nl.bsn("BSN: 999999990")` gives `['BSN: 999999990']`.

## Countries

Every country has its IBAN, BIC, VAT number, phone and mobile numbers, IMSI and ICCID, MRZ,
license plates, addresses and company names, and on top of those:

- [International](regexes/index.md) (`rre.*`): email, URL, IBAN, payment cards and card dumps,
  IMEI, crypto addresses and seed phrases, MRZ, VIN, ship and container numbers, parcel tracking,
  messaging links, API keys, private keys and password hashes
- [Belgium](regexes/be.md) (`rre.be.*`): national and BIS number, enterprise number (KBO), OGM,
  eID card number
- [Germany](regexes/de.md) (`rre.de.*`): Steuer-ID, USt-IdNr, Rentenversicherungsnummer,
  Krankenversichertennummer, Personalausweis, Handelsregister
- [Spain](regexes/es.md) (`rre.es.*`): DNI, NIE, CIF, Seguridad Social number
- [France](regexes/fr.md) (`rre.fr.*`): NIR (sécurité sociale), SIREN, SIRET, numéro fiscal, RIB,
  CNI, and the overseas departments' numbers
- [United Kingdom](regexes/gb.md) (`rre.gb.*`): National Insurance number, NHS number, UTR,
  company number, sort code, driving licence number, postcode
- [Italy](regexes/it.md) (`rre.it.*`): codice fiscale, partita IVA, carta d'identità
- [Luxembourg](regexes/lu.md) (`rre.lu.*`): national number (matricule), RCS number
- [Netherlands](regexes/nl.md) (`rre.nl.*`): BSN, RSIN, KvK number, kenteken, postcode
- [Poland](regexes/pl.md) (`rre.pl.*`): PESEL, NIP, REGON, KRS, NRB, dowód osobisty
- [Romania](regexes/ro.md) (`rre.ro.*`): CNP, CUI, trade register number (ONRC)

National formats overlap (a Belgian 0495 12 34 56 is also a valid Dutch number), so run the
countries that fit the case.

## Adding regexes

Universal regexes go in `regular_regexes/intl/regexes.json`, country specific ones in
`regular_regexes/<country code>/regexes.json`, and their one-line description for this site in
`docs/descriptions/<country code>.json`. A new country folder is picked up automatically, here
too. A regex can be paired with a checksum validator from `regular_regexes/validators.py`:

```json
"iban": {"regex": "...", "validator": "iban"}
```

Tests live in the same layout (`tests/<country code>/test_regexes.py`); run them with `pytest`.
