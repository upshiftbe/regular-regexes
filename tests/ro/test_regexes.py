from regular_regexes import rre

# Numbers below are published specimens or computed with the check digit algorithm. Romania reserves no phone
# numbers for fiction: the phone tests use placeholder digits.


def test_cnp():
    # born 1 January 2090 in Cluj (12)
    assert rre.ro.cnp("CNP 5900101123454") == ["5900101123454"]
    assert rre.ro.cnp("5900101123455") == []
    assert rre.ro.cnp("5900101993451") == []  # checksum fine, county 99


def test_cui():
    assert rre.ro.cui("CUI 12345674, C.I.F.: RO 12345674") == ["CUI 12345674", "C.I.F.: RO 12345674"]
    assert rre.ro.cui("CUI 12345675") == []
    assert rre.ro.cui("nr 12345674") == []


def test_vat_number():
    assert rre.ro.vat_number("TVA RO12345674") == ["RO12345674"]
    assert rre.ro.vat_number("RO12345675") == []


def test_trade_register_number():
    assert rre.ro.trade_register_number("J40/1234/2020 si J2025000001004") == ["J40/1234/2020", "J2025000001004"]
    assert rre.ro.trade_register_number("J2025000001005") == []
    assert rre.ro.trade_register_number("J41/1234/2020 J40/1234/2025") == []  # county 41, old format after 2024


def test_id_card_number():
    assert rre.ro.id_card_number("CI seria RX nr. 123456, C.I. KX 654321, XB123456") == [
        "RX nr. 123456", "KX 654321", "XB123456"]
    assert rre.ro.id_card_number("seria QQ 123456") == []  # no such series


def test_passport_number():
    assert rre.ro.passport_number("pașaport nr. 051234567") == ["pașaport nr. 051234567"]
    assert rre.ro.passport_number("nr. 051234567") == []


def test_mrz_id_card():
    td2 = "RX123456<9ROU9001011M300101914000108"  # line 2 of the older card
    td1 = "IDROUMB12345675" + "<" * 15  # line 1 of the electronic card
    assert rre.ro.mrz_id_card(f"{td2}\n{td1}") == [td2, td1]
    assert rre.ro.mrz_id_card(td2.replace("<9", "<8")) == []


def test_mrz_passport():
    # ICAO 9303 specimen with ROU nationality
    line = "L898902C36ROU7408122F1204159ZE184226B<<<<<10"
    assert rre.ro.mrz_passport(line) == [line]
    assert rre.ro.mrz_passport(line.replace("C36", "C37")) == []


def test_iban():
    # IBAN registry example
    assert rre.ro.iban("cont RO49 AAAA 1B31 0075 9384 0000") == ["RO49 AAAA 1B31 0075 9384 0000"]
    assert rre.ro.iban("RO49AAAA1B31007593840001") == []


def test_bic():
    assert rre.ro.bic("BIC RNCBROBU sau BTRLRO22") == ["RNCBROBU", "BTRLRO22"]
    assert rre.ro.bic("PKOPPLPW") == []


def test_phone_number():
    assert rre.ro.phone_number("tel 021 123 4567, (0264) 123 456, +40 722 123 456") == [
        "021 123 4567", "(0264) 123 456", "+40 722 123 456"]
    assert rre.ro.phone_number("data 02.03.2024 15:30, 0123456789") == []


def test_mobile_number():
    assert rre.ro.mobile_number("mobil 0722.123.456 sau +40722123456") == ["0722.123.456", "+40722123456"]
    assert rre.ro.mobile_number("021 123 4567") == []


def test_premium_number():
    assert rre.ro.premium_number("suna la 0900 123 456") == ["0900 123 456"]
    assert rre.ro.premium_number("0800 123 456") == []


def test_msisdn():
    assert rre.ro.msisdn("msisdn 40722123456") == ["40722123456"]
    assert rre.ro.msisdn("40212345678") == []


def test_imsi():
    assert rre.ro.imsi("imsi 226011234567890") == ["226011234567890"]
    assert rre.ro.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.ro.iccid("sim 8940011234567890125") == ["8940011234567890125"]
    assert rre.ro.iccid("sim 8940011234567890126") == []


def test_license_plate():
    assert rre.ro.license_plate("masina B 123 ABC, CJ-12-XYZ") == ["B 123 ABC", "CJ-12-XYZ"]
    assert rre.ro.license_plate("CJ 123 ABC, B 12 IAB, XX 12 ABC") == []


def test_postal_code_city():
    assert rre.ro.postal_code_city("400001 Cluj-Napoca, 010011 București") == [
        "400001 Cluj-Napoca", "010011 București"]
    assert rre.ro.postal_code_city("comanda 400001 livrata") == []


def test_street_address():
    assert rre.ro.street_address("Str. Mihai Eminescu nr. 5, bl. A2, sc. 1, ap. 12, Cluj") == [
        "Str. Mihai Eminescu nr. 5, bl. A2, sc. 1, ap. 12"]
    assert rre.ro.street_address("Calea Victoriei 155 si Șos. Kiseleff nr. 1") == [
        "Calea Victoriei 155", "Șos. Kiseleff nr. 1"]
    assert rre.ro.street_address("strada noastra") == []


def test_company_name():
    assert rre.ro.company_name("intre S.C. Alfa Beta S.R.L. si Popescu Ion PFA") == [
        "S.C. Alfa Beta S.R.L.", "Popescu Ion PFA"]
    assert rre.ro.company_name("PFA Popescu Ion") == ["PFA Popescu Ion"]
    assert rre.ro.company_name("un srl mic") == []


def test_ecli():
    # e-Justice portal example
    assert rre.ro.ecli("vezi ECLI:RO:JDS4B:2017:001.004053.") == ["ECLI:RO:JDS4B:2017:001.004053"]


def test_aircraft_registration():
    assert rre.ro.aircraft_registration("YR-ABC, YR-1234, drona YR-D0012") == ["YR-ABC", "YR-1234", "YR-D0012"]
    assert rre.ro.aircraft_registration("YR-AB YR-0123") == []
