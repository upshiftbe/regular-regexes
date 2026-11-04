from regular_regexes import rre


def test_codice_fiscale():
    assert rre.it.codice_fiscale("CF RSSMRA85T10A562S e RCCMNL83S18D969H") == ["RSSMRA85T10A562S", "RCCMNL83S18D969H"]
    # omocodia: the last digit replaced by a letter (9 -> V)
    assert rre.it.codice_fiscale("RCCMNL83S18D96VW") == ["RCCMNL83S18D96VW"]
    assert rre.it.codice_fiscale("RSSMRA85T10A562T") == []
    # right check letter, but 31 November does not exist
    assert rre.it.codice_fiscale("RCCMNL83S31D969Q") == []


def test_partita_iva():
    assert rre.it.partita_iva("P.IVA 07643520567 e 00743110157") == ["07643520567", "00743110157"]
    assert rre.it.partita_iva("07643520568") == []
    assert rre.it.partita_iva("12345675002") == []  # Luhn is right, office code 500 does not exist


def test_vat_number():
    assert rre.it.vat_number("IT07643520567 o IT 00743110157") == ["IT07643520567", "IT 00743110157"]
    assert rre.it.vat_number("IT07643520568") == []


def test_iban():
    assert rre.it.iban("IBAN IT60 X054 2811 1010 0000 0123 456 o IT60X0542811101000000123456") == [
        "IT60 X054 2811 1010 0000 0123 456", "IT60X0542811101000000123456"]
    assert rre.it.iban("IT60 X054 2811 1010 0000 0123 457") == []


def test_bic():
    assert rre.it.bic("BIC UNCRITMM o BCITITMMXXX") == ["UNCRITMM", "BCITITMMXXX"]
    assert rre.it.bic("BNPAFRPP") == []


def test_id_card_number():
    assert rre.it.id_card_number("CIE n. CA00000AA") == ["CA00000AA"]
    assert rre.it.id_card_number("CA0000AA e CA000000AA") == []


def test_passport_number():
    assert rre.it.passport_number("passaporto n. YA1234567 e PASSPORT: YB7654321") == ["YA1234567", "YB7654321"]
    assert rre.it.passport_number("passaporto YA123456 e YAB1234567") == []


def test_mrz_id_card():
    line = "CIITACA00000AA4" + "<" * 15
    assert rre.it.mrz_id_card(f"mrz {line}") == [line]
    assert rre.it.mrz_id_card("CIITACA00000AA5" + "<" * 15) == []


def test_mrz_passport():
    # ICAO 9303 specimen with ITA nationality
    line = "L898902C36ITA7408122F1204159ZE184226B<<<<<10"
    assert rre.it.mrz_passport(line) == [line]
    assert rre.it.mrz_passport(line.replace("C36", "C37")) == []


def test_phone_number():
    # example numbers from libphonenumber's metadata: Italy has no range reserved for fiction
    assert rre.it.phone_number("tel 02 1234 5678, +39 02 12345678, 312 345 6789 o 0571 123456") == [
        "02 1234 5678", "+39 02 12345678", "312 345 6789", "0571 123456"]
    assert rre.it.phone_number("il 01/02/2024, orario 08.30-12.30, +3531234567") == []
    # a Belgian KBO number and the digit groups of an IBAN
    assert rre.it.phone_number("KBO 0123.456.749, IBAN DE89 3704 0044 0532 0130 00") == []


def test_mobile_number():
    assert rre.it.mobile_number("cell +39 312 345 6789, 3123456789 o 312/3456789") == [
        "+39 312 345 6789", "3123456789", "312/3456789"]
    assert rre.it.mobile_number("02 1234 5678 e 32470123456") == []


def test_premium_number():
    assert rre.it.premium_number("chiama 899 123 456 o 899123456") == ["899 123 456", "899123456"]
    assert rre.it.premium_number("verde 800 123 456, € 899.000") == []


def test_msisdn():
    assert rre.it.msisdn("msisdn 393123456789") == ["393123456789"]
    assert rre.it.msisdn("390212345678") == []


def test_imsi():
    assert rre.it.imsi("imsi 222011234567890") == ["222011234567890"]
    assert rre.it.imsi("imsi 214011234567890") == []


def test_iccid():
    assert rre.it.iccid("sim 8939011234567890127") == ["8939011234567890127"]
    assert rre.it.iccid("sim 8939011234567890128") == []


def test_license_plate():
    assert rre.it.license_plate("targa AB 123 CD ed EF456GH") == ["AB 123 CD", "EF456GH"]
    assert rre.it.license_plate("AI 123 CD, AB 1234 CD") == []


def test_postal_code_city():
    assert rre.it.postal_code_city("00184 Roma e 20121 Milano (MI)") == ["00184 Roma", "20121 Milano (MI)"]
    assert rre.it.postal_code_city("40017 San Giovanni in Persiceto (BO), 42121 Reggio nell'Emilia") == [
        "40017 San Giovanni in Persiceto (BO)", "42121 Reggio nell'Emilia"]
    assert rre.it.postal_code_city("10000 Euro, 2024 Roma") == []


def test_street_address():
    assert rre.it.street_address("abita in Via Roma 1, Milano") == ["Via Roma 1"]
    assert rre.it.street_address("Via Giuseppe Garibaldi, 12/A e Piazza della Repubblica n. 5") == [
        "Via Giuseppe Garibaldi, 12/A", "Piazza della Repubblica n. 5"]
    assert rre.it.street_address("Corso Vittorio Emanuele II 23") == ["Corso Vittorio Emanuele II 23"]
    assert rre.it.street_address("via email 3 volte, Via libera a 2 decreti") == []


def test_company_name():
    assert rre.it.company_name("tra Rossi Costruzioni S.r.l. e Fiat S.p.A.") == ["Rossi Costruzioni S.r.l.", "Fiat S.p.A."]
    assert rre.it.company_name("Bianchi & C. S.n.c. e ROSSI SRL") == ["Bianchi & C. S.n.c.", "ROSSI SRL"]
    assert rre.it.company_name("la srl di Mario") == []


def test_ecli():
    assert rre.it.ecli("vedi ECLI:IT:CASS:2016:12345CIV.") == ["ECLI:IT:CASS:2016:12345CIV"]
    assert rre.it.ecli("ECLI:ES:TS:2015:1234") == []


def test_aircraft_registration():
    assert rre.it.aircraft_registration("aereo I-ABCD") == ["I-ABCD"]
    assert rre.it.aircraft_registration("I-ABC e HI-ABCD") == []
