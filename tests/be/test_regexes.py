from rre import rre


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
    assert rre.be.phone_number("call +32 470 12 34 56 or 02/123.45.67") == ["+32 470 12 34 56", "02/123.45.67"]


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
    assert rre.be.premium_number("bel 0900 12 345 of 070 12 34 56") == ["0900 12 345", "070 12 34 56"]


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
