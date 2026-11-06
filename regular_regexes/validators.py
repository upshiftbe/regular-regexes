import base64
import hashlib
import ipaddress
import json
import re
import string

import phonenumbers


def _digits(text):
    return re.sub(r'\D', '', text)


def luhn(text):
    digits = [int(d) for d in reversed(_digits(text))]
    return (sum(digits[0::2]) + sum(sum(divmod(2 * d, 10)) for d in digits[1::2])) % 10 == 0


def iban(text):
    s = re.sub(r'\s', '', text)
    # shortest IBAN (Norway) is 15 characters
    return len(s) >= 15 and int(''.join(str(int(c, 36)) for c in s[4:] + s[:4])) % 97 == 1


def be_national_number(text):
    d = _digits(text)
    # born from 2000 on: a 2 is prefixed before the mod 97
    return int(d[9:]) in (97 - int(d[:9]) % 97, 97 - int('2' + d[:9]) % 97)


def be_enterprise_number(text):
    d = _digits(text)
    return 97 - int(d[:8]) % 97 == int(d[8:])


def mod97(text):
    # last two digits = the rest mod 97, 97 when that is 0 (eID card, old account number, OGM)
    d = _digits(text)
    return (int(d[:-2]) % 97 or 97) == int(d[-2:])


def be_bis_number(text):
    # bis number: national number with month +20 or +40
    month = int(_digits(text)[2:4])
    return (20 <= month <= 32 or 40 <= month <= 52) and be_national_number(text)


def _icao_check(field):
    weights = (7, 3, 1)
    return sum((0 if c == '<' else int(c, 36)) * weights[i % 3] for i, c in enumerate(field)) % 10


def mrz_td1(line):
    # ID card line 1: document number at 5-13, check digit at 14. A longer number (Belgian eID has 12 digits)
    # puts '<' at 14 and continues in the optional field, followed by its check digit.
    doc, check = line[5:14], line[14]
    if check == '<':
        extra = line[15:].split('<')[0]
        doc, check = doc + extra[:-1], extra[-1:]
    return check.isdigit() and _icao_check(doc) == int(check)


def mrz_td3(line):
    # passport line 2: document number, birth date and expiry date each followed by their check digit
    return all(_icao_check(line[a:b]) == int(line[b]) for a, b in ((0, 9), (13, 19), (21, 27)))


def ipv6(text):
    try:
        ipaddress.IPv6Address(text)
        return True
    except ValueError:
        return False


_BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base58check(text):
    # bitcoin/litecoin/tron legacy addresses and WIF keys: last 4 bytes = double sha256 of the rest
    n = 0
    for c in text:
        n = n * 58 + _BASE58.index(c)
    raw = b'\0' * (len(text) - len(text.lstrip('1'))) + n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:]


def bech32(text):
    # segwit addresses (bc1..., ltc1...): BIP173 / BIP350 checksum
    hrp, _, data = text.lower().rpartition('1')
    values = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]
    values += ['qpzry9x8gf2tvdw0s3jn54khce6mua7l'.index(c) for c in data]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i, g in enumerate((0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3)):
            chk ^= g if (top >> i) & 1 else 0
    return chk in (1, 0x2bc830a3)  # bech32, bech32m


def crypto_address(text):
    return bech32(text) if text.lower().startswith(('bc1', 'ltc1')) else base58check(text)


_ISO6346 = dict(zip(string.ascii_uppercase, (v for v in range(10, 39) if v % 11)))


def iso6346(text):
    # container number: weighted sum of owner code + serial, mod 11, mod 10 = check digit
    s = re.sub(r'[^A-Z0-9]', '', text.upper())
    total = sum((int(c) if c.isdigit() else _ISO6346[c]) * 2 ** i for i, c in enumerate(s[:10]))
    return total % 11 % 10 == int(s[10])


def imo(text):
    d = _digits(text)
    return sum(int(c) * w for c, w in zip(d, range(7, 1, -1))) % 10 == int(d[6])


def nl_bsn(text):
    # BSN and RSIN, the 11-proef: digits weighted 9 down to 2, the last one -1, the sum divisible by 11
    d = _digits(text)
    return len(d) == 9 and int(d) > 0 and sum(int(c) * w for c, w in zip(d, (9, 8, 7, 6, 5, 4, 3, 2, -1))) % 11 == 0


def nl_vat_number(text):
    # NL + 9 digits + B + 2 digits (not 00). The btw-nummer has the RSIN or BSN as its 9 digits; the btw-id of
    # sole proprietors (since 2020) is 1 mod 97 as a whole, letters as numbers (N=23, L=21, B=11)
    s = re.sub(r'[\s.]', '', text).upper()
    return s[-2:] != '00' and (nl_bsn(s[2:11]) or int(''.join(str(int(c, 36)) for c in s)) % 97 == 1)


def fr_nir(text):
    # French social security number: key = 97 - the first 13 digits mod 97, Corsica's 2A/2B counted as 19/18
    s = re.sub(r'\s', '', text)
    n = s[:5] + {'2A': '19', '2B': '18'}.get(s[5:7], s[5:7]) + s[7:13]
    return n.isdigit() and s[13:].isdigit() and 97 - int(n) % 97 == int(s[13:])


def fr_siret(text):
    d = _digits(text)
    # La Poste's establishments (SIREN 356 000 000) have digits summing to a multiple of 5, except the head office
    if d[:9] == '356000000' and d != '35600000000048':
        ok = sum(int(c) for c in d) % 5 == 0
    else:
        ok = luhn(d)
    return ok and luhn(d[:9])


_FR_VAT_KEY = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'  # no I or O


def fr_vat_number(text):
    s = re.sub(r'\s', '', text)
    key, siren = s[2:4], s[4:]
    # a SIREN starting with 000 is no SIREN (Monaco): no Luhn there
    if not (luhn(siren) or siren.startswith('000')):
        return False
    if key.isdigit():
        return int(key) == (12 + 3 * int(siren)) % 97
    # new-style key, with a letter
    c1, c2 = (_FR_VAT_KEY.index(c) for c in key)
    total = c1 * 24 + c2 - 10 if key[0].isdigit() else c1 * 34 + c2 - 100
    return total % 11 == (int(siren) + total // 11 + 1) % 11


# letters in a RIB account number: A-I and J-R are 1-9, S-Z are 2-9
_FR_RIB_LETTERS = dict(zip(string.ascii_uppercase, '12345678912345678923456789'))


def fr_rib(text):
    s = ''.join(_FR_RIB_LETTERS.get(c, c) for c in re.sub(r'\s', '', text))
    return 97 - (89 * int(s[:5]) + 15 * int(s[5:10]) + 3 * int(s[10:21])) % 97 == int(s[21:])


def fr_numero_fiscal(text):
    # numero fiscal (SPI): the last three digits are the first ten mod 511
    d = _digits(text)
    return int(d[:10]) % 511 == int(d[10:])


def fr_mrz_id_card(line):
    # the 2021 card is a TD1; the older card (2 lines of 36) is matched on its second line: card number + check digit
    # at 0-12, date of birth + check digit at 27-33
    if len(line) == 30:
        return mrz_td1(line)
    return _icao_check(line[:12]) == int(line[12]) and _icao_check(line[27:33]) == int(line[33])


def _de_mod11_10(d):
    # ISO 7064 MOD 11,10 over all digits but the last, which is the check digit
    product = 10
    for c in d[:-1]:
        product = 2 * ((int(c) + product) % 10 or 10) % 11
    return (11 - product) % 10 == int(d[-1])


def de_tax_id(text):
    # Steuer-IdNr: in the first ten digits exactly one digit occurs twice or three times, the three never in a row
    d = _digits(text)
    counts = sorted(d[:10].count(c) for c in set(d[:10]))
    return counts[-1] in (2, 3) and counts[-2] == 1 and not re.search(r'(\d)\1\1', d[:10]) and _de_mod11_10(d)


def de_vat_number(text):
    return _de_mod11_10(_digits(text))


def _de_letter_digits(c):
    # A=01 ... Z=26
    return '%02d' % (ord(c) - 64)


def de_pension_insurance_number(text):
    # area, birth date, first letter of the birth name (as two digits), serial, check digit
    s = re.sub(r'\s', '', text)
    d = s[:8] + _de_letter_digits(s[8]) + s[9:11]
    total = sum(sum(divmod(int(c) * w, 10)) for c, w in zip(d, (2, 1, 2, 5, 7, 1, 2, 1, 2, 1, 2, 1)))
    return total % 10 == int(s[11])


def de_health_insurance_number(text):
    d = _de_letter_digits(text[0]) + text[1:9]
    total = sum(sum(divmod(int(c) * (1 + i % 2), 10)) for i, c in enumerate(d))
    return total % 10 == int(text[9])


_LU_VERHOEFF_D = ('0123456789', '1234067895', '2340178956', '3401289567', '4012395678',
                  '5987604321', '6598710432', '7659821043', '8765932104', '9876543210')
_LU_VERHOEFF_P = '1576283094'


def _lu_verhoeff(digits):
    # Verhoeff: the digits from the right, each permuted (position mod 8) times, combined in the dihedral group D5
    c = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        for _ in range(i % 8):
            n = int(_LU_VERHOEFF_P[n])
        c = int(_LU_VERHOEFF_D[c][n])
    return c == 0


def lu_national_number(text):
    # matricule: YYYYMMDD + 3 digits, then a Luhn and a Verhoeff check digit, both over those 11.
    # An unknown birth month or day is 00.
    import calendar
    d = _digits(text)
    year, month, day = int(d[:4]), int(d[4:6]), int(d[6:8])
    if month > 12 or (month and day > calendar.monthrange(year, month)[1]):
        return False
    return luhn(d[:12]) and _lu_verhoeff(d[:11] + d[12])


def lu_vat_number(text):
    # TVA: the first six digits mod 89 are the last two
    d = _digits(text)
    return int(d[:6]) % 89 == int(d[6:])


def gb_nhs_number(text):
    # first nine digits weighted 10 down to 2: 11 minus the sum mod 11 is the tenth (11 counts as 0, 10 is never issued)
    d = _digits(text)
    return (11 - sum(int(c) * w for c, w in zip(d, range(10, 1, -1))) % 11) % 11 == int(d[9])


def gb_utr(text):
    # the FIRST digit checks the other nine, weighted 6, 7, 8, 9, 10, 5, 4, 3, 2: 11 minus the sum mod 11,
    # with 10 and 11 written as 1 and 2
    d = _digits(text)
    check = 11 - sum(int(c) * w for c, w in zip(d[1:], (6, 7, 8, 9, 10, 5, 4, 3, 2))) % 11
    return int(d[0]) == (check - 9 if check > 9 else check)


def gb_vat_number(text):
    d = _digits(text)
    if len(d) == 3:
        # GD000-GD499 (government departments) and HA500-HA999 (health authorities) have no check digits
        return True
    # first seven digits weighted 8 down to 2, plus the two check digits; a branch suffix (12 digits) is not checked
    total = sum(int(c) * w for c, w in zip(d, (8, 7, 6, 5, 4, 3, 2))) + int(d[7:9])
    # the 9755 series (issued from November 2009, restarting at 100 0000 00) adds 55 before the mod 97
    return total % 97 == 0 or (total % 97 == 42 and d[0] != '0')


def es_nif(text):
    # DNI, NIE and the K/L/M numbers end in the letter of the number mod 23; a CIF ends in a control digit
    s = re.sub(r'\W', '', text.upper())
    s = s[2:] if len(s) == 11 else s  # VAT number: ES in front
    if s[0] in 'ABCDEFGHJNPQRSUVW':
        d = [int(c) for c in s[1:8]]
        check = -(sum(d[1::2]) + sum(sum(divmod(2 * x, 10)) for x in d[0::2])) % 10
        # some entity types take the control as a letter: JABCDEFGHI for 0-9
        return s[8] in (str(check), 'JABCDEFGHI'[check])
    # an NIE counts X, Y, Z as 0, 1, 2; K, L, M numbers use their seven digits
    number = s[:8].replace('X', '0').replace('Y', '1').replace('Z', '2').lstrip('KLM')
    return 'TRWAGMYFPDXBNJZSQVHLCKE'[int(number) % 23] == s[8]


def es_nss(text):
    # Spanish social security number: the last two digits are province + number mod 97. A number below
    # 10 000 000 (an old 7-digit number, padded with a zero) is counted without that zero.
    d = _digits(text)
    number = int(d[2:-2])
    return (int(d[:2]) * 10 ** (8 if number >= 10 ** 7 else 7) + number) % 97 == int(d[-2:])


_IT_ODD = (1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23)


def it_codice_fiscale(text):
    # check letter: odd positions through a table, even positions by value (0-9, A=0 ... Z=25), sum mod 26
    s = text.upper()
    values = [int(c) if c.isdigit() else ord(c) - 65 for c in s]
    if sum(_IT_ODD[v] if i % 2 == 0 else v for i, v in enumerate(values[:15])) % 26 != values[15]:
        return False
    # birth date: omocodia replaces digits by LMNPQRSTUV (0-9), women have 40 added to the day
    n = [int(c) if c.isdigit() else 'LMNPQRSTUV'.index(c) for c in s[6:8] + s[9:11]]
    year, day = 10 * n[0] + n[1], 10 * n[2] + n[3]
    day = day - 40 if day > 40 else day
    days = (31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return 1 <= day <= days['ABCDEHLMPRST'.index(s[8])]


def it_partita_iva(text):
    # 7-digit number (not all zeros), office code 001-100, 120, 121, 888 or 999, then a Luhn check digit
    d = _digits(text)
    return int(d[:7]) > 0 and (1 <= int(d[7:10]) <= 100 or d[7:10] in ('120', '121', '888', '999')) and luhn(d)


def _pl_ro_date(year, month, day):
    # the birth date inside a PESEL or CNP is a real calendar date
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    return 1 <= month <= 12 and 1 <= day <= (31, 28 + leap, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month - 1]


def pl_pesel(text):
    # weights 1,3,7,9 repeated, and 1 for the check digit, give a multiple of 10; the month carries the century
    d = _digits(text)
    month = int(d[2:4])
    year = (1900, 2000, 2100, 2200, 1800)[month // 20] + int(d[:2])
    return sum(int(c) * w for c, w in zip(d, (1, 3, 7, 9, 1, 3, 7, 9, 1, 3, 1))) % 10 == 0 and _pl_ro_date(
        year, month % 20, int(d[4:6]))


def pl_nip(text):
    # first nine digits weighted 6,5,7,2,3,4,5,6,7: the sum mod 11 is the tenth digit (a sum giving 10 is never issued)
    d = _digits(text)
    return sum(int(c) * w for c, w in zip(d, (6, 5, 7, 2, 3, 4, 5, 6, 7))) % 11 == int(d[9])


def _pl_regon_check(d, weights):
    return sum(int(c) * w for c, w in zip(d, weights)) % 11 % 10 == int(d[-1])


def pl_regon(text):
    # 9 digits, or 14 whose first nine are the parent unit's REGON
    d = _digits(text)
    return _pl_regon_check(d[:9], (8, 9, 2, 3, 4, 5, 6, 7)) and (
        len(d) == 9 or _pl_regon_check(d, (2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8)))


def pl_document_number(text):
    # ID card ABA300000 and passport ZZ3000001: the first digit is the ICAO check digit of the other characters
    s = text.replace(' ', '')
    k = len(s) - len(s.lstrip(string.ascii_uppercase))
    return _icao_check(s[:k] + s[k + 1:]) == int(s[k])


def pl_nrb(text):
    # the domestic account number is a Polish IBAN without its PL
    return iban('PL' + _digits(text))


def ro_cnp(text):
    # first twelve digits weighted 2,7,9,1,4,6,3,5,8,2,7,9: the sum mod 11 is the last digit (10 gives 1)
    d = _digits(text)
    centuries = {'1': (1900,), '2': (1900,), '3': (1800,), '4': (1800,), '5': (2000,), '6': (2000,)}
    # residents (7, 8) and foreigners (9) carry no century
    born = any(_pl_ro_date(c + int(d[1:3]), int(d[3:5]), int(d[5:7])) for c in centuries.get(d[0], (1900, 2000)))
    county = int(d[7:9])
    check = sum(int(c) * w for c, w in zip(d, (2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9))) % 11
    return born and (1 <= county <= 48 or county in (51, 52, 70)) and (check if check < 10 else 1) == int(d[12])


def ro_cui(text):
    # the digits before the check digit, right-aligned under 7,5,3,2,1,7,5,3,2: their sum * 10 mod 11 mod 10
    d = _digits(text)
    return 2 <= len(d) <= 10 and sum(
        int(c) * w for c, w in zip(d[:-1].zfill(9), (7, 5, 3, 2, 1, 7, 5, 3, 2))) * 10 % 11 % 10 == int(d[-1])


def ro_onrc(text):
    s = re.sub(r'\s', '', text)
    if '/' in s:
        # J40/1234/2020: county 1-40, 51 or 52, and a year up to 2024, the last of this format
        county, _, year = (int(p) for p in s[1:].split('/'))
        return (1 <= county <= 40 or county in (51, 52)) and 1990 <= year <= 2024
    # J2025000001004: year, serial, county (00 for registrations since 26 July 2024), then a check digit: the
    # letter's ASCII code plus the twelve digits, mod 10
    year, county = int(s[1:5]), int(s[11:13])
    if year > 2024:
        county_ok = county == 0
    else:
        county_ok = 1 <= county <= 40 or county in (51, 52) or (year == 2024 and county == 0)
    return year >= 1990 and county_ok and (ord(s[0]) + sum(int(c) for c in s[1:13])) % 10 == int(s[13])


def ro_mrz_id_card(line):
    # the electronic card's TD1 line 1, or line 2 of the older card's 36-character zone (TD2), whose document number,
    # birth date and expiry date check digits sit where a passport line has them
    return mrz_td1(line) if len(line) == 30 else mrz_td3(line)


_BIP39 = {}


def _bip39_index():
    # the BIP39 English word list (intl/bip39_english.txt), read on first use: word -> index
    if not _BIP39:
        from pathlib import Path
        words = (Path(__file__).parent / 'intl' / 'bip39_english.txt').read_text(encoding='ascii').split()
        _BIP39.update(zip(words, range(len(words))))
    return _BIP39


def _bip39_checksum(n, count):
    # count words of 11 bits in n: the entropy, then the first count/3 bits of its sha256
    bits = count // 3
    entropy = (n >> bits).to_bytes(count * 4 // 3, 'big')
    return hashlib.sha256(entropy).digest()[0] >> (8 - bits) == n & ((1 << bits) - 1)


def bip39(text):
    # a seed phrase in a run of words: the longest valid 24/21/18/15/12 list words in a row, earliest first
    index = _bip39_index()
    words = [(m.start(), m.end(), index.get(m.group().lower())) for m in re.finditer('[A-Za-z]+', text)]
    in_list = [0] * (len(words) + 1)  # list words in a row from word i on
    for i in range(len(words) - 1, -1, -1):
        in_list[i] = 0 if words[i][2] is None else in_list[i + 1] + 1
    for i in range(len(words)):
        size = min(in_list[i], 24)
        n, found = 0, 0
        for _, _, k in words[i:i + size]:
            n = n << 11 | k
        for count in range(12, size + 1, 3):
            if _bip39_checksum(n >> 11 * (size - count), count):
                found = count
        if found:
            return text[words[i][0]:words[i + found - 1][1]]
    return ''


_RIPPLE_TO_BASE58 = str.maketrans('rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz', _BASE58)


def ripple_base58check(text):
    # XRP Ledger addresses: base58check with Ripple's own alphabet, where 'r' is the zero digit
    return base58check(text.translate(_RIPPLE_TO_BASE58))


def card_pan(text):
    # card track data and card dumps start with the card number
    return luhn(re.search(r'\d+', text).group())


def lei(text):
    # ISO 17442 / ISO 7064 mod 97-10: letters as numbers (A=10 ... Z=35), the whole mod 97 is 1
    return int(''.join(str(int(c, 36)) for c in text)) % 97 == 1


def isin(text):
    # the ISIN ends the match: letters as numbers (A=10 ... Z=35), then luhn
    return luhn(''.join(str(int(c, 36)) for c in text[-12:]))


def _gs1_mod10(digits):
    # weights 1, 3, 1, 3 ... from the right, check digit included: the sum ends in 0
    return sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(reversed(digits))) % 10 == 0


def gtin(text):
    # the number follows the keyword and its ':' or space ('EAN-13: ...'): 8, 12, 13 or 14 digits
    d = _digits(re.split(r'[:\s]', text, maxsplit=1)[1])
    return len(d) in (8, 12, 13, 14) and _gs1_mod10(d)


def isbn(text):
    # the keyword's 10 or 13 (ISBN-13:) adds 0 or 2 digits in front of the 10 or 13 of the number
    s = re.sub('[^0-9X]', '', text.upper())
    if len(s) in (13, 15):
        return _gs1_mod10(s[-13:])
    # ISBN-10: weights 10 down to 1, X is 10, the sum mod 11 is 0
    s = s[-10:]
    return len(s) == 10 and sum((10 - i) * (10 if c == 'X' else int(c)) for i, c in enumerate(s)) % 11 == 0


def upu_s10(text):
    # serial weighted 8 6 4 2 3 5 9 7, check = 11 - sum mod 11, where 10 becomes 0 and 11 becomes 5
    d = _digits(text)
    check = 11 - sum(int(c) * w for c, w in zip(d, (8, 6, 4, 2, 3, 5, 9, 7))) % 11
    return {10: 0, 11: 5}.get(check, check) == int(d[8])


def ups_1z(text):
    # the 15 characters after 1Z, letters as (ord - 63) mod 10: odd positions + twice the even ones
    s = re.sub(r'\s', '', text)[2:]
    v = [int(c) if c.isdigit() else (ord(c) - 63) % 10 for c in s[:15]]
    return (10 - (sum(v[0::2]) + 2 * sum(v[1::2])) % 10) % 10 == int(s[15])


def air_waybill(text):
    # 3-digit airline prefix, 7-digit serial, check digit = serial mod 7
    d = _digits(text)
    return int(d[3:10]) % 7 == int(d[10])


def jwt(text):
    # JSON Web Token: the header (up to the first dot) is base64url JSON with an "alg" field
    header = text.split('.')[0]
    try:
        decoded = json.loads(base64.urlsafe_b64decode(header + '=' * (-len(header) % 4)))
    except (ValueError, RecursionError):
        return False
    return isinstance(decoded, dict) and 'alg' in decoded


_PHONE_TYPES = {
    'mobile': {phonenumbers.PhoneNumberType.MOBILE, phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE},
    'premium': {phonenumbers.PhoneNumberType.PREMIUM_RATE, phonenumbers.PhoneNumberType.SHARED_COST},
}
_PHONE_TYPES['msisdn'] = _PHONE_TYPES['mobile']


def phone(text, regions='', kind=''):
    # libphonenumber (the phonenumbers package): a valid number of one of the regions, any region when none are
    # given; a national number is read as one of each region in turn. An msisdn is a mobile number without its +
    if kind == 'msisdn':
        text = '+' + text
    for region in regions.split() or [None]:
        try:
            number = phonenumbers.parse(text, region)
        except phonenumbers.NumberParseException:
            continue
        if phonenumbers.is_valid_number(number) and (
                not regions or phonenumbers.region_code_for_number(number) in regions.split()):
            return kind not in _PHONE_TYPES or phonenumbers.number_type(number) in _PHONE_TYPES[kind]
    return False


def mac_address(text):
    # 02:00:00:00:00:00 is what Android (6 on) and iOS (7 on) give apps instead of the device's address; all zeros
    # and all ff (broadcast) are no device's address either
    return re.sub('[^0-9a-f]', '', text.lower()) not in ('020000000000', '000000000000', 'ffffffffffff')


def _luhn16(text):
    # Luhn in base 16: every second hex digit from the right doubled, the digits of the products added
    digits = [int(c, 16) for c in reversed(text)]
    return (sum(digits[0::2]) + sum(sum(divmod(2 * d, 16)) for d in digits[1::2])) % 16 == 0


def meid(text):
    # the MEID after its label (3GPP2 X.S0008): 14 hex digits, from A0 on or all decimal (an IMEI's first 14), or the
    # 18-digit decimal form, each with an optional check digit
    v = re.sub(r'\s', '', re.sub(r'(?i)^meid[\W_]*(?:(?:hex|dec)\b[\W_]*)?', '', text))
    if not re.fullmatch('[0-9A-Fa-f]{14,15}|[0-9]{18,19}', v):
        return False
    if len(v) >= 18:
        # decimal form: the manufacturer code (32 bits) in 10 digits and the serial number (24 bits) in 8, then Luhn
        return int(v[:10]) <= 0xFFFFFFFF and int(v[10:18]) <= 0xFFFFFF and (len(v) == 18 or luhn(v))
    if v[:14].isdigit():
        return len(v) == 14 or (v.isdigit() and luhn(v))
    # with letters: Luhn in base 16
    return v[0] in 'ABCDEFabcdef' and (len(v) == 14 or _luhn16(v))


# Mobile country codes: ITU-T E.212's list (position on 1 February 2017) and its amendments since (902, 991 and 999
# for internal use), 001 for test networks, and two in use that the ITU does not list, 289 (Abkhazia) and 995
# (British Indian Ocean Territory)
_MCC = set('''
001 202 204 206 208 212 213 214 216 218 219 220 221 222 225 226 228 230 231 232 234 235 238 240 242 244 246 247 248
250 255 257 259 260 262 266 268 270 272 274 276 278 280 282 283 284 286 288 289 290 292 293 294 295 297 302 308 310
311 312 313 314 315 316 330 332 334 338 340 342 344 346 348 350 352 354 356 358 360 362 363 364 365 366 368 370 372
374 376 400 401 402 404 405 406 410 412 413 414 415 416 417 418 419 420 421 422 424 425 426 427 428 429 430 431 432
434 436 437 438 440 441 450 452 454 455 456 457 460 461 466 467 470 472 502 505 510 514 515 520 525 528 530 536 537
539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 602 603 604 605 606 607 608 609 610 611 612 613
614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642
643 645 646 647 648 649 650 651 652 653 654 655 657 658 659 702 704 706 708 710 712 714 716 722 724 730 732 734 736
738 740 742 744 746 748 750 901 902 991 995 999
'''.split())


def mcc_mnc(text):
    # the country code comes first, except in a 3GPP domain name (mnc001.mcc206); network codes change too often to list
    d = _digits(text)
    return (d[-3:] if text[:3].lower() == 'mnc' else d[:3]) in _MCC


_FILE_EXTENSIONS = set('apk bin csv dat db doc docx gif heic html ipa jpeg jpg js json log mov mp3 mp4 pdf plist png '
                       'sqlite sqlitedb txt xls xlsx xml zip'.split())


def app_package_name(text):
    # a file named after the app (com.apple.mobilesafari.plist) loses its extension, a name ending in a generic
    # top-level domain is a web address (de.wikipedia.org). Only com and org names can have two parts (not com.au);
    # others need three, do not end in a two-letter country code (ec.europa.eu, app.example.io) and have a part of
    # five letters or more (ch.threema.app, not words joined by dots: il.fait.beau)
    labels = text.split('.')
    if len(labels) > 1 and labels[-1].lower() in _FILE_EXTENSIONS:
        labels.pop()
        # an app's shared preferences: com.whatsapp_preferences.xml
        if labels[-1].endswith('_preferences'):
            labels[-1] = labels[-1][:-12]
    if labels[-1].lower() in ('com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'info', 'biz'):
        return ''
    if labels[0] in ('com', 'org'):
        ok = len(labels) > 2 or (len(labels) == 2 and len(labels[1]) > 2)
    else:
        ok = len(labels) > 2 and len(labels[-1]) > 2 and max(map(len, labels)) > 4
    return '.'.join(labels) if ok else ''


def unix_timestamp(text):
    # the last number in the match: Unix time in seconds (9-10 digits) or milliseconds (12-13) from 2000 to 2040 UTC
    numbers = re.findall(r'\d+', text)
    n = int(numbers[-1]) if numbers and len(numbers[-1]) <= 13 else 0
    return 946684800 <= n < 2240611200 or 946684800000 <= n < 2240611200000


def exif_gps_rational(text):
    # EXIF GPS degrees, minutes and seconds as three rationals (51/1, 15/1, 4536/100)
    try:
        degrees, minutes, seconds = (int(n) / int(d) for n, d in re.findall(r'(\d+)/(\d+)', text))
    except (ValueError, ZeroDivisionError, OverflowError):
        return False
    return minutes < 60 and seconds < 60 and degrees + minutes / 60 + seconds / 3600 <= 180


def _base58_bytes(text):
    # base58 (Bitcoin's alphabet) to bytes, with a zero byte for each leading '1'
    n = 0
    for c in text:
        n = n * 58 + _BASE58.index(c)
    return b'\0' * (len(text) - len(text.lstrip('1'))) + n.to_bytes((n.bit_length() + 7) // 8, 'big')


def solana_address(text):
    # an ed25519 public key: the base58 word that ends the match (after its keyword) decodes to 32 bytes
    return len(_base58_bytes(re.search('[1-9A-HJ-NP-Za-km-z]+$', text).group())) == 32


def dogecoin_address(text):
    # base58check with Dogecoin's version byte: 30 (D..., P2PKH) or 22 (9... or A..., P2SH)
    return base58check(text) and _base58_bytes(text)[0] in (30, 22)


def cashaddr(text):
    # Bitcoin Cash CashAddr: one case only, and a 40-bit BCH checksum over the prefix (bitcoincash when it is left
    # out), a zero and the payload
    prefix, _, payload = text.rpartition(':')
    if not (text.islower() or text.isupper()):
        return False
    values = [ord(c) & 31 for c in prefix or 'bitcoincash'] + [0]
    values += ['qpzry9x8gf2tvdw0s3jn54khce6mua7l'.index(c) for c in payload.lower()]
    chk = 1
    for v in values:
        top = chk >> 35
        chk = (chk & 0x07ffffffff) << 5 ^ v
        for i, g in enumerate((0x98f2bc8e61, 0x79b76d99e2, 0xf33e5fb3c4, 0xae2eabe2a8, 0x1e4f43e470)):
            chk ^= g if (top >> i) & 1 else 0
    return chk == 1


def dhl(text):
    # JJD and JVGL numbers have no check digit. After the keyword: an Express waybill (10 digits, the first nine mod 7
    # are the last), a DHL Paket Identcode (12 digits weighted 4, 9, ...) or a 20-digit SSCC (GS1 mod 10)
    if text.startswith(('JJD', 'JVGL')):
        return True
    d = _digits(text)
    if len(d) == 10:
        return int(d[:9]) % 7 == int(d[9])
    if len(d) == 12:
        return -sum(int(c) * w for c, w in zip(d[:11], (4, 9) * 6)) % 10 == int(d[11])
    return _gs1_mod10(d)


def dpd(text):
    # the 14-digit DPD parcel number after the keyword, and the ISO 7064 MOD 37,36 check character printed after it
    s = re.sub(r'\s', '', text[re.search(r'\d', text).start():])
    p = 36
    for c in s[:14]:
        p = 2 * ((p + int(c)) % 36 or 36) % 37
    return len(s) == 14 or int(s[14], 36) == (37 - p) % 36


def gls(text):
    # 11 digits, or 12 whose last is the check digit: GS1 mod 10 (3 on the rightmost digit) with 1 added to the sum
    d = _digits(text)
    total = 1 + sum(int(c) * (3 if i % 2 == 0 else 1) for i, c in enumerate(reversed(d[:11])))
    return len(d) == 11 or -total % 10 == int(d[11])


def cardano_address(text):
    # Shelley addresses (addr1..., stake1...) are bech32 without its length limit. A Byron address is the base58 of
    # CBOR [tag 24 (the address as bytes), CRC32 of those bytes]
    if text.startswith(('addr1', 'stake1')):
        return bech32(text)
    raw = _base58_bytes(text)
    if raw[:4] == b'\x82\xd8\x18\x58':
        size, start = raw[4], 5
    elif raw[:4] == b'\x82\xd8\x18\x59':
        size, start = int.from_bytes(raw[4:6], 'big'), 6
    else:
        return False
    import zlib
    crc = zlib.crc32(raw[start:start + size])
    # the CRC as a CBOR unsigned integer, in its shortest form: one byte below 24, else 0x18, 0x19 or 0x1a and 1, 2 or
    # 4 bytes
    n = 0 if crc < 24 else 1 if crc < 256 else 2 if crc < 65536 else 4
    return raw[start + size:] == (bytes([crc]) if not n else bytes([{1: 24, 2: 25, 4: 26}[n]]) + crc.to_bytes(n, 'big'))


def ss58(text):
    # Polkadot (prefix 0), Kusama (2) and generic Substrate (42) addresses: the prefix byte, the 32-byte account and
    # the first two bytes of the BLAKE2b-512 of 'SS58PRE', prefix and account
    raw = _base58_bytes(text)
    return len(raw) == 35 and raw[0] in (0, 2, 42) and hashlib.blake2b(b'SS58PRE' + raw[:33]).digest()[:2] == raw[33:]


def stellar_strkey(text):
    # Stellar account (G...) and muxed account (M...) addresses: base32 of the version byte, the key (and the muxed
    # id), and their CRC16-XModem, little-endian. Written without padding, unused trailing bits zero.
    import binascii
    raw = base64.b32decode(text + '=' * (-len(text) % 8))
    return (base64.b32encode(raw).decode().rstrip('=') == text
            and binascii.crc_hqx(raw[:-2], 0) == int.from_bytes(raw[-2:], 'little'))


def zcash_address(text):
    # transparent addresses (t1..., t3...) are base58check; Sapling (zs1...) and unified (u1...) addresses are bech32
    # and bech32m, without the length limit
    return base58check(text) if text.startswith('t') else bech32(text)


def dash_address(text):
    # base58check with Dash's version byte: 76 (X..., P2PKH) or 16 (7..., P2SH)
    return base58check(text) and _base58_bytes(text)[0] in (76, 16)


def ton_address(text):
    # TON user-friendly address, base64 or base64url: flag, workchain, 32-byte account, then the CRC16-XModem of
    # those 34 bytes, big-endian
    import binascii
    raw = base64.urlsafe_b64decode(text.replace('+', '-').replace('/', '_'))
    return binascii.crc_hqx(raw[:34], 0) == int.from_bytes(raw[34:], 'big')


def tox_id(text):
    # Tox ID: public key (32 bytes), nospam (4) and checksum (2), the XOR of the first 36 bytes taken two at a time.
    # A random key has about 16 different hex digits; a few repeated ones is filler (zeros) that also XORs to 0000
    try:
        data = bytes.fromhex(text)
    except ValueError:
        return False
    checksum = [0, 0]
    for i, byte in enumerate(data[:36]):
        checksum[i % 2] ^= byte
    return bytes(checksum) == data[36:] and len(set(text[:64].upper())) > 8


def bitlocker_recovery_key(text):
    # BitLocker recovery password: 8 blocks of 6 digits, each a 16-bit number times 11; eight equal blocks
    # (000000-000000-...) are a placeholder
    blocks = [int(b) for b in re.findall(r'\d{6}', text)]
    return len(blocks) == 8 and len(set(blocks)) > 1 and all(b % 11 == 0 and b < 65536 * 11 for b in blocks)


def _2000_to_2040(unix_seconds):
    # the range unix_timestamp accepts
    return 946684800 <= unix_seconds < 2240611200


def mac_absolute_time(text):
    # the last number in the match: seconds since 1 January 2001 UTC, or nanoseconds (18-19 digits, newer Messages)
    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    n = float(numbers[-1]) if numbers else 0
    return _2000_to_2040((n / 1e9 if n >= 1e17 else n) + 978307200)


def webkit_timestamp(text):
    # the last number in the match: microseconds since 1 January 1601 UTC
    numbers = re.findall(r'\d+', text)
    return bool(numbers) and _2000_to_2040(int(numbers[-1]) / 1e6 - 11644473600)


def windows_filetime(text):
    # the last number in the match, decimal or 0x hexadecimal: 100-nanosecond intervals since 1 January 1601 UTC
    numbers = re.findall(r'0x[0-9A-Fa-f]+|\d+', text)
    if not numbers:
        return False
    n = int(numbers[-1], 16) if numbers[-1].startswith('0x') else int(numbers[-1])
    return _2000_to_2040(n / 1e7 - 11644473600)


def cidr(text):
    # an IPv4 or IPv6 address with a prefix length; host bits may be set (192.168.1.10/24, an interface's address)
    try:
        ipaddress.ip_network(text, strict=False)
        return True
    except ValueError:
        return False


def asn(text):
    # the only number in the match: 32 bits, without 0 and 4294967295 (reserved)
    return 0 < int(_digits(text) or 0) < 4294967295


def eid(text):
    # eSIM EID (GSMA SGP.29): the 32 digits mod 97 are 1, as in an IBAN
    d = _digits(text)
    return len(d) == 32 and int(d) % 97 == 1


def bcbp(text):
    # IATA boarding pass barcode (BCBP, Resolution 792): 23 characters, then per leg 37 that end in the hex size of the
    # leg's variable part, then maybe ^, a type, a hex size and the security data. Returns the barcode, cut where it ends
    pos = 23
    for _ in range(int(text[1])):
        leg = text[pos:pos + 37]
        if not (re.fullmatch('[A-Z0-9 ]{7}[A-Z]{6}[A-Z0-9 ]{3}[0-9 ]{4}[A-Z ][0-9]{3}[A-Z][A-Z0-9 ]{10}[0-9A-F]{2}', leg)
                and 1 <= int(leg[21:24]) <= 366):
            return ''
        pos += 37 + int(leg[35:], 16)
    security = re.match(r'\^.([0-9A-F]{2})', text[pos:])
    if security:
        pos += 4 + int(security.group(1), 16)
    return text[:pos]


def fedex(text):
    # after the keyword: Express (12 digits: the first eleven weighted 3, 1, 7, 3, ..., the sum mod 11 mod 10 is the
    # last) or Ground (15 digits, or 22 starting with 96 that end in those 15: GS1 mod 10). Returned as a string, so a
    # failing 15-digit number is not tried again as its first 12 digits
    d = _digits(text)
    if len(d) == 12:
        ok = sum(int(c) * w for c, w in zip(d[:11], (3, 1, 7) * 4)) % 11 % 10 == int(d[11])
    else:
        ok = _gs1_mod10(d[-15:])
    return text if ok else ''


def usps(text):
    # GS1 mod 10; a 20-digit number is printed without its application identifier 91, which counts in the sum. Returned
    # as a string, so a failing 22-digit number is not tried again as its first 20 digits
    d = _digits(text)
    return text if _gs1_mod10('91' + d if len(d) == 20 else d) else ''


def iso11649(text):
    # RF creditor reference: RF and the check digits moved to the end, then ISO 7064 mod 97-10 as for the LEI
    s = re.sub(r'\s', '', text)
    return lei(s[4:] + s[:4])


def sepa_creditor_id(text):
    # SEPA creditor identifier: as iso11649, with the creditor business code (characters 5 to 7) left out
    s = re.sub(r'\s', '', text)
    return lei(s[7:] + s[:4])
