---
seo_title: "Checksum validators: Luhn, IBAN, MRZ, Base58Check - Regular regexes"
description: "How Regular regexes checks a match: Luhn, IBAN mod 97, national ID checksums, MRZ check digits, Base58Check, Bech32, ISO 6346, IMO, BIP39 and libphonenumber."
---

# Checksum validators

A regex can name a validator from `regular_regexes/validators.py`. Every match of the regex is
passed to it, and one that fails is dropped. When a greedy match swallowed a trailing word
("BE68 5390 0754 7034 BIC"), words are dropped from the right until what is left validates.
A validator can also return the valid part of the match itself: that is how a seed phrase is cut
out of a longer run of words. Any other key in a regex's entry is passed on to its validator:
`{"regex": "...", "validator": "phone", "regions": "BE", "kind": "mobile"}`.

## phone
Phone numbers, against [libphonenumber](https://github.com/google/libphonenumber)'s numbering plans
(the `phonenumbers` package): the number must be valid in one of the `regions` (any region when none
are given) and be of the `kind` asked: `mobile`, `premium` (premium rate and shared cost) or `msisdn`
(a mobile number in international format without its +). A national number is read as one of each
region in turn, so `rre.fr.*` also finds the overseas departments' 0690 ... numbers.

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

## nl_bsn
Dutch citizen service number (BSN) and the RSIN of legal entities, the 11-proef: the nine digits weighted
9 down to 2 and the last one -1, the sum divisible by 11.

## nl_vat_number
Dutch VAT number (NL, nine digits, B, two digits other than 00): the nine digits pass the 11-proef (btw-nummer
built on an RSIN or BSN), or the whole number is 1 mod 97 with letters as numbers (btw-id, since 2020).

## fr_nir
French social security number (NIR): the last two digits are 97 minus the first thirteen mod 97, with Corsica's
2A and 2B counted as 19 and 18.

## fr_siret
French SIRET: Luhn over the fourteen digits and over the SIREN they start with. La Poste's establishments (SIREN
356 000 000, except the head office) instead have digits that add up to a multiple of 5.

## fr_vat_number
French VAT number: FR, a two-character key and the SIREN (Luhn, except Monaco's numbers starting with 000). A numeric
key is (12 + 3 × SIREN) mod 97; a key with a letter (no I or O) passes a mod 11 check against the SIREN.

## fr_rib
French bank details (RIB): the two-digit key is 97 minus (89 × bank code + 15 × branch code + 3 × account number)
mod 97, with letters in the account number counted as digits (A to I and J to R as 1 to 9, S to Z as 2 to 9).

## fr_numero_fiscal
French tax number (numéro fiscal, SPI): the last three digits are the first ten mod 511.

## fr_mrz_id_card
French ID card MRZ: `mrz_td1` for the 2021 card. The older card (two lines of 36) is matched on its second line, where
the card number and the date of birth are each followed by their check digit.

## de_tax_id
German tax identification number (Steuer-IdNr): the last digit is the ISO 7064 MOD 11,10 check digit, and in
the first ten digits exactly one digit occurs twice or three times, but never three times in a row.

## de_vat_number
German VAT number (USt-IdNr): the ninth digit is the ISO 7064 MOD 11,10 check digit of the first eight.

## de_pension_insurance_number
German pension insurance number (Versicherungsnummer): with the letter replaced by its position in the alphabet
(two digits), the first twelve digits are weighted 2, 1, 2, 5, 7, 1, 2, 1, 2, 1, 2, 1, and the sum of the
products' digit sums, mod 10, is the check digit.

## de_health_insurance_number
German health insurance number (KVNR, the part printed on the card): with the letter replaced by its position in
the alphabet (two digits), the ten digits are weighted 1, 2, 1, 2, ..., and the sum of the products' digit sums,
mod 10, is the check digit.

## lu_national_number
Luxembourg national identification number (matricule): birth date and a three-digit sequence, then a Luhn and a
Verhoeff check digit, both over those first eleven digits. An unknown birth month or day is written as 00.

## lu_vat_number
Luxembourg VAT number (TVA): the first six digits mod 89 are the last two.

## gb_nhs_number
UK NHS number: the first nine digits weighted 10 down to 2; 11 minus the sum mod 11 is the tenth digit
(11 counts as 0, and a result of 10 is never issued).

## gb_utr
UK Unique Taxpayer Reference: the last nine digits weighted 6, 7, 8, 9, 10, 5, 4, 3, 2; 11 minus the sum
mod 11 is the first digit, with 10 and 11 written as 1 and 2.

## gb_vat_number
UK VAT registration number: the first seven digits weighted 8 down to 2, plus the last two, is a multiple
of 97, or 42 more than one for the "9755" series issued from November 2009 (which does not start with 0).
A branch suffix is not checked; government department (GD) and health authority (HA) numbers have no check digits.

## es_nif
Spanish NIF: a DNI, an NIE (X, Y, Z read as 0, 1, 2) or a K/L/M number ends in the letter of the number mod 23
(`TRWAGMYFPDXBNJZSQVHLCKE`); a company CIF ends in a control digit computed from its seven digits, or the letter at
that place in `JABCDEFGHI`. Also used for the VAT number (ES in front).

## es_nss
Spanish social security number (NSS/NAF): the last two digits are the province and number mod 97; a number below
10 000 000 (an old seven-digit number) is counted without its leading zero.

## it_codice_fiscale
Italian codice fiscale: the check letter (odd positions through a table, even positions by value, sum mod 26) and a
real birth date, with the omocodia letters `LMNPQRSTUV` read as digits and 40 added to the day for women.

## it_partita_iva
Italian partita IVA, also inside the VAT number: a Luhn check digit, an office code from 001 to 100 or 120, 121, 888,
999, and a number that is not all zeros.

## pl_pesel
Polish PESEL: the eleven digits weighted 1, 3, 7, 9 repeated (1 for the check digit) sum to a multiple of 10, and
the first six are a real birth date, the month raised by 20, 40, 60 or 80 for the 2000s, 2100s, 2200s or 1800s.

## pl_nip
Polish NIP (tax number, also inside a `PL` VAT number): the first nine digits weighted 6, 5, 7, 2, 3, 4, 5, 6, 7,
the sum mod 11 is the tenth digit.

## pl_regon
Polish REGON: nine digits weighted 8, 9, 2, 3, 4, 5, 6, 7, or fourteen weighted 2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8
whose first nine are a valid REGON themselves; the sum mod 11 is the check digit, 10 counting as 0.

## pl_document_number
Polish ID card (three letters, six digits) and passport (two letters, seven digits) numbers: the first digit is the
ICAO 9303 check digit (weights 7, 3, 1) of the letters and the digits after it.

## pl_nrb
Polish domestic account number (NRB, 26 digits): `iban` with `PL` put in front.

## ro_cnp
Romanian CNP: the first twelve digits weighted 2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9, the sum mod 11 is the last digit
(10 gives 1). Digits 2 to 7 are a real birth date, in the century the first digit gives, and digits 8 and 9 a county
code (01-48, 51, 52, or 70 for numbers from the national system).

## ro_cui
Romanian CUI/CIF company code (also inside an `RO` VAT number): the digits before the check digit, right-aligned under
7, 5, 3, 2, 1, 7, 5, 3, 2, give a sum whose tenfold mod 11 mod 10 is the check digit.

## ro_onrc
Romanian trade register number. The old `J40/1234/2020` needs a county code (1-40, 51, 52) and a year up to 2024. The
new `J2025000001004` (registration year, serial, county: 00 for registrations since 26 July 2024) ends in a check
digit: the letter's ASCII code plus the twelve digits, mod 10.

## ro_mrz_id_card
Romanian identity card MRZ: `mrz_td1` for line 1 of the electronic card, `mrz_td3`'s three check digits for line 2
of the older card's 36-character zone (TD2), where they sit at the same places.

## bip39
BIP39 seed phrases: 12, 15, 18, 21 or 24 words of the English word list in a row, whose last bits are the
start of the SHA-256 of the rest. It returns the first valid phrase in a run of words (the longest one where
several start at the same word), or nothing.

## ripple_base58check
XRP Ledger addresses (`r...`): Base58Check with Ripple's own alphabet.

## card_pan
Luhn over the card number at the start of magnetic stripe track data and card dumps.

## lei
Legal Entity Identifiers (ISO 17442): letters as numbers (A=10 ... Z=35), the whole mod 97 is 1 (ISO 7064 mod 97-10).

## isin
ISINs (ISO 6166): letters as numbers (A=10 ... Z=35), then Luhn over the digits.

## gtin
EAN-8, UPC-A (12), EAN-13 and GTIN-14 product codes: the digits weighted 1, 3, 1, 3 ... from the right, check digit
included, add up to a multiple of 10.

## isbn
ISBN-13 (978 or 979) as `gtin`; ISBN-10 weighted 10 down to 1, X as 10, a multiple of 11.

## upu_s10
UPU S10 postal item numbers (`RR123456785BE`): the eight serial digits weighted 8 6 4 2 3 5 9 7, the check digit is
11 minus the sum mod 11, with 10 as 0 and 11 as 5.

## ups_1z
UPS `1Z` tracking numbers: the 15 characters after `1Z`, letters as (code point - 63) mod 10, odd positions plus
twice the even ones; the check digit brings the sum to a multiple of 10.

## air_waybill
IATA air waybill numbers: after the 3-digit airline prefix, the 7-digit serial mod 7 is the last digit.

## jwt
A JSON Web Token (RFC 7519): the header, before the first dot, decodes from base64url to a JSON
object with an `alg` field.

## mac_address
MAC addresses that are not a placeholder for one: `02:00:00:00:00:00` (what Android 6 and later and iOS 7 and later
give apps instead of the real address), all zeros and all `ff` (broadcast), in any case and with any separator.

## meid
CDMA mobile equipment identifiers (MEID, 3GPP2 X.S0008): 14 hexadecimal digits starting from `A0`, or all decimal (the
first 14 digits of an IMEI), or the 18-digit decimal form, whose manufacturer code (the first 10 digits) is at most
4294967295 and serial number (the last 8) at most 16777215. An optional check digit is Luhn, in base 16 when the
hexadecimal form has letters.

## mcc_mnc
Mobile network codes: the country code (MCC) is one of ITU-T E.212's mobile country codes, 001 (test networks), or 289
(Abkhazia) or 995 (British Indian Ocean Territory), which are in use but not listed by the ITU. The network code (MNC) is
not checked: new ones are assigned every month.

## app_package_name
Android package names and iOS bundle IDs. A file extension at the end is cut off (`com.apple.mobilesafari.plist`, also
`_preferences.xml`), and a name ending in a generic top-level domain (`.com`, `.org`, `.net`, ...) is a web address. A
name can have just two parts after `com` or `org` (the second of three characters or more, so not `com.au`); others need
three, do not end in a two-letter country code (`ec.europa.eu`, `app.example.io`) and have a part of five characters or
more (`ch.threema.app`, not words joined by dots like `il.fait.beau`).

## unix_timestamp
A Unix time, the last number in the match: seconds (9 or 10 digits) or milliseconds (12 or 13) since 1 January 1970
UTC, from the start of 2000 to the end of 2040.

## exif_gps_rational
EXIF GPS latitude or longitude as three rationals (degrees, minutes, seconds): minutes and seconds below 60, and the
whole at most 180 degrees.

## solana_address
Solana addresses: the base58 word that ends the match, after its keyword, decodes to 32 bytes, the size of an ed25519
public key.

## dogecoin_address
`base58check`, with Dogecoin's version byte: 30 for a P2PKH address (`D...`), 22 for a P2SH address (`9...` or `A...`).

## cashaddr
Bitcoin Cash CashAddr addresses: all lowercase or all uppercase, and the 40-bit BCH checksum over the lower five bits
of the prefix's letters (`bitcoincash` when the address is written without it), a zero and the payload.

## dhl
DHL tracking numbers after the keyword: in an Express waybill (10 digits) the first nine mod 7 are the last digit; a
12-digit DHL Paket number (Identcode) has its first eleven digits weighted 4, 9, 4, 9 ... and a check digit that brings
the sum to a multiple of 10; a 20-digit one is an SSCC, checked like `gtin`. JJD and JVGL numbers have no check digit.

## dpd
DPD parcel numbers: the check character printed after the 14 digits is ISO 7064 MOD 37,36 (0-9, then A-Z for 10-35).
A number written without it is not checked.

## gls
GLS parcel numbers: a twelfth digit is the check digit, GS1 mod 10 (weights 3, 1, 3 ... from the rightmost digit) with
1 added to the sum. An 11-digit number is not checked.

## cardano_address
Cardano addresses: `bech32` for Shelley addresses (`addr1...`, `stake1...`), longer than its usual 90 characters. A
Byron address (`Ae2...`, `DdzFF...`) is the base58 of a CBOR array of the address bytes, tagged 24, and their CRC32.

## ss58
Polkadot's SS58 addresses: the base58 of a prefix byte (0 for Polkadot, 2 for Kusama, 42 for generic Substrate), the
32-byte account and two checksum bytes, the start of the BLAKE2b-512 hash of `SS58PRE`, the prefix and the account.

## stellar_strkey
Stellar addresses (SEP-23 strkey): the base32 of a version byte, the key (and a muxed account's 8-byte ID) and their
CRC16-XModem, little-endian, written without padding and with unused trailing bits zero.

## zcash_address
`base58check` for transparent Zcash addresses (`t1...`, `t3...`), `bech32` (Bech32m for unified addresses) for Sapling
(`zs1...`) and unified (`u1...`) addresses, without the 90-character limit.

## dash_address
`base58check`, with Dash's version byte: 76 for a P2PKH address (`X...`), 16 for a P2SH address (`7...`).

## ton_address
TON user-friendly addresses: the base64 or base64url of a flag byte, the workchain, the 32-byte account and the
CRC16-XModem of those 34 bytes, big-endian.

## tox_id
Tox IDs (76 hexadecimal characters): the last two bytes are the XOR of the public key and nospam taken two bytes at a
time, and the 64-character public key has more than eight different hexadecimal digits, so a run of zeros or other
filler, whose XOR is also 0000, is dropped.

## bitlocker_recovery_key
BitLocker recovery passwords: each of the eight blocks of six digits is a 16-bit number times 11, so it is divisible by
11 and below 720896. Eight equal blocks (`000000-000000-...`) are a placeholder.

## mac_absolute_time
Mac absolute time (Cocoa, Core Data): the last number in the match is seconds since 1 January 2001 UTC, or nanoseconds
when it has 18 digits or more, and falls between the start of 2000 and the end of 2040.

## webkit_timestamp
WebKit and Chrome time: the last number in the match is microseconds since 1 January 1601 UTC, and falls between the
start of 2000 and the end of 2040.

## windows_filetime
Windows FILETIME, also Active Directory's LDAP timestamps: the last number in the match, decimal or `0x` hexadecimal,
is 100-nanosecond intervals since 1 January 1601 UTC, and falls between the start of 2000 and the end of 2040.

## cidr
A valid IPv4 or IPv6 network and prefix length, by Python's `ipaddress`. The address may have host bits set
(`192.168.1.10/24`: an interface's address with the length of its network's prefix).

## asn
Autonomous system numbers: 32 bits, without 0 and 4294967295, which are reserved.

## eid
eSIM EIDs (GSMA SGP.29): the 32 digits mod 97 are 1 (ISO 7064 mod 97-10, as in an IBAN).

## bcbp
IATA boarding pass barcodes (BCBP, Resolution 792): after the first 23 characters (`M`, the number of legs, the name
and the e-ticket flag), each leg takes 37 characters that end in the hexadecimal size of its variable part, with a
flight date from day 001 to 366; security data after `^` gives its own size. The barcode is cut where those sizes say it ends, so text after it on the line is left out.

## fedex
FedEx tracking numbers after the keyword: in an Express number (12 digits) the first eleven are weighted 3, 1, 7, 3, 1,
7 ..., and the sum mod 11 mod 10 is the last digit; a Ground number (15 digits, also the end of a 22-digit one starting
with 96) is checked like `gtin`.

## usps
USPS tracking numbers, checked like `gtin`; a 20-digit number is printed without its application identifier 91, which
counts in the sum.

## iso11649
RF creditor references (ISO 11649): `RF` and the check digits moved to the end, letters as numbers (A=10 ... Z=35), the
whole mod 97 is 1, as in an IBAN.

## sepa_creditor_id
SEPA creditor identifiers: `iso11649` over the country code, the check digits and the national identifier, leaving out
the creditor business code (`ZZZ`).
