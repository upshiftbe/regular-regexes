import time

from regular_regexes import rre


def test_license_plate():
    assert rre.be.license_plate("car 1-ABC-123 and 2XYZ987") == ["1-ABC-123", "2XYZ987"]
    assert rre.be.license_plate("old ABC-123 and 123-ABC") == ["ABC-123", "123-ABC"]
    assert rre.be.license_plate("nothing 12-AB-34 here") == []


def test_national_number():
    assert rre.be.national_number("rr 85.07.30-033.28") == ["85.07.30-033.28"]
    assert rre.be.national_number("born 2005: 05073003326") == ["05073003326"]
    assert rre.be.national_number("85.07.30-033.29") == []


def test_enterprise_number():
    assert rre.be.enterprise_number("KBO 0123.456.749") == ["0123.456.749"]
    assert rre.be.enterprise_number("KBO 0123.456.748") == []


def test_iban():
    assert rre.be.iban("pay to BE68 5390 0754 7034 please") == ["BE68 5390 0754 7034"]
    assert rre.be.iban("BE68 5390 0754 7035") == []


def test_phone_number():
    assert rre.be.phone_number("call +32 470 12 34 56 or 02/234.56.78") == ["+32 470 12 34 56", "02/234.56.78"]


def test_bis_number():
    assert rre.be.bis_number("bis 85.27.30-033.71") == ["85.27.30-033.71"]
    assert rre.be.bis_number("85.07.30-033.28") == []  # valid national number, but not a bis number
    assert rre.be.bis_number("85.27.30-033.72") == []


def test_eid_card_number():
    assert rre.be.eid_card_number("kaart 592-1234567-32") == ["592-1234567-32"]
    assert rre.be.eid_card_number("kaart 592-1234567-33") == []


def test_passport_number():
    assert rre.be.passport_number("paspoort EH123456") == ["EH123456"]
    assert rre.be.passport_number("EH12345") == []


def test_mrz_id_card():
    line = "IDBEL592123456<782" + "<" * 12
    assert rre.be.mrz_id_card(f"mrz {line}") == [line]
    assert rre.be.mrz_id_card("IDBEL592123456<783" + "<" * 12) == []


def test_mrz_passport():
    # ICAO 9303 specimen with BEL nationality
    line = "L898902C36BEL7408122F1204159ZE184226B<<<<<10"
    assert rre.be.mrz_passport(line) == [line]
    assert rre.be.mrz_passport(line.replace("C36", "C37")) == []


def test_bban():
    assert rre.be.bban("rekening 539-0075470-34") == ["539-0075470-34"]
    assert rre.be.bban("rekening 539-0075470-35") == []


def test_bic():
    assert rre.be.bic("BIC GEBABEBB of KREDBEBBXXX") == ["GEBABEBB", "KREDBEBBXXX"]
    assert rre.be.bic("ABNANL2A") == []


def test_structured_communication():
    assert rre.be.structured_communication("+++123/4567/89002+++ en ***123/4567/89002***") == [
        "+++123/4567/89002+++", "***123/4567/89002***"]
    assert rre.be.structured_communication("+++123/4567/89003+++") == []
    assert rre.be.structured_communication("+++123/4567/89002***") == []


def test_bancontact_card():
    assert rre.be.bancontact_card("kaart 6703 1234 5678 9012 1") == ["6703 1234 5678 9012 1"]
    assert rre.be.bancontact_card("67031234567890122") == []


def test_vat_number():
    assert rre.be.vat_number("btw BE0123.456.749") == ["BE0123.456.749"]
    assert rre.be.vat_number("BE 0123456748") == []


def test_establishment_number():
    assert rre.be.establishment_number("vestiging 2.123.456.791") == ["2.123.456.791"]
    assert rre.be.establishment_number("2.123.456.792") == []


def test_company_name():
    assert rre.be.company_name("contract tussen Janssens Bouw BV en Dupont SRL") == ["Janssens Bouw BV", "Dupont SRL"]
    assert rre.be.company_name("de bv van Jan") == []


def test_amount_eur():
    assert rre.be.amount_eur("betaald € 1.234,56 en 250 EUR") == ["€ 1.234,56", "250 EUR"]
    assert rre.be.amount_eur("in 2024 betaald") == []


def test_mobile_number():
    assert rre.be.mobile_number("gsm 0470 12 34 56 of +32 499/12.34.56") == ["0470 12 34 56", "+32 499/12.34.56"]
    assert rre.be.mobile_number("02 123 45 67") == []


def test_msisdn():
    assert rre.be.msisdn("msisdn 32470123456") == ["32470123456"]
    assert rre.be.msisdn("3221234567") == []


def test_premium_number():
    assert rre.be.premium_number("bel 0900 12 345 of 070 22 33 44") == ["0900 12 345", "070 22 33 44"]


def test_imsi():
    assert rre.be.imsi("imsi 206011234567890") == ["206011234567890"]
    assert rre.be.imsi("imsi 204011234567890") == []


def test_iccid():
    assert rre.be.iccid("sim 89320112345678901232") == ["89320112345678901232"]
    assert rre.be.iccid("sim 89320112345678901233") == []


def test_ecli():
    assert rre.be.ecli("zie ECLI:BE:CASS:2020:ARR.20200115.1.") == ["ECLI:BE:CASS:2020:ARR.20200115.1"]


def test_street_address_nl():
    assert rre.be.street_address_nl("woont Kerkstraat 12 bus 3, Gent") == ["Kerkstraat 12 bus 3"]
    assert rre.be.street_address_nl("Stationslaan 5 bij de kerk") == ["Stationslaan 5"]


def test_street_address_fr():
    assert rre.be.street_address_fr("habite Rue de la Loi 16 bte 2") == ["Rue de la Loi 16 bte 2"]
    assert rre.be.street_address_fr("Avenue Louise 54") == ["Avenue Louise 54"]


def test_postal_code_city():
    assert rre.be.postal_code_city("9000 Gent en 1000 Bruxelles") == ["9000 Gent", "1000 Bruxelles"]
    assert rre.be.postal_code_city("9100 Sint-Niklaas") == ["9100 Sint-Niklaas"]


def test_date_text():
    assert rre.be.date_text("op 12 januari 2024, le 1er mars 2023, am 3. März 2022") == [
        "12 januari 2024", "1er mars 2023", "3. März 2022"]


def test_date_numeric():
    assert rre.be.date_numeric("op 12/01/2024 en 3.2.24") == ["12/01/2024", "3.2.24"]
    assert rre.be.date_numeric("12/01.2024") == []


def test_time():
    assert rre.be.time("om 14u30, 9h05 en 23:59") == ["14u30", "9h05", "23:59"]
    assert rre.be.time("24u00") == []


def test_domain_be():
    assert rre.be.domain_be("zie www.politie.be en stad.brussels") == ["www.politie.be", "stad.brussels"]
    assert rre.be.domain_be("example.com") == []
    assert rre.be.domain_be("mail jan@test.be, info.be@gmail.com or jan@sub.stad.gent") == []


def test_aircraft_registration():
    assert rre.be.aircraft_registration("OO-SNA, ULM OO-I36, paramotor OO-1AB en zelfbouw OO-123") == [
        "OO-SNA", "OO-I36", "OO-1AB", "OO-123"]
    assert rre.be.aircraft_registration("OO-AB, OO-ABCD en FOO-ABC") == []


def test_long_runs_stay_fast():
    # these used to retry from every word of a long run: minutes on 100 KB.
    # The last run checks that domain_be looks at most 64 characters ahead for an email's @.
    start = time.perf_counter()
    for text in ('1-' * 25000, 'A ' * 25000, 'L-' * 25000, 'A.' * 25000, 'x.be.' * 20000 + '@'):
        rre.be.domain_be(text), rre.be.company_name(text), rre.be.street_address_nl(text)
    assert time.perf_counter() - start < 1


def test_bpost_tracking_number():
    # examples from bpost's FAQ
    text = "bpost 329998745632147852365873, 323256984521032569 en JJBEA2356412012365478896541"
    assert rre.be.bpost_tracking_number(text) == [
        "329998745632147852365873", "323256984521032569", "JJBEA2356412012365478896541"]
    # too short, another prefix, 19 digits
    assert rre.be.bpost_tracking_number("329998745632147852365 123256984521032569 3232569845210325691") == []


def test_pv_number():
    assert rre.be.pv_number("pv AN.55.LB.000123/2026 en HA.43.L1.012345/16") == [
        "AN.55.LB.000123/2026", "HA.43.L1.012345/16"]
    # as the parket writes it: no dot after its code, or a dash before the year
    assert rre.be.pv_number("parket AN55.L1.012345/26 en KO43.F0.004567-24") == ["AN55.L1.012345/26", "KO43.F0.004567-24"]
    assert rre.be.pv_number("AN.5.LB.000123/2026, AN.55.12.000123/2026, AN.55.LB.12/2026, file 23/1234/A") == []


def test_notice_number():
    assert rre.be.notice_number("Notitienummer: AN55.L1.012345/26, not.nr. KO.43.L2.004567/24") == [
        "Notitienummer: AN55.L1.012345/26", "not.nr. KO.43.L2.004567/24"]
    assert rre.be.notice_number("numéro de notice : CH.55.L1.012345/14, notitienummer parket GE/D/43/12/1234/2024") == [
        "numéro de notice : CH.55.L1.012345/14", "notitienummer parket GE/D/43/12/1234/2024"]
    assert rre.be.notice_number("pv AN.55.LB.000123/2026") == []  # no label


def test_docket_number():
    assert rre.be.docket_number("rolnummer 2026/AR/1234, 2025/AB/123 en R.G. n° 2024/RG/12") == [
        "rolnummer 2026/AR/1234", "2025/AB/123", "R.G. n° 2024/RG/12"]
    assert rre.be.docket_number("Cass. P.24.0123.N en 26/CAS/0123") == ["P.24.0123.N", "26/CAS/0123"]
    # first instance, enterprise court and justice of the peace only after their label
    assert rre.be.docket_number("AR 26/1234/A, rolnummer A/26/01234 en A.R. nr. 26A1234") == [
        "AR 26/1234/A", "rolnummer A/26/01234", "A.R. nr. 26A1234"]
    assert rre.be.docket_number("file 23/1234/A, ref 2024/HR/12, factuur 2024/0172, AR 12/03/2024") == []


def test_birth_date():
    assert rre.be.birth_date("Jan (° 3/2/1990), geboren te Sint-Niklaas op 1 januari 1980") == [
        "° 3/2/1990", "geboren te Sint-Niklaas op 1 januari 1980"]
    assert rre.be.birth_date("née à La Louvière le 1er mars 1990, geb. am 3. März 1990, DOB: 12/03/1990") == [
        "née à La Louvière le 1er mars 1990", "geb. am 3. März 1990", "DOB: 12/03/1990"]
    assert rre.be.birth_date("n° 12/03/2024, 21.5 °C, geboren in Marokko en kwam op 12/03/2010") == []


def test_birth_date_named_group():
    # the date alone is in the group "date", for whoever uses the pattern directly
    import json
    import re
    from pathlib import Path

    import regular_regexes
    regexes = json.loads((Path(regular_regexes.__file__).parent / 'be' / 'regexes.json').read_text(encoding='utf-8'))
    assert re.search(regexes['birth_date'], "geboren te Gent op 1 januari 1980").group('date') == "1 januari 1980"


def test_driving_licence_number():
    # 0123456789 is the number on the PRADO specimens of the card (BEL-FO-03001, BEL-FO-05001)
    assert rre.be.driving_licence_number("rijbewijs nr. 0123456789, permis de conduire n° 0123456789") == [
        "rijbewijs nr. 0123456789", "permis de conduire n° 0123456789"]
    assert rre.be.driving_licence_number("Führerschein-Nr. 0123456789, driving licence number 0123456789") == [
        "Führerschein-Nr. 0123456789", "driving licence number 0123456789"]
    assert rre.be.driving_licence_number("gsm 0470123456, ondernemingsnummer 0123456749, permis de séjour 0123456789") == []


def test_case_numbers_stay_fast():
    start = time.perf_counter()
    for text in ('AN.55.' * 20000, 'R.G. n° ' * 15000, '° ' * 50000, 'geboren te Gent ' * 7000, 'rijbewijs nr. ' * 8000):
        for find in (rre.be.pv_number, rre.be.notice_number, rre.be.docket_number, rre.be.birth_date,
                     rre.be.driving_licence_number):
            find(text)
    assert time.perf_counter() - start < 1


# Hardened tests: per regex, six or more written forms that match and six or more near-misses that do not,
# each near-miss in its own call. Check digits are computed for made-up numbers.

def _check(find, found, missed):
    for text, expected in found:
        assert find(text) == expected, text
    for text in missed:
        assert find(text) == [], text


def test_hard_aircraft_registration():
    _check(rre.be.aircraft_registration, [
        ("OO-SNA", ["OO-SNA"]),
        ("Het toestel (OO-JEF) landde in Deurne.", ["OO-JEF"]),
        ("L'avion immatriculé OO-VAS a atterri.", ["OO-VAS"]),
        ('ULM "OO-B52"', ["OO-B52"]),
        ("Gleitschirm OO-9XY.", ["OO-9XY"]),
        ("zelfbouw OO-45", ["OO-45"]),
    ], ["OO-AB", "OO-ABCD", "FOO-ABC", "OO-0AB", "OO-1234", "PH-ABC", "OO ABC", "OO-SNA1", "D-EABC"])


def test_hard_amount_eur():
    _check(rre.be.amount_eur, [
        ("€ 1.234,56", ["€ 1.234,56"]),
        ("totaal 99,95€.", ["99,95€"]),
        ("le prix est de 1 249,99 euros", ["1 249,99 euros"]),
        ("Eintritt 12 Euro", ["12 Euro"]),
        ("(€50,-)", ["€50,-"]),
        ("boete van 1.000.000 EUR", ["1.000.000 EUR"]),
        ("€1234", ["€1234"]),
        ("250 eur", ["250 eur"]),
        ("1 249,99 €", ["1 249,99 €"]),
        ("in 2024 250 EUR", ["250 EUR"]),  # the year is not part of the amount
    ], ["€ 12.50", "€ 1.234,5", "250 eurocent", "$ 250", "250 USD", "1,5 EUR", "€ 1.23", "v2.250 EUR",
        "1.234.567.890.123.456 EUR"])
    start = time.perf_counter()
    rre.be.amount_eur('070 ' * 25000)  # used to try every group of digits from every start: seconds on 100 KB
    assert time.perf_counter() - start < 1


def test_hard_bancontact_card():
    _check(rre.be.bancontact_card, [
        ("67031234567890121", ["67031234567890121"]),
        ("kaart 6703 0000 0000 0000 3.", ["6703 0000 0000 0000 3"]),
        ("carte n° 6703-9876-5432-1098-0", ["6703-9876-5432-1098-0"]),
        ("(6703 1111 2222 3333 7)", ["6703 1111 2222 3333 7"]),
        ("Bankkarte: 67035555666677779,", ["67035555666677779"]),
        ("« 6703 2468 1357 9024 4 »", ["6703 2468 1357 9024 4"]),
    ], ["6703123456789012", "670312345678901210", "6704 1234 5678 9012 1", "x67031234567890121",
        "4111 1111 1111 1111", "6703  1234 5678 9012 1", "6703 1234 5678 9012 2"])


def test_hard_bban():
    _check(rre.be.bban, [
        ("001-0000000-76", ["001-0000000-76"]),
        ("rekening 310-1234567-37.", ["310-1234567-37"]),
        ("compte n° 735-0012345-14, merci", ["735-0012345-14"]),
        ("(063-0987654-35)", ["063-0987654-35"]),
        ('Konto "979-0555555-41"', ["979-0555555-41"]),
        ("539-0075470-34", ["539-0075470-34"]),
    ], ["539007547034", "5390-075470-34", "539-0075470-345", "1-539-0075470-34", "539-0075470-34-1",
        "12-03-2024", "BE68 5390 0754 7034"])


def test_hard_bic():
    _check(rre.be.bic, [
        ("ABCDBEBB", ["ABCDBEBB"]),
        ("BIC: ZYXWBE22.", ["ZYXWBE22"]),
        ("(QRSTBEB1XXX)", ["QRSTBEB1XXX"]),
        ("code SWIFT MNOPBE9A, merci", ["MNOPBE9A"]),
        ('BIC-code "EFGHBEBB123"', ["EFGHBEBB123"]),
        ("Bank IJKLBE2X", ["IJKLBE2X"]),
    ], ["GEBABEB", "GEBABEBBX", "GEBABEBBXX", "gebabebb", "GEB1BEBB", "GEBAFRPP",
        # capitals that only look like one: no B or digit in the location code
        "PLUMBERS", "OVERBEEK", "COLEBERT"])


def test_hard_birth_date():
    _check(rre.be.birth_date, [
        ("Geboortedatum: 03.02.1990", ["Geboortedatum: 03.02.1990"]),
        ("date de naissance : 12-03-1985", ["date de naissance : 12-03-1985"]),
        ("born on 5 May 1990", ["born on 5 May 1990"]),
        ("Geburtsdatum 01.01.2000", ["Geburtsdatum 01.01.2000"]),
        ("(°12/03/1990)", ["°12/03/1990"]),
        ("née le 31 décembre 1985.", ["née le 31 décembre 1985"]),
    ], ["n° 12/03/2024", "21.5 °C", "geboren in Marokko en kwam op 12/03/2010", "geboren op 32/01/1990",
        "° 3/13/1990", "geboren op 12/03", "geboren op 12/03-1990", "DOB: 1990"])


def test_hard_bis_number():
    _check(rre.be.bis_number, [
        ("85.27.30-033.71", ["85.27.30-033.71"]),
        ("bisnummer 90.45.01-123.15.", ["90.45.01-123.15"]),
        ("numéro bis 75421299727", ["75421299727"]),
        ("(60.20.10-455.63)", ["60.20.10-455.63"]),
        ("BIS: 93.32.15-270.02,", ["93.32.15-270.02"]),
        ("85473003317", ["85473003317"]),
    ], ["75.00.20-001.04", "85.33.30-033.16", "85.53.30-033.59", "8527300337", "852730033711", "85.27.30-033.7"])


def test_hard_bpost_tracking_number():
    _check(rre.be.bpost_tracking_number, [
        ("pakje 323212345678901234567890.", ["323212345678901234567890"]),
        ("(JJBEA0000000000000000000001)", ["JJBEA0000000000000000000001"]),
        ("colis 323200000000000001,", ["323200000000000001"]),
    ], ["329998745632147852365", "123256984521032569", "3232569845210325691", "3299123456789012345678",
        "JJBEA235641201236547889654", "JJBEB2356412012365478896541", "3299987456321478523658731"])


def test_hard_company_name():
    _check(rre.be.company_name, [
        ("Janssens Bouw BV", ["Janssens Bouw BV"]),
        ("Peeters & Zonen NV.", ["Peeters & Zonen NV"]),
        ("la société Dupont Frères SA, à Liège", ["Dupont Frères SA"]),
        ("(Vlaamse Vereniging VZW)", ["Vlaamse Vereniging VZW"]),
        ("JANSSENS BVBA", ["JANSSENS BVBA"]),
        ("A.B.C. Bouw CommV", ["A.B.C. Bouw CommV"]),
        ("Janssens CV", ["Janssens CV"]),
        # a sentence or a line before the name is not part of it
        ("Ik woon in Gent. Janssens Bouw BV betaalt", ["Janssens Bouw BV"]),
        ("Factuur\nMartin SPRL", ["Martin SPRL"]),
    ], ["Stuur Uw CV naar ons", "Mijn CV", "Votre CV est complet", "Janssens BVs", "Janssens Bouw",
        "janssens bv", "Janssens GmbH"])


def test_hard_date_numeric():
    _check(rre.be.date_numeric, [
        ("12/01/2024", ["12/01/2024"]),
        ("le 31-12-1999.", ["31-12-1999"]),
        ("(01.01.2000)", ["01.01.2000"]),
        ("Datum: 7/8/2023,", ["7/8/2023"]),
        ("am 29.02.2024 um", ["29.02.2024"]),
        ("12/03/2024 14:30", ["12/03/2024"]),
    ], ["S-1-5-32-544", "06.12.34.56.78", "10.12.1.24", "32/01/2024", "12/13/2024", "12/03/202", "03/2026",
        "12-03-2024-001", "2024-03-12"])


def test_hard_date_text():
    _check(rre.be.date_text, [
        ("12 januari 2024", ["12 januari 2024"]),
        ("le 1er mars 2023,", ["1er mars 2023"]),
        ("Op 01 Mei 2020", ["01 Mei 2020"]),
        ("(15 août 1985)", ["15 août 1985"]),
        ("31 DECEMBER 1999", ["31 DECEMBER 1999"]),
        ("le 7 fevrier 2021", ["7 fevrier 2021"]),  # typed without its accent
        ("am 3. Maerz 2022.", ["3. Maerz 2022"]),
        ("am 9 Juli 2019", ["9 Juli 2019"]),
    ], ["32 januari 2024", "12 januari", "12 jan 2024", "12 january 2024", "12 janvier 24", "januari 2024",
        "112 januari 2024", "12 januari 20245"])


def test_hard_docket_number():
    _check(rre.be.docket_number, [
        ("numéro de rôle 2023/RG/456", ["numéro de rôle 2023/RG/456"]),
        ("(2024/NT/12)", ["2024/NT/12"]),
        ("Cass. C.21.0456.F.", ["C.21.0456.F"]),
    ], ["file 23/1234/A", "ref 2024/HR/12", "factuur 2024/0172", "AR 12/03/2024", "2026/AR/123456",
        "1826/AR/1234", "26/CAS/012345", "P.24.0123.X", "rolnummer 26/1234/ABC"])


def test_hard_domain_be():
    _check(rre.be.domain_be, [
        ("WWW.VOORBEELD.BE", ["WWW.VOORBEELD.BE"]),
        ("zie https://www.voorbeeld.be/nl/contact", ["www.voorbeeld.be"]),
        ("(mijn-site.vlaanderen)", ["mijn-site.vlaanderen"]),
        ("site: exemple.gent.", ["exemple.gent"]),
        ('"café.be"', ["café.be"]),
        ("Sub.Domein.Test.Be", ["Sub.Domein.Test.Be"]),
    ], ["jan@test.be", "info.be@gmail.com", "jan@sub.stad.gent", "test.be.com", "report.be.pdf", "politie.bel",
        "stad.gentse", ".be"])


def test_hard_driving_licence_number():
    _check(rre.be.driving_licence_number, [
        ("Rijbewijsnummer: 0123456789", ["Rijbewijsnummer: 0123456789"]),
        ("numéro du permis de conduire 0123456789.", ["numéro du permis de conduire 0123456789"]),
        ("Fuehrerscheinnummer 0123456789", ["Fuehrerscheinnummer 0123456789"]),
        ("driver's license #0123456789", ["driver's license #0123456789"]),
        ("RIJBEWIJS NR 0123456789", ["RIJBEWIJS NR 0123456789"]),
    ], ["gsm 0470123456", "ondernemingsnummer 0123456749", "permis de séjour 0123456789", "rijbewijs nr. 012345678",
        "rijbewijs nr. 01234567890", "rijbewijs 0123 456 789", "0123456789", "rijbewijsnummer x0123456789"])


def test_hard_ecli():
    _check(rre.be.ecli, [
        ("ECLI:BE:GHCC:2021:ARR.042", ["ECLI:BE:GHCC:2021:ARR.042"]),
        ("(ECLI:BE:RVSCE:2022:ARR.253123)", ["ECLI:BE:RVSCE:2022:ARR.253123"]),
        ("arrêt ECLI:BE:CTLIE:2019:ARR.20190301.2, voir", ["ECLI:BE:CTLIE:2019:ARR.20190301.2"]),
        ('Urteil "ECLI:BE:HBANT:2023:ARR.20230612.5"', ["ECLI:BE:HBANT:2023:ARR.20230612.5"]),
        ("ECLI:BE:CABRL:2018:ARR.20181120.12.", ["ECLI:BE:CABRL:2018:ARR.20181120.12"]),
    ], ["ECLI:NL:HR:2020:123", "ECLI:BE:CASS:20:ARR.1", "ECLI:BE:cass:2020:ARR.1", "ECLIBE:CASS:2020:ARR.1",
        "ECLI:BE:CASS:2020:", "XECLI:BE:CASS:2020:ARR.1",
        "ECLI:BE:CASS:2020:ARR.20200115.1abc"])  # not cut out of a longer word


def test_hard_eid_card_number():
    _check(rre.be.eid_card_number, [
        ("591-1234567-53", ["591-1234567-53"]),
        ("kaartnummer 593-0123456-35.", ["593-0123456-35"]),
        ("carte d'identité n° 600000004252,", ["600000004252"]),
        ("(599-0876543-82)", ["599-0876543-82"]),
        ('Ausweis "601111222310"', ["601111222310"]),
        ("592-0000001-82", ["592-0000001-82"]),
    ], ["592-1234567-33", "59212345673", "5921234567321", "x592123456732", "1-592-1234567-32", "592-1234567-32-5",
        "85.07.30-033.28", "0470 12 34 56"])


def test_hard_enterprise_number():
    _check(rre.be.enterprise_number, [
        ("0876.543.270", ["0876.543.270"]),
        ("ondernemingsnummer 1000.000.021.", ["1000.000.021"]),
        ("numéro d'entreprise 0200123470,", ["0200123470"]),
        ("(KBO 0999.555.504)", ["0999.555.504"]),
        ("BCE: 0555.555.523", ["0555.555.523"]),
        ("Unternehmensnummer 0123456749", ["0123456749"]),
    ], ["0123.456.748", "123.456.749", "2123.456.791", "01234567490", "x0123456749", "BE0123456749", "0470123456"])


def test_hard_establishment_number():
    _check(rre.be.establishment_number, [
        ("2.345.678.942", ["2.345.678.942"]),
        ("vestigingseenheid 4.567.890.148.", ["4.567.890.148"]),
        ("unité d'établissement n° 8765432120,", ["8765432120"]),
        ("(3.000.000.162)", ["3.000.000.162"]),
        ("Niederlassung 6.543.210.917", ["6.543.210.917"]),
        ("2.123.456.791", ["2.123.456.791"]),
    ], ["2.123.456.792", "9.999.999.917", "1.000.000.021", "2.123.456.79", "21234567910", "x2123456791",
        "0123.456.749"])


def test_hard_iban():
    _check(rre.be.iban, [
        ("BE09 0010 0000 0097", ["BE09 0010 0000 0097"]),
        ("IBAN: BE11310123456781.", ["BE11310123456781"]),
        ("compte BE21 7350 0123 4567, merci", ["BE21 7350 0123 4567"]),
        ("(BE41 0630 9876 5432)", ["BE41 0630 9876 5432"]),
        ('Konto "BE68 0001 2345 6789"', ["BE68 0001 2345 6789"]),
        ("BE68 5390 0754 7034", ["BE68 5390 0754 7034"]),
    ], ["BE68 5390 0754 703", "BE68 5390 0754 70341", "BE68-5390-0754-7034", "NL91 ABNA 0417 1643 00",
        "XBE68539007547034", "BE6853900754703", "BE69 5390 0754 7034"])


def test_hard_iccid():
    _check(rre.be.iccid, [
        ("89321022223333444459", ["89321022223333444459"]),
        ("ICCID: 893205123456789016.", ["893205123456789016"]),
        ("carte SIM 8932209876543210981,", ["8932209876543210981"]),
        ("(8932300000000000011)", ["8932300000000000011"]),
        ('SIM-Nummer "89324455667788990012"', ["89324455667788990012"]),
        ("8932010000000000004", ["8932010000000000004"]),
    ], ["89310112345678901232", "89320112345678901", "893201123456789012323", "x89320112345678901232",
        "8932 0112 3456 7890 1232", "8932010000000000005"])


def test_hard_imsi():
    _check(rre.be.imsi, [
        ("206011234567890", ["206011234567890"]),
        ("IMSI: 206101234567890.", ["206101234567890"]),
        ("imsi=206200000000001;", ["206200000000001"]),
        ("(206051122334455)", ["206051122334455"]),
        ("abonné 206069876543210,", ["206069876543210"]),
        ('"206300000012345"', ["206300000012345"]),
    ], ["20601123456789", "2060112345678901", "x206011234567890", "206 01 1234567890", "310150123456789",
        "204011234567890"])


def test_hard_license_plate():
    _check(rre.be.license_plate, [
        ("(7-XYZ-001)", ["7-XYZ-001"]),
        ("nummerplaat 1-AAA-001.", ["1-AAA-001"]),
        ('plaque "2-DEF-456",', ["2-DEF-456"]),
        ("Kennzeichen 9ZZZ999", ["9ZZZ999"]),
        ("ABC-123", ["ABC-123"]),
        ("oude plaat 123-ABC", ["123-ABC"]),
    ], ["ABC123", "PNR ABC123", "0-ABC-123", "1-ABC-1234", "1-ABC-12", "AB-123-CD", "x1-ABC-123", "B-AB 1234"])


def test_hard_mobile_number():
    _check(rre.be.mobile_number, [
        ("0485123456", ["0485123456"]),
        ("+32 (0)477 12 34 56.", ["+32 (0)477 12 34 56"]),
        ("gsm: 0032 456 12 34 56,", ["0032 456 12 34 56"]),
        ("(0499.12.34.56)", ["0499.12.34.56"]),
        ("Handy +32468123456", ["+32468123456"]),
        ("tél. 0455/12.34.56", ["0455/12.34.56"]),
    ], ["0470 12 34 5", "0470 12 34 567", "0470 12 34 56 78", "10032470123456", "+31 6 12345678", "0440 12 34 56",
        "+32 2 234 56 78", "x0470123456"])


def test_hard_mrz_id_card():
    line = "IDBEL591123456<7535<<<<<<<<<<<"
    _check(rre.be.mrz_id_card, [
        (line + "\n8507309M3001019BEL<<<<<<<<<<<6\nPEETERS<<JAN<<<<<<<<<<<<<<<<<", [line]),
        ("MRZ: IDBEL593012345<6354<<<<<<<<<<<.", ["IDBEL593012345<6354<<<<<<<<<<<"]),
        ("(IDBEL600000004<2527<<<<<<<<<<<)", ["IDBEL600000004<2527<<<<<<<<<<<"]),
        ("IDBELB123456781<<<<<<<<<<<<<<<", ["IDBELB123456781<<<<<<<<<<<<<<<"]),  # nine-character number
        ('"I<BEL599087654<3820<<<<<<<<<<<"', ["I<BEL599087654<3820<<<<<<<<<<<"]),
        ("ARBELB123456781<<<<<<<<<<<<<<<", ["ARBELB123456781<<<<<<<<<<<<<<<"]),
    ], ["IDNLD591123456<7535<<<<<<<<<<<", line[:-1], line + "<", line.lower(), "X" + line,
        "IDBEL591123456<7536<<<<<<<<<<<"])


def test_hard_mrz_passport():
    line = "EH123456<0BEL8507309M3001019<<<<<<<<<<<<<<<6"
    _check(rre.be.mrz_passport, [
        ("P<BELPEETERS<<JAN<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" + line, [line]),
        ("(EM654321<7BEL9002018F2812313<<<<<<<<<<<<<<<0)", ["EM654321<7BEL9002018F2812313<<<<<<<<<<<<<<<0"]),
        ("MRZ: EJ000001<8BEL7512319X3106154<<<<<<<<<<<<<<<2.", ["EJ000001<8BEL7512319X3106154<<<<<<<<<<<<<<<2"]),
        ("EP987654<2BEL0507303F270301785073003328<<<96", ["EP987654<2BEL0507303F270301785073003328<<<96"]),
        ('"EK246810<1BEL9306152<2909093<<<<<<<<<<<<<<<2"', ["EK246810<1BEL9306152<2909093<<<<<<<<<<<<<<<2"]),
        ("EA100200<1BEL8201010M3202296<<<<<<<<<<<<<<<0", ["EA100200<1BEL8201010M3202296<<<<<<<<<<<<<<<0"]),
    ], [line.replace("BEL", "NLD"), line.replace("8507309", "8507308"), line.replace("3001019", "3001018"),
        line[:-1], line + "0", line.replace("9M", "9Z")])


def test_hard_msisdn():
    _check(rre.be.msisdn, [
        ("32485123456", ["32485123456"]),
        ("MSISDN=32456123456;", ["32456123456"]),
        ("(32499123456)", ["32499123456"]),
        ("appelant 32460123456, durée", ["32460123456"]),
        ("wa.me/32477123456", ["32477123456"]),
        ('"32468123456"', ["32468123456"]),
    ], ["+32470123456", "3247012345", "324701234567", "31612345678", "32440123456", "0032470123456"])


def test_hard_national_number():
    _check(rre.be.national_number, [
        ("90.02.01-001.30", ["90.02.01-001.30"]),
        ("rijksregisternummer 75123199723.", ["75123199723"]),
        ("(93.06.15-270.14)", ["93.06.15-270.14"]),
        ("NN: 82.00.00-001.72,", ["82.00.00-001.72"]),  # unknown birth date
        ("numéro de registre national 12.03.14-567.91", ["12.03.14-567.91"]),
        ('Nationalregisternummer "60101045590"', ["60101045590"]),
    ], ["85.27.30-033.71",  # a BIS number: its month is raised by 20 or 40
        "85.13.30-033.70", "85.07.32-033.65", "8507300332", "850730033289", "0123.456.749", "85.07.30-033.2"])


def test_hard_notice_number():
    _check(rre.be.notice_number, [
        ("notice n° HA.43.L1.012345/16.", ["notice n° HA.43.L1.012345/16"]),
        ("Notitienummer van het parket AN.55.LB.000123/2026,", ["Notitienummer van het parket AN.55.LB.000123/2026"]),
        ("(n° de notice BR.12.L3.123456/2025)", ["n° de notice BR.12.L3.123456/2025"]),
    ], ["notitienummer: AN.5.LB.000123/2026", "notitienummer AN.55.12.000123/2026",
        "notitienummer GE/D/43/12/1234/1824", "notice AN.55.LB.12/2026", "notitie: 12/03/2024",
        "notitienummer AN.55.LB.000123"])


def test_hard_passport_number():
    _check(rre.be.passport_number, [
        ("EM654321", ["EM654321"]),
        ("paspoortnummer: EJ000001.", ["EJ000001"]),
        ("(EP987654)", ["EP987654"]),
        ("passeport n° EK246810, délivré", ["EK246810"]),
        ('Reisepass "EA100200"', ["EA100200"]),
        ("paspoort EH123456", ["EH123456"]),
    ], ["EH1234567", "eh123456", "E1234567", "EHX123456", "EH 123456", "BE68539007547034"])


def test_hard_phone_number():
    _check(rre.be.phone_number, [
        ("011 23 45 67", ["011 23 45 67"]),
        ("tel. 050 12 34 56.", ["050 12 34 56"]),
        ("(016 12 34 56)", ["016 12 34 56"]),
        ("+32 (0)2 234 56 78", ["+32 (0)2 234 56 78"]),
        ("Telefon 0032 71 12 34 56,", ["0032 71 12 34 56"]),
        ("Tel.: +3287123456", ["+3287123456"]),
        ("gratis 0800 123 10", ["0800 123 10"]),
    ], ["1983 0800 123 10",  # a Luxembourg matricule, not a number after its first group
        "02 123 45 6", "02 234 56 789", "0470 12 34 56 78", "+31 20 123 4567", "12/03/2024",
        "10032 2 234 56 78", "03 123 45 67"])


def test_hard_postal_code_city():
    _check(rre.be.postal_code_city, [
        ("Kerkstraat 12, 2000 Antwerpen.", ["2000 Antwerpen"]),
        ("B-4000 Liège", ["4000 Liège"]),
        ("1000 BRUXELLES", ["1000 BRUXELLES"]),
        ("(7190 Écaussinnes)", ["7190 Écaussinnes"]),
        ("domicilié à 7800 ATH,", ["7800 ATH"]),
        ("wohnhaft in 4700 Eupen", ["4700 Eupen"]),
        ("Kerkstraat 12\n9000 Gent\nBelgië", ["9000 Gent"]),  # the next line is not part of the city
    ], ["1234 AB", "2048 MB", "1234 BCD", "0900 Gent", "12345 Berlin", "9000 gent", "L-1234 Luxembourg", "900 Gent"])


def test_hard_premium_number():
    _check(rre.be.premium_number, [
        ("0903/12.345", ["0903/12.345"]),
        ("bel 0905 12 345.", ["0905 12 345"]),
        ("(0909 12 345)", ["0909 12 345"]),
        ("appelez le 070 23 45 67,", ["070 23 45 67"]),
        ("Hotline 090212345", ["090212345"]),
        ("070.25.25.25", ["070.25.25.25"]),
    ], ["0800 12 345", "0900 12 34", "0900 12 3456", "070 22 33 4", "02 123 45 67", "0470 12 34 56", "x0900 12 345"])


def test_hard_pv_number():
    _check(rre.be.pv_number, [
        ("BR.12.L3.123456/2025", ["BR.12.L3.123456/2025"]),
        ("(GE.43.LR.001234/2023)", ["GE.43.LR.001234/2023"]),
        ("pv nr. AN 55.LB.000123/2026.", ["AN 55.LB.000123/2026"]),
        ("PV LE.55.L1.0123/24,", ["LE.55.L1.0123/24"]),
    ], ["AN.5.LB.000123/2026", "AN.55.12.000123/2026", "AN.55.LB.12/2026", "file 23/1234/A", "an.55.lb.000123/2026",
        "AN.55.LB.000123", "AN.55.LB.00012345/2026", "AN.55.LB.000123/1826"])


def test_hard_street_address_fr():
    _check(rre.be.street_address_fr, [
        ("Chaussée de Wavre 1234", ["Chaussée de Wavre 1234"]),
        ("domicilié Boulevard Anspach 1, 1000 Bruxelles", ["Boulevard Anspach 1"]),
        ("(Place Flagey 7A)", ["Place Flagey 7A"]),
        ("Chemin du Moulin 3 boîte 4.", ["Chemin du Moulin 3 boîte 4"]),
        ("Av. de Tervueren 12,", ["Av. de Tervueren 12"]),
        ("Bd. du Roi Albert II 30", ["Bd. du Roi Albert II 30"]),
        ("Rue de l’Église 5", ["Rue de l’Église 5"]),
        ("Square Ambiorix 32 bt. 5", ["Square Ambiorix 32 bt. 5"]),
    ], ["Rue de la Loi", "Ruelle 12", "Placement 12", "Kerkstraat 12", "Rue16", "Avenue Louise 12345", "Place 12"])
    start = time.perf_counter()
    rre.be.street_address_fr('Rue ' * 25000)  # the street name used to run on to the end of the text from every Rue
    assert time.perf_counter() - start < 1


def test_hard_street_address_nl():
    _check(rre.be.street_address_nl, [
        ("Brusselsesteenweg 123", ["Brusselsesteenweg 123"]),
        ("woont Frankrijklei 45, 2000 Antwerpen", ["Frankrijklei 45"]),
        ("(Korenmarkt 7A)", ["Korenmarkt 7A"]),
        ("Vaartdreef 2 b. 4.", ["Vaartdreef 2 b. 4"]),
        ("Scheldekaai 9,", ["Scheldekaai 9"]),
        ("Antwerpsebaan 300", ["Antwerpsebaan 300"]),
        ("Dorpsweg 3", ["Dorpsweg 3"]),
    ], ["Kerkstraat", "kerkstraat 12", "Kerkstraten 12", "Kerkstraat12", "Kerkstraat 12345", "Rue de la Loi 16",
        "Straat 12"])


def test_hard_structured_communication():
    _check(rre.be.structured_communication, [
        ("+++090/9337/55493+++", ["+++090/9337/55493+++"]),
        ("mededeling: +++000/0000/00101+++.", ["+++000/0000/00101+++"]),
        ("(***555/5555/55559***)", ["***555/5555/55559***"]),
        ('communication "+++101/0101/01046+++",', ["+++101/0101/01046+++"]),
        ("Verwendungszweck +++987/6543/21009+++", ["+++987/6543/21009+++"]),
        ("***123/4567/89002***", ["***123/4567/89002***"]),
    ], ["++123/4567/89002++", "+++1234/567/89002+++", "+++123/4567/8900+++", "+*+123/4567/89002+*+",
        "123/4567/89002", "+++123-4567-89002+++"])


def test_hard_time():
    _check(rre.be.time, [
        ("00:00", ["00:00"]),
        ("om 7u30.", ["7u30"]),
        ("(12h00)", ["12h00"]),
        ("à 14H30,", ["14H30"]),
        ("um 18:05:30 Uhr", ["18:05:30"]),
        ("2024-03-12 14:30:00.123", ["14:30:00"]),
        ("Tijd:14:30", ["14:30"]),
    ], ["14u60", "14:3", "25:00", "1430", "14 u 30", "ISO 9001:2015", "16:9",
        "00:11:22:33:44:55", "a4:bc:12:34:ef:01", "fe80::1:20"])  # MAC and IPv6 addresses


def test_hard_vat_number():
    _check(rre.be.vat_number, [
        ("BE 0876.543.270", ["BE 0876.543.270"]),
        ("btw-nr. BE0200123470.", ["BE0200123470"]),
        ("TVA BE 1000.000.021,", ["BE 1000.000.021"]),
        ("(BE0999555504)", ["BE0999555504"]),
        ('USt-IdNr. "BE0555.555.523"', ["BE0555.555.523"]),
        ("btw BE0123.456.749", ["BE0123.456.749"]),
    ], ["BE 2123456791", "BE012345674", "BE01234567490", "NL0123456749", "XBE0123456749", "BE-0123456749",
        "BE 0123456748"])


def test_overlap_postal_code_city():
    # amounts and Spanish plates (consonants only) are no postcode and town
    for text in ("1500 Lei", "2500 RON", "1000 USD", "750 EUR", "9876 ZYX"):
        assert rre.be.postal_code_city(text) == []
    assert rre.be.postal_code_city("1000 Bruxelles, 3000 LEUVEN") == ["1000 Bruxelles", "3000 LEUVEN"]


def test_hard_quay():
    _check(rre.be.quay, [
        ("Kaai 913", ["Kaai 913"]),
        ("container gelost aan kaai 1700 Deurganckdok", ["kaai 1700"]),
        ("PSA Quay 869,", ["Quay 869"]),
        ("quai n° 1742", ["quai n° 1742"]),
        ("kaainummer 730", ["kaainummer 730"]),
        ("berth 1700 and ligplaats 913", ["berth 1700", "ligplaats 913"]),
        ("KAAI 913.", ["KAAI 913"]),
    ], ["Rijnkaai 100", "Quai de la Batte 10", "kaai 0", "kaai 12345", "Kaaien 5", "kaai 913a", "kaai 0913"])
