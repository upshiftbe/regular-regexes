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


def test_postnl_tracking_number():
    # examples from PostNL's barcode API documentation
    text = "PostNL 3SDEVC903942795 en jouw.postnl.nl/track-and-trace/3SABCD3427702-NL-1234AB"
    assert rre.nl.postnl_tracking_number(text) == ["3SDEVC903942795", "3SABCD3427702"]
    # 11 and 14 characters, five letters, lower case
    assert rre.nl.postnl_tracking_number("3SAB1234567 3SBCC000123456 3SABCDE123456 3sabcd3427702") == []


# Hardened tests: every regex gets at least six written forms that match and six near misses that don't. The
# registrations, BICs, document numbers and phone numbers below are made up in the right shape and ranges.


def test_hard_aircraft_registration():
    assert rre.nl.aircraft_registration("PH-QZX") == ["PH-QZX"]
    assert rre.nl.aircraft_registration("drone (PH-1AB)") == ["PH-1AB"]
    assert rre.nl.aircraft_registration("zweefvliegtuig 'PH-412'.") == ["PH-412"]
    assert rre.nl.aircraft_registration("het toestel PH-ZZQ landde om 14.30 uur") == ["PH-ZZQ"]
    assert rre.nl.aircraft_registration("registration:PH-9Z9") == ["PH-9Z9"]
    assert rre.nl.aircraft_registration("ULV PH-2B3, glider PH-1801") == ["PH-2B3", "PH-1801"]
    assert rre.nl.aircraft_registration("PH-AB") == []  # too short
    assert rre.nl.aircraft_registration("PH-QZXA") == []  # too long
    assert rre.nl.aircraft_registration("PH-0123") == []  # a glider number doesn't start with 0
    assert rre.nl.aircraft_registration("PH-12345") == []
    assert rre.nl.aircraft_registration("APH-QZX") == []  # inside a longer word
    assert rre.nl.aircraft_registration("ph-qzx") == []
    assert rre.nl.aircraft_registration("OO-QZX en D-EQZX") == []  # Belgian and German


def test_hard_bic():
    assert rre.nl.bic("(BIC: ABCDNL2A)") == ["ABCDNL2A"]
    assert rre.nl.bic("bic=QWERNL3B.") == ["QWERNL3B"]
    assert rre.nl.bic("SWIFT ZYXWNL21XXX") == ["ZYXWNL21XXX"]
    assert rre.nl.bic("ABCDNL2A123 is het filiaal") == ["ABCDNL2A123"]
    assert rre.nl.bic("over te maken naar 'QWERNL2U'") == ["QWERNL2U"]
    assert rre.nl.bic("BIC-code: ABCDNL22") == ["ABCDNL22"]
    assert rre.nl.bic("ABCDNL2") == []  # seven characters
    assert rre.nl.bic("ABCDNL2AX") == []  # nine
    assert rre.nl.bic("ABCDNL2AXXXX") == []  # twelve
    assert rre.nl.bic("AB1DNL2A") == []  # a digit in the bank code
    assert rre.nl.bic("ABCDBE2A") == []  # Belgian
    assert rre.nl.bic("XABCDNL2A") == []
    assert rre.nl.bic("NL91ABNA0417164300") == []  # an IBAN


def test_hard_bsn():
    assert rre.nl.bsn("burgerservicenummer 999-90-0018") == ["burgerservicenummer 999-90-0018"]
    assert rre.nl.bsn("(BSN 999900031)") == ["BSN 999900031"]
    assert rre.nl.bsn("Persoonsnummer: 999.900.043") == ["Persoonsnummer: 999.900.043"]
    assert rre.nl.bsn("SoFi-nr 999900055") == ["SoFi-nr 999900055"]
    assert rre.nl.bsn("Bsn:999900067.") == ["Bsn:999900067"]
    assert rre.nl.bsn("9999.00.080 staat op de pas") == ["9999.00.080"]
    assert rre.nl.bsn("BSN: 99999999") == []  # eight digits
    assert rre.nl.bsn("BSN: 9999999900") == []  # ten digits
    assert rre.nl.bsn("9999.99.991") == []  # 11-proef fails
    assert rre.nl.bsn("versie 1.9999.99.990") == []  # part of a longer dotted number
    assert rre.nl.bsn("9999.99.990.1") == []
    assert rre.nl.bsn("BSN 000000000") == []
    assert rre.nl.bsn("BSN-loket: bel 020 123 4567") == []  # a phone number


def test_hard_company_name():
    assert rre.nl.company_name("De Vries Transport NV") == ["De Vries Transport NV"]
    assert rre.nl.company_name("aannemer Bouwbedrijf A.B. Jansen C.V.") == ["Bouwbedrijf A.B. Jansen C.V."]
    assert rre.nl.company_name("Coöperatie Zuivel Noord U.A. levert") == ["Coöperatie Zuivel Noord U.A."]
    assert rre.nl.company_name('"Van der Berg & Zn. B.V."') == ["Van der Berg & Zn. B.V."]
    assert rre.nl.company_name("factuur van Gebr. Jansen B.V.") == ["Gebr. Jansen B.V."]
    assert rre.nl.company_name("(Stichting Het Open Huis)") == ["Stichting Het Open Huis"]
    assert rre.nl.company_name("Stichting voor de Kunst en Cultuur") == ["Stichting voor de Kunst en Cultuur"]
    assert rre.nl.company_name("café Het Wapen BV, JANSEN HOLDING BV.") == ["Het Wapen BV", "JANSEN HOLDING BV"]
    # an article or possessive alone is no name
    assert rre.nl.company_name("Mijn BV is opgericht") == []
    assert rre.nl.company_name("De BV heeft winst gemaakt") == []
    assert rre.nl.company_name("Onze B.V. groeit") == []
    assert rre.nl.company_name("Een BV oprichten") == []
    assert rre.nl.company_name("Jansen BVBA") == []  # the old Belgian form
    assert rre.nl.company_name("Jansen B.V.B.A.") == []
    assert rre.nl.company_name("Stichting heeft") == []


def test_hard_document_number():
    assert rre.nl.document_number("XR1001R58") == ["XR1001R58"]
    assert rre.nl.document_number("(BH3K72L94)") == ["BH3K72L94"]
    assert rre.nl.document_number('nummer "NXP2R1C34".') == ["NXP2R1C34"]
    assert rre.nl.document_number("documentnummer:SPECI2014") == ["SPECI2014"]
    assert rre.nl.document_number("SPECI2021 is het nummer") == ["SPECI2021"]
    assert rre.nl.document_number("nr. PP12AB345, geldig tot 2033") == ["PP12AB345"]
    assert rre.nl.document_number("SPECI201") == []  # eight characters
    assert rre.nl.document_number("SPECI20145") == []  # ten
    assert rre.nl.document_number("1PECI2014") == []  # starts with a digit
    assert rre.nl.document_number("OPECI2014") == []  # the letter O
    assert rre.nl.document_number("SPECI-2014") == []
    assert rre.nl.document_number("speci2014") == []


def test_hard_ecli():
    assert rre.nl.ecli("ECLI:NL:RBAMS:2021:1234") == ["ECLI:NL:RBAMS:2021:1234"]
    assert rre.nl.ecli("(ECLI:NL:GHARL:2019:5678)") == ["ECLI:NL:GHARL:2019:5678"]
    assert rre.nl.ecli("arrest ECLI:NL:HR:2012:BV1234, r.o. 3.2") == ["ECLI:NL:HR:2012:BV1234"]
    assert rre.nl.ecli("conclusie ECLI:NL:PHR:2020:123.") == ["ECLI:NL:PHR:2020:123"]
    assert rre.nl.ecli("ECLI:NL:CRVB:2018:12.AB") == ["ECLI:NL:CRVB:2018:12.AB"]
    assert rre.nl.ecli("'ECLI:NL:RVS:2022:1'") == ["ECLI:NL:RVS:2022:1"]
    assert rre.nl.ecli("ECLI:NL:HR:20:1234") == []  # two-digit year
    assert rre.nl.ecli("ECLI:NL:HR:2020:") == []  # no number
    assert rre.nl.ecli("ECLI:NL::2020:1234") == []  # no court
    assert rre.nl.ecli("XECLI:NL:HR:2020:1234") == []
    assert rre.nl.ecli("ECLI:NL:hr:2020:1234") == []
    assert rre.nl.ecli("ECLI:DE:BGH:2020:010120UIZR12.19.0") == []


def test_hard_iban():
    assert rre.nl.iban("IBAN: NL20 INGB 0001 2345 67.") == ["NL20 INGB 0001 2345 67"]
    assert rre.nl.iban("(NL44RABO0123456789)") == ["NL44RABO0123456789"]
    assert rre.nl.iban("NL02ABNA0123456789") == ["NL02ABNA0123456789"]
    assert rre.nl.iban("NL63TRIO0212345678 t.n.v. J. Jansen") == ["NL63TRIO0212345678"]
    assert rre.nl.iban("rekening:NL68KNAB0123456789") == ["NL68KNAB0123456789"]
    assert rre.nl.iban("'NL20 INGB 0001234567'") == ["NL20 INGB 0001234567"]
    assert rre.nl.iban("NL91ABNA041716430") == []  # one digit short
    assert rre.nl.iban("NL91ABNA04171643000") == []  # one digit too many
    assert rre.nl.iban("XNL91ABNA0417164300") == []
    assert rre.nl.iban("NL91 ABNA 0417 1643 0") == []
    assert rre.nl.iban("NL91-ABNA-0417-1643-00") == []
    assert rre.nl.iban("NL20INGB0001234568") == []  # check digits fail


def test_hard_iccid():
    assert rre.nl.iccid("iccid 893102000012345679") == ["893102000012345679"]  # 18 digits
    assert rre.nl.iccid("ICCID: 8931160000123456786.") == ["8931160000123456786"]  # 19
    assert rre.nl.iccid("(89310812345678901236)") == ["89310812345678901236"]  # 20
    assert rre.nl.iccid("893104111222333443") == ["893104111222333443"]
    assert rre.nl.iccid("simkaart=89310412345678901230;") == ["89310412345678901230"]
    assert rre.nl.iccid("'8931160000123456786'") == ["8931160000123456786"]
    assert rre.nl.iccid("89310200001234567") == []  # 17 digits
    assert rre.nl.iccid("893108123456789012361") == []  # 21
    assert rre.nl.iccid("8931 0412 3456 7890 1230") == []
    assert rre.nl.iccid("x89310412345678901230") == []
    assert rre.nl.iccid("893102000012345670") == []  # Luhn fails
    assert rre.nl.iccid("8944102000012345678") == []  # British


def test_hard_imsi():
    assert rre.nl.imsi("IMSI: 204081234567890.") == ["204081234567890"]
    assert rre.nl.imsi("(204161234567890)") == ["204161234567890"]
    assert rre.nl.imsi("imsi=204201234567890;") == ["204201234567890"]
    assert rre.nl.imsi("204041234567890 is de imsi") == ["204041234567890"]
    assert rre.nl.imsi("'204691234567890'") == ["204691234567890"]
    assert rre.nl.imsi("IMSI 204 08 1234567890") == []  # not written with spaces
    assert rre.nl.imsi("20404123456789") == []  # 14 digits
    assert rre.nl.imsi("2040412345678901") == []  # 16
    assert rre.nl.imsi("A204041234567890") == []
    assert rre.nl.imsi("0204041234567890") == []
    assert rre.nl.imsi("204-04-1234567890") == []
    assert rre.nl.imsi("310260123456789") == []  # American


def test_hard_kvk_number():
    assert rre.nl.kvk_number("KVK 68750110") == ["KVK 68750110"]
    assert rre.nl.kvk_number("(kvk nr. 69599084)") == ["kvk nr. 69599084"]
    assert rre.nl.kvk_number("Handelsregister: 68750110.") == ["Handelsregister: 68750110"]
    assert rre.nl.kvk_number("Chamber of Commerce no. 69599084") == ["Chamber of Commerce no. 69599084"]
    assert rre.nl.kvk_number("CoC 68750110") == ["CoC 68750110"]
    assert rre.nl.kvk_number("K.v.K. 69599084") == ["K.v.K. 69599084"]
    assert rre.nl.kvk_number("KvK 6875011") == []  # seven digits
    assert rre.nl.kvk_number("KvK 68750110123") == []  # eleven
    assert rre.nl.kvk_number("KvK: bel 0201234567") == []  # a phone number
    assert rre.nl.kvk_number("KvK, Postbus 48, 3000 AA Rotterdam") == []
    assert rre.nl.kvk_number("Kamer van Koophandel sinds 12-03-2024") == []
    assert rre.nl.kvk_number("Kvkx 68750110") == []


def test_hard_license_plate():
    assert rre.nl.license_plate("1-KBB-23") == ["1-KBB-23"]
    assert rre.nl.license_plate("bestelbus GB-123-X") == ["GB-123-X"]
    assert rre.nl.license_plate("kenteken '99-ZZ-99'.") == ["99-ZZ-99"]
    assert rre.nl.license_plate("(12-GBB-3)") == ["12-GBB-3"]
    assert rre.nl.license_plate("1KBB23 geparkeerd") == ["1KBB23"]
    assert rre.nl.license_plate("ZZ-99-ZZ en B-12-XYZ") == ["ZZ-99-ZZ", "B-12-XYZ"]
    assert rre.nl.license_plate("AB-12-3") == []  # too short
    assert rre.nl.license_plate("AB-12-345") == []  # too long
    assert rre.nl.license_plate("CD-12-34") == []  # no C
    assert rre.nl.license_plate("QB-12-34") == []  # no Q
    assert rre.nl.license_plate("ab-12-cd") == []
    assert rre.nl.license_plate("AB-CD-EF") == []  # letters only
    # the three-letter sidecodes (since 1999) have no vowels: product codes and the like
    assert rre.nl.license_plate("ISO-12-A") == []
    assert rre.nl.license_plate("EUR-12-B") == []


def test_hard_mobile_number():
    assert rre.nl.mobile_number("0612345678") == ["0612345678"]
    assert rre.nl.mobile_number("+31612345678.") == ["+31612345678"]
    assert rre.nl.mobile_number("0031 6 87654321") == ["0031 6 87654321"]
    assert rre.nl.mobile_number("(+31-6-41234567)") == ["+31-6-41234567"]
    assert rre.nl.mobile_number("Mijn nummer is 06 51 23 45 67!") == ["06 51 23 45 67"]
    assert rre.nl.mobile_number("tel. (06) 12345678") == ["(06) 12345678"]
    assert rre.nl.mobile_number("(+31) 6 1234 5678") == ["(+31) 6 1234 5678"]
    assert rre.nl.mobile_number("06-1234567") == []  # one digit short
    assert rre.nl.mobile_number("06-123456789") == []  # one digit too many
    assert rre.nl.mobile_number("0661234567") == []  # 066 is a pager
    assert rre.nl.mobile_number("NL91 ABNA 0612 3456 78") == []  # an IBAN's account number
    assert rre.nl.mobile_number("12 0612345678") == []
    assert rre.nl.mobile_number("+32 6 12345678") == []  # Belgian prefix
    assert rre.nl.mobile_number("06123456789") == []


def test_hard_mrz_id_card():
    assert rre.nl.mrz_id_card("I<NLDXR1001R586999999990<<<<<<") == ["I<NLDXR1001R586999999990<<<<<<"]
    assert rre.nl.mrz_id_card("MRZ: IDNLDBH3K72L942999900018<<<<<<") == ["IDNLDBH3K72L942999900018<<<<<<"]
    assert rre.nl.mrz_id_card("I<NLDSPECI20212<<<<<<<<<<<<<<<\n6503101F3103094NLD<<<<<<<<<<<0") == [
        "I<NLDSPECI20212<<<<<<<<<<<<<<<"]
    assert rre.nl.mrz_id_card("'IRNLDNXP2R1C348<<<<<<<<<<<<<<<'") == ["IRNLDNXP2R1C348<<<<<<<<<<<<<<<"]
    assert rre.nl.mrz_id_card("zone: I<NLDSPECI20142999999990<<<<<<.") == ["I<NLDSPECI20142999999990<<<<<<"]
    assert rre.nl.mrz_id_card("IDNLDPP12AB3454<<<<<<<<<<<<<<<") == ["IDNLDPP12AB3454<<<<<<<<<<<<<<<"]
    assert rre.nl.mrz_id_card("I<NLDXR1001R587999999990<<<<<<") == []  # check digit
    assert rre.nl.mrz_id_card("I<DEUXR1001R586999999990<<<<<<") == []  # German
    assert rre.nl.mrz_id_card("I<NLDXR1001R586999999990<<<<<") == []  # 29 characters
    assert rre.nl.mrz_id_card("I<NLDXR1001R586999999990<<<<<<<") == []  # 31
    assert rre.nl.mrz_id_card("P<NLDXR1001R586999999990<<<<<<") == []  # a passport's type
    assert rre.nl.mrz_id_card("i<nldxr1001r586999999990<<<<<<") == []


def test_hard_mrz_passport():
    lines = [
        "NXP2R1C348NLD8501019M3201015999900018<<<<<32",
        "BH3K72L942NLD0112318<2906151<<<<<<<<<<<<<<<8",
        "XR1001R586NLD7707076X2707071999900031<<<<<28",
        "PP12AB3454NLD9211306F3302288<<<<<<<<<<<<<<<4",
    ]
    assert rre.nl.mrz_passport(lines[0]) == [lines[0]]
    assert rre.nl.mrz_passport(f"MRZ: {lines[1]}.") == [lines[1]]
    assert rre.nl.mrz_passport(f"'{lines[2]}'") == [lines[2]]
    assert rre.nl.mrz_passport("P<NLDDE<BRUIJN<<WILLEKE<LISELOTTE<<<<<<<<<<<\n" + lines[3]) == [lines[3]]
    assert rre.nl.mrz_passport("\n".join(lines[:2])) == lines[:2]
    assert rre.nl.mrz_passport(lines[3] + "\n") == [lines[3]]
    assert rre.nl.mrz_passport(lines[0].replace("8NLD", "9NLD")) == []  # document number check digit
    assert rre.nl.mrz_passport(lines[0].replace("8501019", "8501018")) == []  # birth date check digit
    assert rre.nl.mrz_passport(lines[0].replace("3201015", "3201016")) == []  # expiry date check digit
    assert rre.nl.mrz_passport(lines[1].replace("NLD", "BEL")) == []
    assert rre.nl.mrz_passport(lines[2][:-1]) == []  # 43 characters
    assert rre.nl.mrz_passport(lines[2] + "<") == []  # 45
    assert rre.nl.mrz_passport(lines[3].replace("6F", "6Z")) == []  # no such sex


def test_hard_msisdn():
    assert rre.nl.msisdn("MSISDN: 31687654321.") == ["31687654321"]
    assert rre.nl.msisdn("(31641234567)") == ["31641234567"]
    assert rre.nl.msisdn("msisdn=31651234567;") == ["31651234567"]
    assert rre.nl.msisdn("31681234567,31612345678") == ["31681234567", "31612345678"]
    assert rre.nl.msisdn("'31620000000'") == ["31620000000"]
    assert rre.nl.msisdn("a_party 31637654321 b_party") == ["31637654321"]
    assert rre.nl.msisdn("3161234567") == []  # ten digits
    assert rre.nl.msisdn("316123456789") == []  # twelve
    assert rre.nl.msisdn("31661234567") == []  # a pager
    assert rre.nl.msisdn("031612345678") == []
    assert rre.nl.msisdn("32470123456") == []  # Belgian
    assert rre.nl.msisdn("x31612345678") == []
    assert rre.nl.msisdn("+31612345678") == []  # international format: mobile_number finds it


def test_hard_phone_number():
    assert rre.nl.phone_number("020-1234567") == ["020-1234567"]
    assert rre.nl.phone_number("0031 20 123 4567") == ["0031 20 123 4567"]
    assert rre.nl.phone_number("+31 70 123 4567") == ["+31 70 123 4567"]
    assert rre.nl.phone_number("0591 123456") == ["0591 123456"]
    # the area code in brackets
    assert rre.nl.phone_number("Tel. (010) 123 45 67.") == ["(010) 123 45 67"]
    assert rre.nl.phone_number("(0591) 123456") == ["(0591) 123456"]
    assert rre.nl.phone_number("(+31) 20 123 4567") == ["(+31) 20 123 4567"]
    assert rre.nl.phone_number("Tel.: 043-8765432.") == ["043-8765432"]
    assert rre.nl.phone_number("0471234567") == []  # no area code 047
    assert rre.nl.phone_number("020-123456") == []  # one digit short
    assert rre.nl.phone_number("020-12345678") == []  # one too many
    assert rre.nl.phone_number("(010) 123456") == []
    assert rre.nl.phone_number("+32 2 123 45 67") == []  # Belgian
    assert rre.nl.phone_number("1.020.123.4567") == []
    assert rre.nl.phone_number("12-02-2023 12:30:45") == []
    assert rre.nl.phone_number("(0800) 1234567") == []  # freephone


def test_hard_postal_code():
    assert rre.nl.postal_code("(3511 LX)") == ["3511 LX"]
    assert rre.nl.postal_code("postcode: 2511CV,") == ["2511CV"]
    assert rre.nl.postal_code("Dorpsstraat 1, 9711 LM Groningen") == ["9711 LM"]
    assert rre.nl.postal_code("1011AB") == ["1011AB"]
    assert rre.nl.postal_code("'6211 XZ'") == ["6211 XZ"]
    assert rre.nl.postal_code("verhuisd naar 4811 ZR.") == ["4811 ZR"]
    assert rre.nl.postal_code("12345 AB") == []
    assert rre.nl.postal_code("123 AB") == []
    assert rre.nl.postal_code("1234 ABC") == []
    assert rre.nl.postal_code("1234 A") == []
    assert rre.nl.postal_code("1000 KB") == []  # a size
    assert rre.nl.postal_code("1234 SD") == []  # SA, SD and SS are not used
    assert rre.nl.postal_code("in 2024 EU-breed") == []  # a year in front of a compound
    assert rre.nl.postal_code("1234-AB") == []


def test_hard_postnl_tracking_number():
    assert rre.nl.postnl_tracking_number("3SXYZ1234567890") == ["3SXYZ1234567890"]
    assert rre.nl.postnl_tracking_number("(3SAB123456789)") == ["3SAB123456789"]
    assert rre.nl.postnl_tracking_number("barcode: 3SKAB0123456789.") == ["3SKAB0123456789"]
    assert rre.nl.postnl_tracking_number("3SA1234567890 is onderweg") == ["3SA1234567890"]
    assert rre.nl.postnl_tracking_number("'3SABCD1234567'") == ["3SABCD1234567"]
    assert rre.nl.postnl_tracking_number("t&t=3SQWE1234567890") == ["3SQWE1234567890"]
    assert rre.nl.postnl_tracking_number("3SA12345678901") == []  # 14 characters
    assert rre.nl.postnl_tracking_number("3SABCD34277021") == []
    assert rre.nl.postnl_tracking_number("33SABCD3427702") == []
    assert rre.nl.postnl_tracking_number("3SABCD342770A") == []  # ends in a letter
    assert rre.nl.postnl_tracking_number("3S1234567890123") == []  # no customer code
    assert rre.nl.postnl_tracking_number("RR123456785NL") == []  # a UPU S10 number
    assert rre.nl.postnl_tracking_number("3S-ABCD3427702") == []


def test_hard_premium_number():
    assert rre.nl.premium_number("0909 1234") == ["0909 1234"]
    assert rre.nl.premium_number("09001234567") == ["09001234567"]
    assert rre.nl.premium_number("(0900-1234)") == ["0900-1234"]
    assert rre.nl.premium_number("Bel 0906-123 4567.") == ["0906-123 4567"]
    assert rre.nl.premium_number("0909-8790123") == ["0909-8790123"]
    assert rre.nl.premium_number("'0900 123 45 67'") == ["0900 123 45 67"]
    assert rre.nl.premium_number("0900-123") == []  # too short
    assert rre.nl.premium_number("0900-12345") == []  # neither four nor seven digits
    assert rre.nl.premium_number("0900-123456789") == []
    assert rre.nl.premium_number("0901 1234") == []  # no such range
    assert rre.nl.premium_number("12 0900 1234") == []
    assert rre.nl.premium_number("0800 1234567") == []  # freephone
    assert rre.nl.premium_number("0900.1234") == []


def test_hard_rsin():
    assert rre.nl.rsin("rsin 999900006") == ["rsin 999900006"]
    assert rre.nl.rsin("RSIN-nummer 810000003") == ["RSIN-nummer 810000003"]
    assert rre.nl.rsin("RSIN/fiscaal nummer: 001000007.") == ["RSIN/fiscaal nummer: 001000007"]
    assert rre.nl.rsin("(Rsin 810 000 015)") == ["Rsin 810 000 015"]
    assert rre.nl.rsin("RSIN: 8100.00.027") == ["RSIN: 8100.00.027"]
    assert rre.nl.rsin("rsin=001000019;") == ["rsin=001000019"]
    assert rre.nl.rsin("RSIN: 99990000") == []  # eight digits
    assert rre.nl.rsin("RSIN: 9999000060") == []  # ten
    assert rre.nl.rsin("RSIN: 000000000") == []
    assert rre.nl.rsin("BSN: 999900006") == []  # another keyword
    assert rre.nl.rsin("arsin 999900006") == []
    assert rre.nl.rsin("RSIN: NL999900006B01") == []  # the VAT number


def test_hard_street_address():
    assert rre.nl.street_address("Keizersgracht 123") == ["Keizersgracht 123"]
    assert rre.nl.street_address("(Prins Hendrikkade 12-H)") == ["Hendrikkade 12-H"]
    assert rre.nl.street_address("Dorpsstr. 5, Ergens") == ["Dorpsstr. 5"]
    assert rre.nl.street_address("KERKSTRAAT 12") == ["KERKSTRAAT 12"]
    assert rre.nl.street_address("Laan van Meerdervoort 50") == ["Laan van Meerdervoort 50"]
    assert rre.nl.street_address("'s-Gravendijkwal 12") == ["Gravendijkwal 12"]
    assert rre.nl.street_address("Hoofdweg 12 III en Oudegracht 231bis") == ["Hoofdweg 12 III", "Oudegracht 231bis"]
    assert rre.nl.street_address("Kerkstraat") == []  # no house number
    assert rre.nl.street_address("Kerkstraat 0") == []
    assert rre.nl.street_address("Kerkstraat 123456") == []
    assert rre.nl.street_address("Kerkstraat12") == []
    assert rre.nl.street_address("kerkstraat 12") == []
    assert rre.nl.street_address("Onderweg 10 minuten") == []
    assert rre.nl.street_address("Laan 5") == []


def test_hard_tikkie_link():
    assert rre.nl.tikkie_link("tikkie.me/pay/AbCd1234") == ["tikkie.me/pay/AbCd1234"]
    assert rre.nl.tikkie_link("www.tikkie.me/pay/Xyz789Abc") == ["www.tikkie.me/pay/Xyz789Abc"]
    assert rre.nl.tikkie_link("http://tikkie.me/pay/Tikkie/Ab3d5f7h") == ["http://tikkie.me/pay/Tikkie/Ab3d5f7h"]
    assert rre.nl.tikkie_link("(https://tikkie.me/pay/Xyz123).") == ["https://tikkie.me/pay/Xyz123"]
    assert rre.nl.tikkie_link("<https://www.tikkie.me/pay/QwErTy12>") == ["https://www.tikkie.me/pay/QwErTy12"]
    assert rre.nl.tikkie_link("Tikkie.me/pay/AbCd1234 graag") == ["Tikkie.me/pay/AbCd1234"]  # capitalized
    assert rre.nl.tikkie_link("tikkie.me/AbCd1234") == []  # no /pay/
    assert rre.nl.tikkie_link("tikkie.me/pay/") == []
    assert rre.nl.tikkie_link("tikkie.nl/pay/AbCd1234") == []
    assert rre.nl.tikkie_link("faketikkie.me/pay/AbCd1234") == []
    # look-alike domains and paths on other sites
    assert rre.nl.tikkie_link("https://pay-tikkie.me/pay/AbCd1234") == []
    assert rre.nl.tikkie_link("https://example.com/tikkie.me/pay/AbCd1234") == []


def test_hard_vat_number():
    assert rre.nl.vat_number("NL999900006B01") == ["NL999900006B01"]
    assert rre.nl.vat_number("btw-nr: NL 999900018 B01.") == ["NL 999900018 B01"]
    assert rre.nl.vat_number("(NL810000003B02)") == ["NL810000003B02"]
    assert rre.nl.vat_number("NL999999990.B01") == ["NL999999990.B01"]
    assert rre.nl.vat_number("btw NL9999.00.006B01") == ["NL9999.00.006B01"]
    assert rre.nl.vat_number("'NL999999990 B 01'") == ["NL999999990 B 01"]
    assert rre.nl.vat_number("NL99999999B01") == []  # eight digits
    assert rre.nl.vat_number("NL9999999900B01") == []  # ten
    assert rre.nl.vat_number("NL999999990C01") == []
    assert rre.nl.vat_number("NL999999990B1") == []
    assert rre.nl.vat_number("NL999999990B012") == []
    assert rre.nl.vat_number("NL000000000B01") == []
    assert rre.nl.vat_number("BE0999999990") == []  # Belgian
