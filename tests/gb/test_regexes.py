from regular_regexes import rre


def test_national_insurance_number():
    assert rre.gb.national_insurance_number("NINO AB 12 34 56 C and AB123456D") == ["AB 12 34 56 C", "AB123456D"]
    # QQ (the prefix used in examples) and GB are never issued, E is not a suffix
    assert rre.gb.national_insurance_number("QQ 12 34 56 C, GB123456A, AB123456E") == []


def test_nhs_number():
    # 999 000 0000 to 999 999 9999 is reserved for testing
    assert rre.gb.nhs_number("NHS Number: 999 000 0018, nhs no 9990000026") == [
        "NHS Number: 999 000 0018", "nhs no 9990000026"]
    assert rre.gb.nhs_number("NHS Number: 999 000 0019") == []
    assert rre.gb.nhs_number("ref 999 000 0018") == []


def test_utr():
    assert rre.gb.utr("UTR 22345 67890 and Unique Taxpayer Reference: 9000000001") == [
        "UTR 22345 67890", "Unique Taxpayer Reference: 9000000001"]
    assert rre.gb.utr("UTR 12345 67890") == []
    assert rre.gb.utr("ref 22345 67890") == []


def test_vat_number():
    # 999 9999 18 uses the 9755 check (numbers from November 2009)
    assert rre.gb.vat_number("VAT GB999 9999 73, XI 999 9999 18 and GBGD001") == [
        "GB999 9999 73", "XI 999 9999 18", "GBGD001"]
    assert rre.gb.vat_number("VAT Reg No: 999 9999 73, branch GB123456782012") == [
        "VAT Reg No: 999 9999 73", "GB123456782012"]
    assert rre.gb.vat_number("GB999 9999 74") == []
    # a 9755 check on a number starting with 0, GD above 499, HA below 500
    assert rre.gb.vat_number("GB012 3456 62, GBGD500, GBHA499") == []


def test_company_number():
    assert rre.gb.company_number("Registered in England and Wales No. 01234567, company no SC123456") == [
        "Registered in England and Wales No. 01234567", "company no SC123456"]
    assert rre.gb.company_number("order no. 01234567") == []


def test_iban():
    assert rre.gb.iban("pay GB29 NWBK 6016 1331 9268 19 or GB29 NWBK 601613 31926819") == [
        "GB29 NWBK 6016 1331 9268 19", "GB29 NWBK 601613 31926819"]
    assert rre.gb.iban("GB29 NWBK 6016 1331 9268 18") == []
    assert rre.gb.iban("BE68 5390 0754 7034") == []


def test_bic():
    assert rre.gb.bic("BIC NWBKGB2L or BARCGB22XXX") == ["NWBKGB2L", "BARCGB22XXX"]
    assert rre.gb.bic("GEBABEBB") == []


def test_sort_code():
    assert rre.gb.sort_code("sort code 60-16-13, account number 31926819") == [
        "sort code 60-16-13, account number 31926819"]
    assert rre.gb.sort_code("pay 60-16-13 31926819 or s/c 601613") == ["60-16-13 31926819", "s/c 601613"]
    assert rre.gb.sort_code("on 12-03-24 at 20:00") == []


def test_passport_number():
    assert rre.gb.passport_number("Passport No: 123456789") == ["Passport No: 123456789"]
    assert rre.gb.passport_number("ref 123456789, passport 12345678") == []


def test_driving_licence_number():
    # DVLA's example (leaflet INS57P), with and without its grouping; 35 is the issue number
    assert rre.gb.driving_licence_number("MORGA657054SM9IJ 35 and MORGA 657054 SM 9IJ") == [
        "MORGA657054SM9IJ", "MORGA 657054 SM 9IJ"]
    assert rre.gb.driving_licence_number("MORGA651354SM9IJ") == []  # month 13


def test_mrz_passport():
    # ICAO 9303 specimen with GBR nationality, and GBN (British National (Overseas))
    line = "L898902C36GBR7408122F1204159ZE184226B<<<<<10"
    bno = line.replace("GBR", "GBN")
    assert rre.gb.mrz_passport(f"mrz {line} {bno}") == [line, bno]
    assert rre.gb.mrz_passport(line.replace("C36", "C37")) == []
    assert rre.gb.mrz_passport(line.replace("GBR", "BEL")) == []


def test_phone_number():
    assert rre.gb.phone_number("call 020 7946 0123, +44 (0)161 496 0999 or (01234) 567890") == [
        "020 7946 0123", "+44 (0)161 496 0999", "(01234) 567890"]
    assert rre.gb.phone_number("+44 7400 123456") == ["+44 7400 123456"]
    # Ofcom's mobile numbers for drama are never given out, so libphonenumber does not count them as valid
    assert rre.gb.phone_number("+44 7700 900123") == []
    assert rre.gb.phone_number("on 01-02-2024 12:30 or 0470 12 34 56") == []


def test_mobile_number():
    assert rre.gb.mobile_number("mob 07400 123456 or +44 7400 123 456") == ["07400 123456", "+44 7400 123 456"]
    assert rre.gb.mobile_number("020 7946 0123 or 07400 12345") == []


def test_msisdn():
    assert rre.gb.msisdn("msisdn 447400123456") == ["447400123456"]
    assert rre.gb.msisdn("442079460123 or 4477009001234") == []


def test_premium_number():
    assert rre.gb.premium_number("call 0909 879 0123 or +44 909 879 0999") == ["0909 879 0123", "+44 909 879 0999"]
    assert rre.gb.premium_number("08081 570123") == []


def test_imsi():
    assert rre.gb.imsi("imsi 234150123456789 and 235770123456789") == ["234150123456789", "235770123456789"]
    assert rre.gb.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.gb.iccid("sim 89441000000000000018") == ["89441000000000000018"]
    assert rre.gb.iccid("sim 89441000000000000019") == []
    assert rre.gb.iccid("sim 89320112345678901232") == []


def test_license_plate():
    assert rre.gb.license_plate("car BD51 SMR, van P123 ABC and old ABC 123D") == ["BD51 SMR", "P123 ABC", "ABC 123D"]
    # I and Q are never used in the area letters, I and Q never in the random letters
    assert rre.gb.license_plate("IQ12 ABC, BD51 SQI, 1-ABC-123") == []
    # prefix plates were issued from 21 (1 to 20 were held back), so paper sizes and cable types stay out
    assert rre.gb.license_plate("print A4 PDF, a USB 3C cable") == []


def test_postal_code():
    assert rre.gb.postal_code("SW1A 1AA, M1 1AE and EC1A1BB") == ["SW1A 1AA", "M1 1AE", "EC1A1BB"]
    # no QA area, C never in the inward code
    assert rre.gb.postal_code("QA1 1AA, SW1A 1AC, 1000 Brussel") == []


def test_street_address():
    assert rre.gb.street_address("lives at 221B Baker Street, London") == ["221B Baker Street"]
    assert rre.gb.street_address("Flat 3, 12 High Road and 4 Privet Drive") == ["Flat 3, 12 High Road", "4 Privet Drive"]
    assert rre.gb.street_address("Kerkstraat 12 and 3 apples") == []
    # St before a capitalised word is Saint
    assert rre.gb.street_address("on 17 March St Patrick's Day, at 10 Downing St") == ["10 Downing St"]


def test_company_name():
    assert rre.gb.company_name("invoice from Acme Widgets Ltd. to Example Holdings PLC") == [
        "Acme Widgets Ltd.", "Example Holdings PLC"]
    assert rre.gb.company_name("a limited offer from plc") == []


def test_aircraft_registration():
    assert rre.gb.aircraft_registration("flew G-ABCD and G-EZAB") == ["G-ABCD", "G-EZAB"]
    assert rre.gb.aircraft_registration("OO-ABC, G-ABC, G-ABCDE") == []
