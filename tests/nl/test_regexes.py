from regular_regexes import rre

# 999999990 is the BSN on the Dutch specimen documents, 9999xxxxx numbers are test BSNs; SPECI2014 is the
# specimen document number; KvK 68750110 and 69599084 are KvK's fictitious test companies. The Netherlands
# reserves no phone numbers for fiction: the phone tests use libphonenumber's example numbers.


def test_bsn():
    assert rre.nl.bsn("BSN: 999999990, sofinummer 999 900 006 en 9999.99.990") == [
        "BSN: 999999990", "sofinummer 999 900 006", "9999.99.990"]
    assert rre.nl.bsn("klantnummer 999999990") == []  # no keyword and not written 1234.56.789
    assert rre.nl.bsn("BSN: 999999991") == []


def test_rsin():
    assert rre.nl.rsin("RSIN: 9999.00.006") == ["RSIN: 9999.00.006"]
    assert rre.nl.rsin("999900006") == []
    assert rre.nl.rsin("RSIN: 9999.00.007") == []


def test_kvk_number():
    assert rre.nl.kvk_number("KvK-nummer: 68750110, ingeschreven bij de Kamer van Koophandel onder nummer 69599084") == [
        "KvK-nummer: 68750110", "Kamer van Koophandel onder nummer 69599084"]
    assert rre.nl.kvk_number("ordernummer 68750110 en KvK 687501101") == []


def test_vat_number():
    # B01 after an RSIN/BSN (11-proef), or the btw-id of a sole proprietor (mod 97)
    assert rre.nl.vat_number("btw NL999999990B01 en NL 9999.99.999.B.67") == ["NL999999990B01", "NL 9999.99.999.B.67"]
    assert rre.nl.vat_number("NL999999990B00") == []
    assert rre.nl.vat_number("NL999999991B01 en NL999999999B68") == []


def test_iban():
    assert rre.nl.iban("op NL91 ABNA 0417 1643 00 of NL91ABNA0417164300") == [
        "NL91 ABNA 0417 1643 00", "NL91ABNA0417164300"]
    assert rre.nl.iban("BE68 5390 0754 7034") == []
    assert rre.nl.iban("NL91ABNA0417164301") == []


def test_bic():
    assert rre.nl.bic("BIC ABNANL2A of RABONL2UXXX") == ["ABNANL2A", "RABONL2UXXX"]
    assert rre.nl.bic("GEBABEBB") == []


def test_document_number():
    assert rre.nl.document_number("paspoortnummer: SPECI2014, ID-kaart nr. SPECI2021") == ["SPECI2014", "SPECI2021"]
    # the letter O is never used, the last character is a digit
    assert rre.nl.document_number("paspoort XR1O01R58 en SPECI201A") == []


def test_mrz_id_card():
    line = "I<NLDSPECI20142999999990<<<<<<"
    assert rre.nl.mrz_id_card(f"mrz {line}") == [line]
    assert rre.nl.mrz_id_card("I<BELSPECI20142999999990<<<<<<") == []
    assert rre.nl.mrz_id_card(line.replace("20142", "20143")) == []


def test_mrz_passport():
    line = "SPECI20142NLD6503101F3103094999999990<<<<<82"
    assert rre.nl.mrz_passport(line) == [line]
    assert rre.nl.mrz_passport(line.replace("NLD", "BEL")) == []
    assert rre.nl.mrz_passport(line.replace("6503101", "6503111")) == []


def test_phone_number():
    assert rre.nl.phone_number("bel 010 123 4567, +31 (0)10-1234567 of 06 12 34 56 78") == [
        "010 123 4567", "+31 (0)10-1234567", "06 12 34 56 78"]
    # Belgian number, an IBAN's account number, a date with a time
    assert rre.nl.phone_number("02 123 45 67, NL91 ABNA 0417 1643 00, 01-02-2023 12:30") == []


def test_mobile_number():
    assert rre.nl.mobile_number("bel 06-12345678 of +31 (0)6 1234 5678") == ["06-12345678", "+31 (0)6 1234 5678"]
    assert rre.nl.mobile_number("vast 010 123 4567, op 06-12-2023 12:30") == []


def test_msisdn():
    assert rre.nl.msisdn("msisdn 31612345678") == ["31612345678"]
    assert rre.nl.msisdn("31101234567") == []


def test_premium_number():
    assert rre.nl.premium_number("bel 0906 1234 of 0900-123 4567") == ["0906 1234", "0900-123 4567"]
    assert rre.nl.premium_number("gratis 0800-1234") == []


def test_imsi():
    assert rre.nl.imsi("imsi 204041234567890") == ["204041234567890"]
    assert rre.nl.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.nl.iccid("sim 89310412345678901230") == ["89310412345678901230"]
    assert rre.nl.iccid("89320112345678901232") == []  # Belgian
    assert rre.nl.iccid("sim 89310412345678901231") == []


def test_license_plate():
    assert rre.nl.license_plate("auto's AB-12-34, XB-12-TZ, 12-GBB-3, G-123-BB en GBB12B") == [
        "AB-12-34", "XB-12-TZ", "12-GBB-3", "G-123-BB", "GBB12B"]
    # flight number, postal code, colour, digits only, a longer code
    assert rre.nl.license_plate("vlucht KL1234, 1234BD, #33FF66, 12-34-56, AB-12-CD-34") == []


def test_postal_code():
    assert rre.nl.postal_code("1234 AB Amsterdam en 9999ZZ") == ["1234 AB", "9999ZZ"]
    assert rre.nl.postal_code("1234 SS, 0123 AB, 2048 MB") == []


def test_street_address():
    assert rre.nl.street_address("woont Dorpsstraat 12A, Molenkade 3-II of Stationsweg 7 hs") == [
        "Dorpsstraat 12A", "Molenkade 3-II", "Stationsweg 7 hs"]
    assert rre.nl.street_address("Kerkstraat 12 in Amsterdam") == ["Kerkstraat 12"]
    assert rre.nl.street_address("in de straat 12 keer") == []


def test_company_name():
    assert rre.nl.company_name("tussen Bakkerij van Dam B.V. en Pietersen & Zonen V.O.F.") == [
        "Bakkerij van Dam B.V.", "Pietersen & Zonen V.O.F."]
    assert rre.nl.company_name("gift aan Stichting Vrienden van Het Park. Daarna") == ["Stichting Vrienden van Het Park"]
    assert rre.nl.company_name("Mijn CV en de c.v.-ketel") == []


def test_ecli():
    assert rre.nl.ecli("zie ECLI:NL:HR:2020:1234.") == ["ECLI:NL:HR:2020:1234"]
    assert rre.nl.ecli("ECLI:BE:CASS:2020:ARR.20200115.1") == []


def test_aircraft_registration():
    assert rre.nl.aircraft_registration("PH-XYZ, microlight PH-1A1 en zweefvliegtuig PH-1234") == [
        "PH-XYZ", "PH-1A1", "PH-1234"]
    assert rre.nl.aircraft_registration("OO-ABC en PH-ABCD") == []


def test_tikkie_link():
    assert rre.nl.tikkie_link("betaal via https://tikkie.me/pay/AbCd1234EfGh5678 aub") == [
        "https://tikkie.me/pay/AbCd1234EfGh5678"]
    assert rre.nl.tikkie_link("tlkkie.me/pay/AbCd1234") == []
