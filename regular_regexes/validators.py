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
