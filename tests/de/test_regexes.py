from regular_regexes import rre


def test_tax_id():
    # examples from the ELSTER IdNr specification (ITZBund concept)
    assert rre.de.tax_id("IdNr 86 095 742 719 und 65929970489") == ["86 095 742 719", "65929970489"]
    assert rre.de.tax_id("86095742718") == []
    # check digit right, but the 9 occurs four times / three times in a row
    assert rre.de.tax_id("65999970482 65299970480") == []


def test_vat_number():
    assert rre.de.vat_number("USt-IdNr. DE123456788 oder DE 123 456 788") == ["DE123456788", "DE 123 456 788"]
    assert rre.de.vat_number("DE123456789") == []
    assert rre.de.vat_number("DE12345678") == []


def test_pension_insurance_number():
    # fictitious example from the Versicherungsnummer article on de.wikipedia
    assert rre.de.pension_insurance_number("SV-Nr. 15 070649 C 103 und 15070649C103") == [
        "15 070649 C 103", "15070649C103"]
    assert rre.de.pension_insurance_number("15 070649 C 104") == []
    assert rre.de.pension_insurance_number("22 070649 C 103") == []  # no carrier has area number 22


def test_health_insurance_number():
    # specimen from the GKV check digit annex (Anlage 1, Prüfziffernberechnung KVNR)
    assert rre.de.health_insurance_number("KVNR A000500015 und C000500021") == ["A000500015", "C000500021"]
    assert rre.de.health_insurance_number("A000500016") == []
    assert rre.de.health_insurance_number("AB00500015") == []


def test_id_card_number():
    # BMI specimen (Erika Mustermann)
    assert rre.de.id_card_number("Ausweisnummer T22000129") == ["T22000129"]
    assert rre.de.id_card_number("Pass C01X00T47, geschwärzt XXXXXXXXX") == []


def test_passport_number():
    assert rre.de.passport_number("Reisepass C01X00T47") == ["C01X00T47"]
    assert rre.de.passport_number("Ausweis T22000129, Pass C01X00T4") == []


def test_mrz_id_card():
    line = "IDD<<T220001293<<<<<<<<<<<<<<<"
    assert rre.de.mrz_id_card(f"mrz {line}") == [line]
    assert rre.de.mrz_id_card(line.replace("1293", "1294")) == []
    assert rre.de.mrz_id_card("IDBEL592123456<782" + "<" * 12) == []


def test_mrz_passport():
    line = "C01X00T478D<<6408125F2702283<<<<<<<<<<<<<<<4"
    assert rre.de.mrz_passport(line) == [line]
    assert rre.de.mrz_passport(line.replace("T478", "T479")) == []
    assert rre.de.mrz_passport("L898902C36BEL7408122F1204159ZE184226B<<<<<10") == []


def test_company_register_number():
    assert rre.de.company_register_number("Amtsgericht München HRB 123456, Sitz Köln") == ["Amtsgericht München HRB 123456"]
    assert rre.de.company_register_number("AG Charlottenburg, HRB 12345 B und HR A 4711") == [
        "AG Charlottenburg, HRB 12345 B", "HR A 4711"]
    assert rre.de.company_register_number("HRB 12345 AG Köln") == ["HRB 12345"]
    assert rre.de.company_register_number("HRC 12345 oder HRB 0123") == []


def test_iban():
    assert rre.de.iban("IBAN DE89 3704 0044 0532 0130 00 bitte") == ["DE89 3704 0044 0532 0130 00"]
    assert rre.de.iban("DE89 3704 0044 0532 0130 01") == []
    assert rre.de.iban("BE68 5390 0754 7034") == []


def test_bic():
    assert rre.de.bic("BIC COBADEFFXXX oder DEUTDEFF") == ["COBADEFFXXX", "DEUTDEFF"]
    assert rre.de.bic("GEBABEBB") == []


def test_phone_number():
    # Bundesnetzagentur drama numbers
    assert rre.de.phone_number("Tel. 030 23125000, (069) 90009 123 oder +49 (0)89 99998 000") == [
        "030 23125000", "(069) 90009 123", "+49 (0)89 99998 000"]
    assert rre.de.phone_number("040 / 66969 999 und 0221-4710123") == ["040 / 66969 999", "0221-4710123"]
    assert rre.de.phone_number("am 01.02.2024, PLZ 01067, IBAN DE89 3704 0044 0532 0130 00") == []


def test_mobile_number():
    # Bundesnetzagentur drama numbers
    assert rre.de.mobile_number("Handy 0152 28817386, +49 171 3920012 oder 0176/04069000") == [
        "0152 28817386", "+49 171 3920012", "0176/04069000"]
    assert rre.de.mobile_number("Festnetz 030 23125000") == []


def test_msisdn():
    assert rre.de.msisdn("msisdn 4915228817386 und 491713920012") == ["4915228817386", "491713920012"]
    assert rre.de.msisdn("493023125000") == []


def test_premium_number():
    assert rre.de.premium_number("ruf 0900 5 123456 an, oder 0180-5 123 456") == ["0900 5 123456", "0180-5 123 456"]
    assert rre.de.premium_number("kostenlos 0800 1234567") == []


def test_imsi():
    assert rre.de.imsi("imsi 262011234567890") == ["262011234567890"]
    assert rre.de.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.de.iccid("sim 8949020000123456788") == ["8949020000123456788"]
    assert rre.de.iccid("sim 8949020000123456789") == []
    assert rre.de.iccid("sim 89320112345678901232") == []


def test_license_plate():
    assert rre.de.license_plate("Kennzeichen B-MW 1234, M AB 123 und HH-XY 99E") == ["B-MW 1234", "M AB 123", "HH-XY 99E"]
    assert rre.de.license_plate("LÖ-K 7H") == ["LÖ-K 7H"]
    assert rre.de.license_plate("nicht 12-AB-34 oder B-MW 0123") == []


def test_postal_code_city():
    assert rre.de.postal_code_city("10115 Berlin und 60311 Frankfurt am Main") == ["10115 Berlin", "60311 Frankfurt am Main"]
    assert rre.de.postal_code_city("D-06108 Halle (Saale)") == ["D-06108 Halle (Saale)"]
    assert rre.de.postal_code_city("für 15000 Euro an 20000 Menschen") == []


def test_street_address():
    assert rre.de.street_address("wohnt Hauptstraße 12, früher Bahnhofstr. 5a") == ["Hauptstraße 12", "Bahnhofstr. 5a"]
    assert rre.de.street_address("Berliner Straße 5-7 oder Am Markt 3") == ["Berliner Straße 5-7", "Am Markt 3"]
    assert rre.de.street_address("Karl-Marx-Allee 90 und Lindenweg 4") == ["Karl-Marx-Allee 90", "Lindenweg 4"]
    assert rre.de.street_address("Im Jahr 2020 auf Parkplatz 3") == []
    assert rre.de.street_address("Bring 3 copies") == []


def test_company_name():
    assert rre.de.company_name("Vertrag zwischen Müller Bau GmbH und Hans Meier GmbH & Co. KG") == [
        "Müller Bau GmbH", "Hans Meier GmbH & Co. KG"]
    assert rre.de.company_name("Die Muster UG (haftungsbeschränkt) und Sportverein Blau-Weiß e.V.") == [
        "Muster UG (haftungsbeschränkt)", "Sportverein Blau-Weiß e.V."]
    assert rre.de.company_name("die ag von Jan, Registergericht AG München") == []


def test_aircraft_registration():
    assert rre.de.aircraft_registration("Flug mit D-AIMA und D-EABC") == ["D-AIMA", "D-EABC"]
    assert rre.de.aircraft_registration("OO-ABC, D-ABC und AD-ABCD") == []


def test_ecli():
    assert rre.de.ecli("siehe ECLI:DE:BVerfG:2018:rk20181212.2bvr145518.") == [
        "ECLI:DE:BVerfG:2018:rk20181212.2bvr145518"]
    assert rre.de.ecli("ECLI:DE:BGH:2017:290317UIXZR86.16.0 und ECLI:NL:HR:2020:1234") == [
        "ECLI:DE:BGH:2017:290317UIXZR86.16.0"]
