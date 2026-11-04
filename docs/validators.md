# Checksum validators

A regex can name a validator from `regular_regexes/validators.py`. Every match of the regex is
passed to it, and one that fails is dropped. When a greedy match swallowed a trailing word
("BE68 5390 0754 7034 BIC"), words are dropped from the right until what is left validates.

## luhn
The Luhn check digit (mod 10): payment cards, IMEI, ICCID.

## iban
ISO 13616: the country code and check digits moved to the end, letters as numbers, the whole mod 97 is 1.

## mod97
The last two digits are the rest mod 97 (97 when that is 0): Belgian eID card numbers, old account
numbers (BBAN), structured communications (OGM/VCS).

## be_national_number
Belgian national register number: the last two digits are 97 minus the first nine mod 97, with a
2 put in front for people born from 2000 on.

## be_bis_number
Belgian BIS number: a national register number whose month is raised by 20 or 40.

## be_enterprise_number
Belgian enterprise (KBO/BCE) and VAT number: the last two digits are 97 minus the first eight mod 97.

## mrz_td1
The machine-readable zone of an ID card (ICAO 9303 TD1): the document number's check digit,
including the longer numbers that continue in the optional field (Belgian eID).

## mrz_td3
The machine-readable zone of a passport (ICAO 9303 TD3): the check digits of the document number,
the date of birth and the expiry date.

## ipv6
A valid IPv6 address, by Python's `ipaddress`.

## base58check
Base58Check: the last four bytes are the double SHA-256 of the rest. Legacy Bitcoin, Litecoin and
Tron addresses, and WIF private keys.

## bech32
Bech32 and Bech32m checksums (BIP 173, BIP 350): SegWit addresses (`bc1...`, `ltc1...`).

## crypto_address
`bech32` for `bc1`/`ltc1` addresses, `base58check` otherwise.

## iso6346
ISO 6346 container numbers: the weighted sum of owner code and serial, mod 11, mod 10, is the check digit.

## imo
IMO ship numbers: the first six digits weighted 7 to 2, the sum's last digit is the seventh.
