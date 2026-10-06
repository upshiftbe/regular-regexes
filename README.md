# Regular regexes

The goal of this repo is avoid having to look up commonly used regexes, but have them all bundled in a single place.
The focus is on identifiers useful in investigations: identity documents, bank and company numbers, phones and SIMs,
crypto addresses, vehicles, ships and containers, locations and messaging links.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage

Install the package using `pip install rre`

```python
from rre import rre

rre.email("mail me at jan@test.com or piet@test.be")  # ['jan@test.com', 'piet@test.be']
rre.be.license_plate("car 1-ABC-123")                 # ['1-ABC-123']
rre.be.iban("BE68 5390 0754 7035")                    # [] (checksum fails)
```

Every function takes a string and returns the list of matched strings.
Universal regexes are on `rre` directly, country specific ones under their two letter country code.

Where an identifier has a checksum (IBAN, national number, Luhn, crypto addresses, MRZ, ...) the match is also
validated, so random numbers of the right shape are dropped.

## Available regexes

### International (`rre/intl`)

| function | checksum validator |
|---|---|
| `rre.bitcoin_address` | `crypto_address` |
| `rre.bitcoin_private_key` | `base58check` |
| `rre.container_number` | `iso6346` |
| `rre.credit_card` | `luhn` |
| `rre.discord_invite` |  |
| `rre.email` |  |
| `rre.ethereum_address` |  |
| `rre.gps_coordinates` |  |
| `rre.gps_dms` |  |
| `rre.hashtag` |  |
| `rre.iban` | `iban` |
| `rre.iccid` | `luhn` |
| `rre.imei` | `luhn` |
| `rre.imo_number` | `imo` |
| `rre.ip_address` |  |
| `rre.ipv6` | `ipv6` |
| `rre.iso_datetime` |  |
| `rre.litecoin_address` | `crypto_address` |
| `rre.mac_address` |  |
| `rre.md5` |  |
| `rre.mention` |  |
| `rre.monero_address` |  |
| `rre.mrz_id_card` | `mrz_td1` |
| `rre.mrz_passport` | `mrz_td3` |
| `rre.multiple_punctuation` |  |
| `rre.onion_address` |  |
| `rre.password` |  |
| `rre.pgp_block` |  |
| `rre.phone_e164` |  |
| `rre.session_id` |  |
| `rre.sha1` |  |
| `rre.sha256` |  |
| `rre.telegram_link` |  |
| `rre.tron_address` | `base58check` |
| `rre.url` |  |
| `rre.uuid` |  |
| `rre.vin` |  |
| `rre.whatsapp_link` |  |

### Belgium (`rre/be`)

| function | checksum validator |
|---|---|
| `rre.be.amount_eur` |  |
| `rre.be.bancontact_card` | `luhn` |
| `rre.be.bban` | `mod97` |
| `rre.be.bic` |  |
| `rre.be.bis_number` | `be_bis_number` |
| `rre.be.company_name` |  |
| `rre.be.date_numeric` |  |
| `rre.be.date_text` |  |
| `rre.be.domain_be` |  |
| `rre.be.ecli` |  |
| `rre.be.eid_card_number` | `mod97` |
| `rre.be.enterprise_number` | `be_enterprise_number` |
| `rre.be.establishment_number` | `be_enterprise_number` |
| `rre.be.iban` | `iban` |
| `rre.be.iccid` | `luhn` |
| `rre.be.imsi` |  |
| `rre.be.license_plate` |  |
| `rre.be.mobile_number` |  |
| `rre.be.mrz_id_card` | `mrz_td1` |
| `rre.be.mrz_passport` | `mrz_td3` |
| `rre.be.msisdn` |  |
| `rre.be.national_number` | `be_national_number` |
| `rre.be.passport_number` |  |
| `rre.be.phone_number` |  |
| `rre.be.postal_code_city` |  |
| `rre.be.premium_number` |  |
| `rre.be.street_address_fr` |  |
| `rre.be.street_address_nl` |  |
| `rre.be.structured_communication` | `mod97` |
| `rre.be.time` |  |
| `rre.be.vat_number` | `be_enterprise_number` |

## Adding regexes

Universal regexes go in `rre/intl/regexes.json`. Country specific ones go in `rre/<country code>/regexes.json`
(e.g. `rre/be/regexes.json`). A new country folder is picked up automatically.

A regex can be paired with a checksum validator from `rre/validators.py`; matches that fail it are dropped:

```json
"iban": {"regex": "...", "validator": "iban"}
```

Tests live in the same layout: `tests/<country code>/test_regexes.py` and `tests/intl/test_regexes.py`.
Run them with `pytest`.
