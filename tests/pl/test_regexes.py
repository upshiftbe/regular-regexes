from regular_regexes import rre

# Numbers below are published specimens or computed with the check digit algorithm. Poland reserves no phone
# numbers for fiction: the phone tests use placeholder digits.


def test_pesel():
    # born 14 May 2101: the month is raised by 40
    assert rre.pl.pesel("PESEL 01451401354") == ["01451401354"]
    assert rre.pl.pesel("PESEL 01451401355") == []
    assert rre.pl.pesel("01130101353") == []  # checksum fine, month 13


def test_nip():
    assert rre.pl.nip("NIP: 123-456-32-18, NIP 1234563218") == ["NIP: 123-456-32-18", "NIP 1234563218"]
    assert rre.pl.nip("firma 123-456-32-18, osoba 123-45-63-218") == ["123-456-32-18", "123-45-63-218"]
    assert rre.pl.nip("NIP 123-456-32-19") == []
    assert rre.pl.nip("nr 1234563218") == []  # ten bare digits need the keyword


def test_vat_number():
    assert rre.pl.vat_number("VAT PL1234563218 / PL 123-456-32-18") == ["PL1234563218", "PL 123-456-32-18"]
    assert rre.pl.vat_number("PL1234563219") == []


def test_regon():
    assert rre.pl.regon("REGON: 123456785, REGON 12345678512347") == ["REGON: 123456785", "REGON 12345678512347"]
    assert rre.pl.regon("REGON 123456786") == []
    assert rre.pl.regon("REGON 12345678612342") == []  # last digit fine, but the first nine are no REGON
    assert rre.pl.regon("123456785") == []


def test_krs_number():
    assert rre.pl.krs_number("KRS 0000123456, nr KRS: 0000654321") == ["KRS 0000123456", "KRS: 0000654321"]
    assert rre.pl.krs_number("nr 0000123456") == []


def test_id_card_number():
    # specimen numbers of the 2001 and 2019 cards
    assert rre.pl.id_card_number("dowód ABA300000 i ZZC 108201") == ["ABA300000", "ZZC 108201"]
    assert rre.pl.id_card_number("ABA300001") == []


def test_passport_number():
    assert rre.pl.passport_number("paszport ZZ3000001") == ["ZZ3000001"]
    assert rre.pl.passport_number("ZZ4000001") == []


def test_mrz_id_card():
    line = "IDPOLZZC1082012" + "<" * 15
    assert rre.pl.mrz_id_card(f"mrz {line}") == [line]
    assert rre.pl.mrz_id_card("IDPOLZZC1082013" + "<" * 15) == []


def test_mrz_passport():
    # ICAO 9303 specimen with POL nationality
    line = "L898902C36POL7408122F1204159ZE184226B<<<<<10"
    assert rre.pl.mrz_passport(line) == [line]
    assert rre.pl.mrz_passport(line.replace("C36", "C37")) == []


def test_iban():
    # IBAN registry example
    assert rre.pl.iban("konto PL61 1090 1014 0000 0712 1981 2874") == ["PL61 1090 1014 0000 0712 1981 2874"]
    assert rre.pl.iban("PL61109010140000071219812875") == []


def test_nrb():
    assert rre.pl.nrb("nr rachunku 61 1090 1014 0000 0712 1981 2874") == ["61 1090 1014 0000 0712 1981 2874"]
    assert rre.pl.nrb("61 1090 1014 0000 0712 1981 2875") == []


def test_bic():
    assert rre.pl.bic("BIC PKOPPLPW lub BREXPLPWXXX") == ["PKOPPLPW", "BREXPLPWXXX"]
    assert rre.pl.bic("GEBABEBB") == []


def test_phone_number():
    assert rre.pl.phone_number("tel. +48 22 123 45 67, (22) 123 45 67 lub 600 123 456") == [
        "+48 22 123 45 67", "(22) 123 45 67", "600 123 456"]
    assert rre.pl.phone_number("nr 221234567 i 1234 5678") == []


def test_mobile_number():
    assert rre.pl.mobile_number("kom. 600-123-456 lub +48 512 345 678") == ["600-123-456", "+48 512 345 678"]
    assert rre.pl.mobile_number("22 123 45 67 i 600 123 456 789") == []


def test_msisdn():
    assert rre.pl.msisdn("msisdn 48600123456") == ["48600123456"]
    assert rre.pl.msisdn("48221234567") == []


def test_imsi():
    assert rre.pl.imsi("imsi 260021234567890") == ["260021234567890"]
    assert rre.pl.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.pl.iccid("sim 8948021234567890126") == ["8948021234567890126"]
    assert rre.pl.iccid("sim 8948021234567890127") == []


def test_license_plate():
    assert rre.pl.license_plate("auto WA 12345, KR 1234A i KRA 1C34") == ["WA 12345", "KR 1234A", "KRA 1C34"]
    assert rre.pl.license_plate("norma ISO 14001, WA 1234, KR 1234B") == []


def test_postal_code_city():
    assert rre.pl.postal_code_city("00-950 Warszawa i 43-300 Bielsko-Biała") == [
        "00-950 Warszawa", "43-300 Bielsko-Biała"]
    assert rre.pl.postal_code_city("od 10-100 osób") == []


def test_street_address():
    assert rre.pl.street_address("mieszka ul. Jana Pawła II 12/34, Kraków") == ["ul. Jana Pawła II 12/34"]
    assert rre.pl.street_address("os. Kościuszkowskie 5 m. 12") == ["os. Kościuszkowskie 5 m. 12"]
    assert rre.pl.street_address("www.onet.pl. Zobacz 5 razy") == []


def test_company_name():
    assert rre.pl.company_name("umowa z Kowalski Budownictwo Sp. z o.o. i Nowak sp.j.") == [
        "Kowalski Budownictwo Sp. z o.o.", "Nowak sp.j."]
    assert rre.pl.company_name("Budex S.A. oraz Alfa Sp. z o.o. sp.k.") == ["Budex S.A.", "Alfa Sp. z o.o. sp.k."]
    assert rre.pl.company_name("ta sp. z o.o. ma") == []


def test_aircraft_registration():
    assert rre.pl.aircraft_registration("SP-ABC, szybowiec SP-3456") == ["SP-ABC", "SP-3456"]
    assert rre.pl.aircraft_registration("SP-AB i SP-4567") == []
