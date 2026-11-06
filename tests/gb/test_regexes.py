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


# Hard tests: every written form and context of a value, and one near miss per call. Numbers below are made up with
# valid check digits, from the ranges kept for testing and drama (NHS 999, Ofcom 0909 879), or the specimens above.


def test_hard_aircraft_registration():
    assert rre.gb.aircraft_registration("G-XYZW") == ["G-XYZW"]
    assert rre.gb.aircraft_registration("the aircraft G-KLMN landed.") == ["G-KLMN"]
    assert rre.gb.aircraft_registration("(G-ZZAB)") == ["G-ZZAB"]
    assert rre.gb.aircraft_registration('"G-OPQR"') == ['G-OPQR']
    assert rre.gb.aircraft_registration("registered G-ABCD, then G-WXYZ") == ["G-ABCD", "G-WXYZ"]
    assert rre.gb.aircraft_registration("G-ABCD/G-EFGH") == ["G-ABCD", "G-EFGH"]
    for text in (
        "G-ABCDE",  # five letters
        "g-abcd",  # lower case
        "XG-ABCD",  # inside a longer token
        "G-ABC1",  # a digit
        "F-ABCD",  # French
        "G ABCD",  # no dash
    ):
        assert rre.gb.aircraft_registration(text) == [], text


def test_hard_bic():
    assert rre.gb.bic("ABCDGB2L") == ["ABCDGB2L"]
    assert rre.gb.bic("BIC: EXMPGB22XXX.") == ["EXMPGB22XXX"]
    assert rre.gb.bic("(TESTGB2LABC)") == ["TESTGB2LABC"]
    assert rre.gb.bic('"BANKGB21"') == ['BANKGB21']
    assert rre.gb.bic("swift ZYXWGB33 then the sort code") == ["ZYXWGB33"]
    assert rre.gb.bic("ABCDGB2L/EXMPGB22XXX") == ["ABCDGB2L", "EXMPGB22XXX"]
    for text in (
        "ABCDGB2",  # seven characters
        "ABCDGB2LX",  # nine
        "ABCDGB2LXXXX",  # twelve
        "AB1DGB2L",  # a digit in the bank code
        "ABCDFRPP",  # French
        "GBABCD2L",  # GB in the wrong place
        "abcdgb2l",  # lower case
    ):
        assert rre.gb.bic(text) == [], text


def test_hard_company_name():
    assert rre.gb.company_name("ACME WIDGETS LIMITED") == ["ACME WIDGETS LIMITED"]
    assert rre.gb.company_name("(Example Trading LLP)") == ["Example Trading LLP"]
    assert rre.gb.company_name('"Northern Lights CIC"') == ['Northern Lights CIC']
    assert rre.gb.company_name("paid Smith & Sons Ltd on time") == ["Smith & Sons Ltd"]
    assert rre.gb.company_name("J. Smith Ltd, Leeds") == ["J. Smith Ltd"]
    assert rre.gb.company_name("Example 2020 Holdings plc.") == ["Example 2020 Holdings plc."]
    # a name does not run on from the line above
    assert rre.gb.company_name("Invoice\nAcme Widgets Ltd") == ["Acme Widgets Ltd"]
    for text in (
        "Acme Ltda",  # Portuguese
        "the ltd",  # no name
        "Acme GmbH",  # German
        "Acme SARL",  # French
        "Ltd",  # legal form alone
        "acme ltd",  # name in lower case
        "AcmeLtd",  # glued to the name
    ):
        assert rre.gb.company_name(text) == [], text


def test_hard_company_number():
    assert rre.gb.company_number("Company Registration Number: 01234567") == ["Company Registration Number: 01234567"]
    assert rre.gb.company_number("(CRN 12345678)") == ["CRN 12345678"]
    assert rre.gb.company_number("Registered in Scotland No. SC123456.") == ["Registered in Scotland No. SC123456"]
    assert rre.gb.company_number("Company No. OC301234") == ["Company No. OC301234"]
    assert rre.gb.company_number("registered number 1234567") == ["registered number 1234567"]
    assert rre.gb.company_number("Registered in Northern Ireland number NI012345") == [
        "Registered in Northern Ireland number NI012345"]
    for text in (
        "company no 12345",  # five digits
        "company no 123456789",  # nine
        "company no SC12345",  # five after the prefix
        "ACRN 01234567",  # keyword inside a longer word
        "registration number 01234567",  # no company
        "company number",  # no number
    ):
        assert rre.gb.company_number(text) == [], text


def test_hard_driving_licence_number():
    assert rre.gb.driving_licence_number("SMITH751025JA9AB") == ["SMITH751025JA9AB"]
    assert rre.gb.driving_licence_number("(SMITH751025JA9AB)") == ["SMITH751025JA9AB"]
    assert rre.gb.driving_licence_number("licence no. MA999 812150 J9 9XY.") == ["MA999 812150 J9 9XY"]
    assert rre.gb.driving_licence_number("Driver number: JONES610313AB9CD") == ["JONES610313AB9CD"]
    assert rre.gb.driving_licence_number('"MORGA 657054 SM9IJ"') == ["MORGA 657054 SM9IJ"]
    assert rre.gb.driving_licence_number("MA999812150J99XY, SMITH751025JA9AB") == [
        "MA999812150J99XY", "SMITH751025JA9AB"]
    for text in (
        "MORGA663054SM9IJ",  # month 63
        "MORGA657324SM9IJ",  # day 32
        "MORGA657004SM9IJ",  # day 00
        "MORGA657054SM9I",  # fifteen characters
        "MORGA657054SM9IJK",  # seventeen
        "morga657054sm9ij",  # lower case
        "9ORGA657054SM9IJ",  # a digit first
    ):
        assert rre.gb.driving_licence_number(text) == [], text


def test_hard_iban():
    assert rre.gb.iban("GB29NWBK60161331926819") == ["GB29NWBK60161331926819"]
    assert rre.gb.iban("IBAN: GB42 ABCD 1234 5612 3456 78.") == ["GB42 ABCD 1234 5612 3456 78"]
    assert rre.gb.iban("(GB73 EXMP 4040 4012 3456 78)") == ["GB73 EXMP 4040 4012 3456 78"]
    assert rre.gb.iban('"GB42ABCD12345612345678"') == ['GB42ABCD12345612345678']
    assert rre.gb.iban("pay into GB29 NWBK 6016 1331 9268 19 today") == ["GB29 NWBK 6016 1331 9268 19"]
    assert rre.gb.iban("GB42ABCD12345612345678/GB73EXMP40404012345678") == [
        "GB42ABCD12345612345678", "GB73EXMP40404012345678"]
    for text in (
        "GB42 ABCD 1234 5612 3456 79",  # wrong check digits
        "GB29 NWBK 6016 1331 9268 1",  # 13 digits
        "GB29 NWBK 6016 1331 9268 190",  # 15 digits
        "GB29 NW1K 6016 1331 9268 19",  # a digit in the bank code
        "gb29nwbk60161331926819",  # lower case
        "XGB29NWBK60161331926819",  # inside a longer token
        "GB29-NWBK-6016-1331-9268-19",  # dashes
    ):
        assert rre.gb.iban(text) == [], text


def test_hard_iccid():
    assert rre.gb.iccid("8944100000000000018") == ["8944100000000000018"]
    assert rre.gb.iccid("ICCID: 89442012345678901235.") == ["89442012345678901235"]
    assert rre.gb.iccid("(894410123456789015)") == ["894410123456789015"]
    assert rre.gb.iccid('"89441000000000000018"') == ['89441000000000000018']
    assert rre.gb.iccid("the SIM 8944100000000000018 was in slot 1") == ["8944100000000000018"]
    assert rre.gb.iccid("8944100000000000018,894410123456789015") == ["8944100000000000018", "894410123456789015"]
    for text in (
        "8944100000000000019",  # wrong check digit
        "89441012345678901",  # 17 digits
        "894420123456789012350",  # 21
        "8933011234567890120",  # French
        "8944 1000 0000 0000 018",  # spaced
        "x8944100000000000018",  # inside a longer token
    ):
        assert rre.gb.iccid(text) == [], text


def test_hard_imsi():
    assert rre.gb.imsi("IMSI: 234300123456789.") == ["234300123456789"]
    assert rre.gb.imsi("(235910123456789)") == ["235910123456789"]
    assert rre.gb.imsi("Jersey imsi=234500123456789;") == ["234500123456789"]
    assert rre.gb.imsi("subscriber 234100123456789 roamed") == ["234100123456789"]
    assert rre.gb.imsi("234150123456789/235770123456789") == ["234150123456789", "235770123456789"]
    assert rre.gb.imsi('"234200123456789"') == ['234200123456789']
    for text in (
        "23415012345678",  # 14 digits
        "2341501234567890",  # 16
        "208011234567890",  # French
        "236150123456789",  # no MCC 236
        "1234150123456789",  # inside a longer number
        "x234150123456789",  # inside a longer token
    ):
        assert rre.gb.imsi(text) == [], text


def test_hard_license_plate():
    assert rre.gb.license_plate("BD51SMR") == ["BD51SMR"]
    assert rre.gb.license_plate("(LV70 ABC)") == ["LV70 ABC"]
    assert rre.gb.license_plate('reg "YX19 KLM"') == ['YX19 KLM']
    assert rre.gb.license_plate("A21 ABC") == ["A21 ABC"]
    assert rre.gb.license_plate("plate GH12 XYZ.") == ["GH12 XYZ"]
    assert rre.gb.license_plate("KLM 99A, 1963") == ["KLM 99A"]
    for text in (
        "BD51 SMI",  # no I
        "BD5 SMR",  # one digit
        "BD51 SMRX",  # four letters
        "XBD51 SMR",  # inside a longer token
        "bd51 smr",  # lower case
        "ABC 9D",  # suffix number below 10
        "ZZ51 SMR",  # no area Z
        "AB-123-CD",  # French
    ):
        assert rre.gb.license_plate(text) == [], text


def test_hard_mobile_number():
    assert rre.gb.mobile_number("+447400123456") == ["+447400123456"]
    assert rre.gb.mobile_number("0044 7400 123456") == ["0044 7400 123456"]
    assert rre.gb.mobile_number("+44 (0)7400 123456") == ["+44 (0)7400 123456"]
    assert rre.gb.mobile_number("(07400 123456)") == ["07400 123456"]
    assert rre.gb.mobile_number("mob: 07400-123-456.") == ["07400-123-456"]
    assert rre.gb.mobile_number("Isle of Man +44 7624 312345") == ["+44 7624 312345"]
    for text in (
        "07400 1234567",  # eleven digits after 0
        "07700 900123",  # Ofcom's drama range, never given out
        "07600 123456",  # pager
        "+33 7 53 12 34 56",  # French
        "4407400123456",  # inside a longer number
        "0161 496 0999",  # landline
    ):
        assert rre.gb.mobile_number(text) == [], text


def test_hard_mrz_passport():
    a = "1234567897GBR8501019M3001019<<<<<<<<<<<<<<<8"
    d = "9876543213GBD9212314F3106154<<<<<<<<<<<<<<<0"
    assert rre.gb.mrz_passport(a) == [a]
    assert rre.gb.mrz_passport(f"P<GBRSMITH<<JOHN<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n{a}") == [a]
    assert rre.gb.mrz_passport(f"({d})") == [d]
    assert rre.gb.mrz_passport(f"line two: {a}.") == [a]
    assert rre.gb.mrz_passport(a.replace("9M", "9<")) == [a.replace("9M", "9<")]  # sex not given
    assert rre.gb.mrz_passport(f"{a} {d}") == [a, d]
    for text in (
        a.replace("897G", "898G"),  # wrong document number check
        a.replace("019M", "018M"),  # wrong birth date check
        a.replace("1019<", "1018<"),  # wrong expiry check
        a.replace("GBR", "FRA"),  # French
        a.replace("GBR", "GBX"),  # no British code GBX
        a[:-1],  # 43 characters
        a + "0",  # 45
    ):
        assert rre.gb.mrz_passport(text) == [], text


def test_hard_msisdn():
    assert rre.gb.msisdn("msisdn=447400123456;") == ["447400123456"]
    assert rre.gb.msisdn("(447624312345)") == ["447624312345"]
    assert rre.gb.msisdn("447797123456") == ["447797123456"]
    assert rre.gb.msisdn("CDR 447400123456, 447797123456") == ["447400123456", "447797123456"]
    assert rre.gb.msisdn('"447400123456"') == ['447400123456']
    assert rre.gb.msisdn("caller 447624312345 at 10:00") == ["447624312345"]
    for text in (
        "+447400123456",  # international format, a phone number
        "00447400123456",  # with 00
        "44740012345",  # eleven digits
        "4474001234567",  # thirteen
        "44 7400 123456",  # spaced
        "33612345678",  # French
    ):
        assert rre.gb.msisdn(text) == [], text


def test_hard_national_insurance_number():
    assert rre.gb.national_insurance_number("AB123456C.") == ["AB123456C"]
    assert rre.gb.national_insurance_number("(CE 12 34 56 A)") == ["CE 12 34 56 A"]
    assert rre.gb.national_insurance_number("NI number: JG 10 34 56 B") == ["JG 10 34 56 B"]
    assert rre.gb.national_insurance_number("AB 123456 C") == ["AB 123456 C"]
    assert rre.gb.national_insurance_number('"ZY123456D"') == ['ZY123456D']
    assert rre.gb.national_insurance_number("NINO ZY123456D and AB123456C") == ["ZY123456D", "AB123456C"]
    for text in (
        "ab123456c",  # lower case
        "AB1234567C",  # seven digits
        "AB12345C",  # five
        "DA123456C",  # no D first
        "AO123456C",  # no O second
        "NK123456A",  # prefix never issued
        "XAB123456C",  # inside a longer token
    ):
        assert rre.gb.national_insurance_number(text) == [], text


def test_hard_nhs_number():
    assert rre.gb.nhs_number("NHS No. 999-000-0034") == ["NHS No. 999-000-0034"]
    assert rre.gb.nhs_number("(NHS number 999 000 0042)") == ["NHS number 999 000 0042"]
    assert rre.gb.nhs_number("nhs: 9990000050.") == ["nhs: 9990000050"]
    assert rre.gb.nhs_number('"NHS 999 000 0069"') == ['NHS 999 000 0069']
    assert rre.gb.nhs_number("patient NHS no 9990000077 seen") == ["NHS no 9990000077"]
    assert rre.gb.nhs_number("NHS 9990000085, NHS 9990000093") == ["NHS 9990000085", "NHS 9990000093"]
    for text in (
        "NHS number 999 123 4567",  # a check digit of 10 is never issued
        "NHS 999 000 001",  # nine digits
        "NHS 99900000180",  # eleven
        "NHS 999 0000 018",  # grouped 3-4-3
        "XNHS 9990000018",  # keyword inside a longer word
        "999 000 0034",  # no keyword
    ):
        assert rre.gb.nhs_number(text) == [], text


def test_hard_passport_number():
    assert rre.gb.passport_number("passport number 123456789.") == ["passport number 123456789"]
    assert rre.gb.passport_number("PASSPORT NO. 987654321") == ["PASSPORT NO. 987654321"]
    assert rre.gb.passport_number("(passport: 135792468)") == ["passport: 135792468"]
    assert rre.gb.passport_number("Passport 102030405, issued 2020") == ["Passport 102030405"]
    assert rre.gb.passport_number("passport no:246813579") == ["passport no:246813579"]
    assert rre.gb.passport_number('"Passport No 123456789"') == ['Passport No 123456789']
    for text in (
        "passport 1234567890",  # ten digits
        "passport no. 12345678A",  # a letter
        "passports 123456789",  # plural
        "Xpassport 123456789",  # keyword inside a longer word
        "Reisepass 123456789",  # German keyword
        "passport no. 123-456-789",  # dashes
    ):
        assert rre.gb.passport_number(text) == [], text


def test_hard_phone_number():
    assert rre.gb.phone_number("+44 20 7946 0123") == ["+44 20 7946 0123"]
    assert rre.gb.phone_number("0044 20 7946 0123") == ["0044 20 7946 0123"]
    assert rre.gb.phone_number("020-7946-0123") == ["020-7946-0123"]
    assert rre.gb.phone_number("tel:+442079460123;") == ["+442079460123"]
    assert rre.gb.phone_number("ring 02079460123 today.") == ["02079460123"]
    assert rre.gb.phone_number('"0161 496 0999"') == ['0161 496 0999']
    for text in (
        "020 7946 012",  # nine digits after 0
        "020 7946 01234",  # eleven
        "+33 1 99 00 12 34",  # French
        "01632 960123",  # Ofcom's drama range
        "02079460123456",  # inside a longer number
        "+44 20 7946 012",  # short after +44
    ):
        assert rre.gb.phone_number(text) == [], text


def test_hard_postal_code():
    assert rre.gb.postal_code("London W1A 2BD.") == ["W1A 2BD"]
    assert rre.gb.postal_code("(GY1 1AA)") == ["GY1 1AA"]
    assert rre.gb.postal_code("Belfast BT1 5GS") == ["BT1 5GS"]
    assert rre.gb.postal_code('"CR2 6XH"') == ['CR2 6XH']
    assert rre.gb.postal_code("M60 1NW, Manchester") == ["M60 1NW"]
    assert rre.gb.postal_code("EH11YZ") == ["EH11YZ"]
    for text in (
        "sw1a 1aa",  # lower case
        "SW1A 1AAA",  # three letters at the end
        "XSW1A 1AA",  # inside a longer token
        "SW 1AA",  # no district
        "SW1A 1A",  # one letter at the end
        "SW1A 1IA",  # no I in the inward code
    ):
        assert rre.gb.postal_code(text) == [], text


def test_hard_premium_number():
    assert rre.gb.premium_number("0044 909 879 0123") == ["0044 909 879 0123"]
    assert rre.gb.premium_number("+44 (0)909 879 0123") == ["+44 (0)909 879 0123"]
    assert rre.gb.premium_number("(0911 234 5678)") == ["0911 234 5678"]
    assert rre.gb.premium_number("call 0982-123-4567 now") == ["0982-123-4567"]
    assert rre.gb.premium_number("09098790123") == ["09098790123"]
    assert rre.gb.premium_number('"0909 879 0123".') == ['0909 879 0123']
    for text in (
        "0909 879 012",  # nine digits after 0
        "0909 879 01234",  # eleven
        "0800 123 4567",  # freephone
        "0870 123 4567",  # not 09
        "+33 8 99 12 34 56",  # French
        "10909 879 0123",  # inside a longer number
    ):
        assert rre.gb.premium_number(text) == [], text


def test_hard_sort_code():
    assert rre.gb.sort_code("Sort Code: 12-34-56") == ["Sort Code: 12-34-56"]
    assert rre.gb.sort_code("s/c 12 34 56, a/c 12345678") == ["s/c 12 34 56, a/c 12345678"]
    assert rre.gb.sort_code("(sort code 123456)") == ["sort code 123456"]
    assert rre.gb.sort_code("SORT CODE 60-16-13 ACCOUNT NO 31926819") == ["SORT CODE 60-16-13 ACCOUNT NO 31926819"]
    assert rre.gb.sort_code("paid from 60-16-13, 31926819.") == ["60-16-13, 31926819"]
    assert rre.gb.sort_code("sort 40-11-22") == ["sort 40-11-22"]
    for text in (
        "sort code 60-16-1",  # five digits
        "sort code 60-16-133",  # seven
        "60-16-13",  # no keyword and no account
        "60-16-13 3192681",  # seven-digit account
        "resort code 601613",  # keyword inside a longer word
        "12-03-2024 12345678",  # a date
    ):
        assert rre.gb.sort_code(text) == [], text


def test_hard_street_address():
    assert rre.gb.street_address("12a High Street") == ["12a High Street"]
    assert rre.gb.street_address("(221b Baker Street)") == ["221b Baker Street"]
    assert rre.gb.street_address("Flat 2, 15 Mill Lane.") == ["Flat 2, 15 Mill Lane"]
    assert rre.gb.street_address("Unit 4B, 7 Mill Lane") == ["Unit 4B, 7 Mill Lane"]
    assert rre.gb.street_address("1 Victoria Rd, Leeds") == ["1 Victoria Rd"]
    assert rre.gb.street_address('"22 Oak Avenue"') == ['22 Oak Avenue']
    # the street ends with its line; St before the next line's town is still Street
    assert rre.gb.street_address("10 Downing St\nLondon") == ["10 Downing St"]
    for text in (
        "the 2019 Supreme Court ruling",  # a year, not a house number
        "the 1960s Coronation Street",
        "Ref 12\nCustomer Services\nLondon Road",  # words from other lines
        "12 high street",  # lower case
        "High Street",  # no number
        "12345 High Street",  # five-digit number
        "12 Rue de la Paix",  # French
    ):
        assert rre.gb.street_address(text) == [], text


def test_hard_utr():
    assert rre.gb.utr("UTR: 2234567890") == ["UTR: 2234567890"]
    assert rre.gb.utr("(UTR 11111 11111)") == ["UTR 11111 11111"]
    assert rre.gb.utr("tax reference no. 9987654321.") == ["tax reference no. 9987654321"]
    assert rre.gb.utr("Unique Taxpayer Reference number: 22345 67890") == [
        "Unique Taxpayer Reference number: 22345 67890"]
    assert rre.gb.utr('"utr 9000000001"') == ['utr 9000000001']
    assert rre.gb.utr("UTR 2234567890, UTR 9987654321") == ["UTR 2234567890", "UTR 9987654321"]
    for text in (
        "UTR 3234567890",  # wrong check digit (the first)
        "UTR 223456789",  # nine digits
        "UTR 22345678901",  # eleven
        "UTR 2234-567890",  # a dash
        "XUTR 2234567890",  # keyword inside a longer word
        "2234567890",  # no keyword
    ):
        assert rre.gb.utr(text) == [], text


def test_hard_vat_number():
    assert rre.gb.vat_number("VAT number: 999 9999 73") == ["VAT number: 999 9999 73"]
    assert rre.gb.vat_number("GB 999 9999 73") == ["GB 999 9999 73"]
    assert rre.gb.vat_number("(GB999999973)") == ["GB999999973"]
    assert rre.gb.vat_number("XI999999973.") == ["XI999999973"]
    assert rre.gb.vat_number("health authority GBHA599") == ["GBHA599"]
    assert rre.gb.vat_number("GB999-9999-73") == ["GB999-9999-73"]
    for text in (
        "GB99999997",  # eight digits
        "GB9999999731",  # ten
        "FR11123456782",  # French
        "XGB999999973",  # inside a longer token
        "vat 999999973",  # no number or no after VAT
        "GB 999 9999 72",  # wrong check digits
    ):
        assert rre.gb.vat_number(text) == [], text
