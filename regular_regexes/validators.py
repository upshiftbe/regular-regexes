import hashlib
import ipaddress
import re
import string


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
