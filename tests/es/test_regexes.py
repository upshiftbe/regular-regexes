from regular_regexes import rre


def test_dni():
    # 99999999R is the specimen DNI
    assert rre.es.dni("DNI 12345678Z, 12.345.678-Z y 99999999R") == ["12345678Z", "12.345.678-Z", "99999999R"]
    assert rre.es.dni("12345678A") == []
    assert rre.es.dni("123456789Z") == []


def test_nie():
    assert rre.es.nie("NIE X1234567L o Y-1234567-X") == ["X1234567L", "Y-1234567-X"]
    assert rre.es.nie("X1234567M") == []
    assert rre.es.nie("W1234567L") == []


def test_cif():
    assert rre.es.cif("CIF B-12345674 y J99216582") == ["B-12345674", "J99216582"]
    assert rre.es.cif("Q1234567D") == ["Q1234567D"]  # control as a letter
    assert rre.es.cif("B12345675") == []
    assert rre.es.cif("I12345674") == []


def test_vat_number():
    assert rre.es.vat_number("NIF-IVA ESB12345674, ES12345678Z, ESX1234567L") == [
        "ESB12345674", "ES12345678Z", "ESX1234567L"]
    assert rre.es.vat_number("ESB12345675") == []
    assert rre.es.vat_number("ES1234567Z") == []


def test_social_security_number():
    assert rre.es.social_security_number("NSS 28/12345678/40 y 281234567840") == ["28/12345678/40", "281234567840"]
    # a number below 10 000 000 is counted without its leading zero, also in the old 11-digit form
    assert rre.es.social_security_number("08 01234567 74 o 28/1234567/42") == ["08 01234567 74", "28/1234567/42"]
    assert rre.es.social_security_number("281234567841") == []
    assert rre.es.social_security_number("991234567840") == []  # no province 99


def test_iban():
    assert rre.es.iban("IBAN ES91 2100 0418 4502 0005 1332 o ES91 2100 0418 45 0200051332") == [
        "ES91 2100 0418 4502 0005 1332", "ES91 2100 0418 45 0200051332"]
    assert rre.es.iban("ES91 2100 0418 4502 0005 1333") == []
    assert rre.es.iban("NL91ABNA0417164300") == []


def test_bic():
    assert rre.es.bic("BIC CAIXESBBXXX o BSCHESMM") == ["CAIXESBBXXX", "BSCHESMM"]
    assert rre.es.bic("GEBABEBB") == []


def test_passport_number():
    assert rre.es.passport_number("nº de pasaporte PAA123456, Passport No. XDA654321") == ["PAA123456", "XDA654321"]
    assert rre.es.passport_number("pasaporte PA123456 y PAA1234567") == []


def test_mrz_id_card():
    # DNI 3.0 specimen: support number BAA000589, DNI 99999999R in the optional field
    line = "IDESPBAA000589599999999R<<<<<<"
    assert rre.es.mrz_id_card(f"mrz {line}") == [line]
    assert rre.es.mrz_id_card(line[:14] + "6" + line[15:]) == []  # check digit 5 changed
    assert rre.es.mrz_id_card(line.replace("ESP", "ITA")) == []


def test_mrz_passport():
    # ICAO 9303 specimen with ESP nationality
    line = "L898902C36ESP7408122F1204159ZE184226B<<<<<10"
    assert rre.es.mrz_passport(line) == [line]
    assert rre.es.mrz_passport(line.replace("C36", "C37")) == []


def test_phone_number():
    # example numbers from libphonenumber's metadata: Spain has no range reserved for fiction
    assert rre.es.phone_number("llama al +34 612 34 56 78, al 810 123 456 o al 0034 81 012 34 56") == [
        "+34 612 34 56 78", "810 123 456", "0034 81 012 34 56"]
    assert rre.es.phone_number("el 12/05/2024, ref 34612345678 y 6123456789") == []


def test_mobile_number():
    assert rre.es.mobile_number("móvil 612 345 678 o +34 712345678") == ["612 345 678", "+34 712345678"]
    assert rre.es.mobile_number("810 123 456 y 701 234 567") == []


def test_premium_number():
    assert rre.es.premium_number("llame al 803 123 456 o al 806 12 34 56") == ["803 123 456", "806 12 34 56"]
    assert rre.es.premium_number("gratis 800 123 456") == []


def test_msisdn():
    assert rre.es.msisdn("msisdn 34612345678") == ["34612345678"]
    assert rre.es.msisdn("34810123456 y 3461234567") == []


def test_imsi():
    assert rre.es.imsi("imsi 214011234567890") == ["214011234567890"]
    assert rre.es.imsi("imsi 222011234567890") == []


def test_iccid():
    assert rre.es.iccid("sim 8934011234567890128") == ["8934011234567890128"]
    assert rre.es.iccid("sim 8934011234567890127") == []


def test_license_plate():
    assert rre.es.license_plate("coche 1234 BCD, 1234-BCD y 5678BCD") == ["1234 BCD", "1234-BCD", "5678BCD"]
    assert rre.es.license_plate("antiguas M-1234-AB y MA 1234 B") == ["M-1234-AB", "MA 1234 B"]
    assert rre.es.license_plate("1234 ABC, 5000 GBP, M-1234 AB") == []


def test_postal_code_city():
    assert rre.es.postal_code_city("28013 Madrid y 28801 Alcalá de Henares (Madrid)") == [
        "28013 Madrid", "28801 Alcalá de Henares (Madrid)"]
    assert rre.es.postal_code_city("15001 A Coruña") == ["15001 A Coruña"]
    assert rre.es.postal_code_city("99999 Madrid, 10000 Euros") == []


def test_street_address():
    assert rre.es.street_address("vive en Calle Mayor 12, 3º B de Madrid") == ["Calle Mayor 12, 3º B"]
    assert rre.es.street_address("C/ Alcalá, 45 y Avda. de la Constitución nº 7") == [
        "C/ Alcalá, 45", "Avda. de la Constitución nº 7"]
    assert rre.es.street_address("Plaza Mayor s/n, Paseo de Gracia 92, 2º 1ª") == [
        "Plaza Mayor s/n", "Paseo de Gracia 92, 2º 1ª"]
    assert rre.es.street_address("Calle sin número, el paseo de 3 horas") == []


def test_company_name():
    assert rre.es.company_name("entre Construcciones García S.L. y Telefónica, S.A.") == [
        "Construcciones García S.L.", "Telefónica, S.A."]
    assert rre.es.company_name("Fomento de Construcciones y Contratas, S.A.U.") == [
        "Fomento de Construcciones y Contratas, S.A.U."]
    assert rre.es.company_name("la sa de Juan") == []


def test_ecli():
    assert rre.es.ecli("ver ECLI:ES:TS:2015:1234A.") == ["ECLI:ES:TS:2015:1234A"]
    assert rre.es.ecli("ECLI:BE:CASS:2020:ARR.20200115.1") == []


def test_aircraft_registration():
    assert rre.es.aircraft_registration("avión EC-XYZ") == ["EC-XYZ"]
    assert rre.es.aircraft_registration("EC-AB, EC-1234 y DEC-XYZ") == []
