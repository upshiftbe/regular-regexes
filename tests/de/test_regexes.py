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


# hardened tests: every value made up or a documented specimen; each negative is one near-miss or look-alike


def test_hard_tax_id():
    f = rre.de.tax_id
    assert f("47156273896") == ["47156273896"]
    assert f("Steuer-ID: 57 328 190 409.") == ["57 328 190 409"]
    assert f("(26471938572)") == ["26471938572"]
    assert f("„39581602432“ und 72 048 193 575") == ["39581602432", "72 048 193 575"]
    assert f("Die IdNr 90513628796 gehört zu ihm") == ["90513628796"]
    for text in ("47156273897", "4715627389", "471562738961", "07156273896", "47-156-273-896",
                 "11111111116", "DE123456788", "x47156273896"):
        assert f(text) == [], text


def test_hard_vat_number():
    f = rre.de.vat_number
    assert f("DE812345673") == ["DE812345673"]
    assert f("USt-IdNr.: DE 136 548 922.") == ["DE 136 548 922"]
    assert f("(DE298765435)") == ["DE298765435"]
    assert f("„DE314159262“, DE271828180 und DE999999995") == ["DE314159262", "DE271828180", "DE999999995"]
    for text in ("DE812345674", "DE81234567", "DE8123456730", "de812345673", "XDE812345673", "ATU12345678",
                 "DE-812345673", "DE012345675"):
        assert f(text) == [], text


def test_hard_pension_insurance_number():
    f = rre.de.pension_insurance_number
    assert f("65170839J003") == ["65170839J003"]
    assert f("SV-Nummer: 12 010180 M 024.") == ["12 010180 M 024"]
    assert f("(04150372A550)") == ["04150372A550"]
    assert f("„53 311299 S 127“, 81240688K075") == ["53 311299 S 127", "81240688K075"]
    assert f("Versicherungsnummer 40 020995 W 338 laut Ausweis") == ["40 020995 W 338"]
    for text in ("65170839J004", "65170839J00", "65170839j003", "X65170839J003", "65 170839 J 0030",
                 "99170839J003", "65-170839-J-003"):
        assert f(text) == [], text


def test_hard_health_insurance_number():
    f = rre.de.health_insurance_number
    assert f("B123456782") == ["B123456782"]
    assert f("KVNR: M987654323.") == ["M987654323"]
    assert f("(Z000000017)") == ["Z000000017"]
    assert f("„K246813573“") == ["K246813573"]
    assert f("Versichertennummer T135792469 laut Karte, C000500021") == ["T135792469", "C000500021"]
    for text in ("B123456783", "B12345678", "B1234567820", "b123456782", "XB123456782", "B 123456782",
                 "DE123456788"):
        assert f(text) == [], text


def test_hard_id_card_number():
    f = rre.de.id_card_number
    assert f("L01X00T47") == ["L01X00T47"]
    assert f("(LZ6311T47)") == ["LZ6311T47"]
    assert f("„M8R4V6KX1“") == ["M8R4V6KX1"]
    assert f("Ausweis-Nr.: PX01234R5.") == ["PX01234R5"]
    assert f("Der Ausweis Y4C9F2H70 ist abgelaufen, N12345678 nicht") == ["Y4C9F2H70", "N12345678"]
    for text in ("T2200012", "T220001293", "A22000129", "T2200A129", "TCFGHJKLM", "XT22000129", "t22000129",
                 "C01X00T47"):
        assert f(text) == [], text


def test_hard_passport_number():
    f = rre.de.passport_number
    assert f("CF4G7H2K1") == ["CF4G7H2K1"]
    assert f("Reisepass-Nr.: K1234567J.") == ["K1234567J"]
    assert f("(G00X7Y4Z9)") == ["G00X7Y4Z9"]
    assert f("„HJ4K8L2M0“ und FX7Y9Z1R3") == ["HJ4K8L2M0", "FX7Y9Z1R3"]
    assert f("Der Pass J7K8L9M01 liegt vor") == ["J7K8L9M01"]
    for text in ("c01x00t47", "C01X00T4", "C01X00T478", "B01X00T47", "C01X00E47", "CFGHJKLMN", "XC01X00T47",
                 "T22000129"):
        assert f(text) == [], text


def test_hard_mrz_id_card():
    f = rre.de.mrz_id_card
    lines = ["IDD<<L01X00T471<<<<<<<<<<<<<<<", "IDD<<LZ6311T475<<<<<<<<<<<<<<<", "IDD<<M8R4V6KXN4<<<<<<<<<<<<<<<",
             "IDD<<PX01234R54<<<<<<<<<<<<<<<", "IDD<<Y4C9F2H702<<<<<<<<<<<<<<<", "ARD<<Y000047126<<<<<<<<<<<<<<<"]
    assert f(lines[0]) == [lines[0]]
    assert f(f"MRZ: {lines[1]}\n6408125F2702283D<<<<<<<<<<<<<4") == [lines[1]]
    assert f(f"({lines[2]})") == [lines[2]]
    assert f(f"„{lines[3]}“") == [lines[3]]
    assert f(f"Zeile 1 {lines[4]} gelesen, Aufenthaltstitel {lines[5]}") == [lines[4], lines[5]]
    for text in (lines[0].replace("T471", "T472"), lines[0] + "<", "X" + lines[0], lines[0].lower(),
                 lines[0].replace("IDD<<", "IDF<<"), "P<D<<MUSTERMANN<<ERIKA<<<<<<<<<<<<<<<<<<<<<",
                 "IDD<<L01X00T471<<<<<<<<<<<<<<"):
        assert f(text) == [], text


def test_hard_mrz_passport():
    f = rre.de.mrz_passport
    lines = ["CF4G7H2K18D<<8501019M3106305<<<<<<<<<<<<<<<2", "K1234567J5D<<9902299X3001019<<<<<<<<<<<<<<<0",
             "G00X7Y4Z90D<<7512249<2810157<<<<<<<<<<<<<<<6", "HJ4K8L2M05D<<9003152M3306149<<<<<<<<<<<<<<<6",
             "FX7Y9Z1R32D<<0211303F2901019<<<<<<<<<<<<<<<8"]
    assert f(lines[0]) == [lines[0]]
    assert f(f"P<D<<MUSTERMANN<<ERIKA<<<<<<<<<<<<<<<<<<<<<<\n{lines[1]}") == [lines[1]]
    assert f(f"({lines[2]})") == [lines[2]]
    assert f(f"„{lines[3]}“ und {lines[4]}") == [lines[3], lines[4]]
    line = lines[0]
    for text in (line.replace("K18D", "K17D"), line.replace("8501019", "8501018"), line.replace("3106305", "3106304"),
                 line.replace("D<<", "BEL"), line + "<", line.lower(), "X" + line):
        assert f(text) == [], text


def test_hard_company_register_number():
    f = rre.de.company_register_number
    assert f("HRB12345") == ["HRB12345"]
    assert f("Handelsregister: HRB-Nr. 98765.") == ["HRB-Nr. 98765"]
    assert f("(HRA 1234)") == ["HRA 1234"]
    assert f("Amtsgericht Frankfurt am Main, HRB 54321") == ["Amtsgericht Frankfurt am Main, HRB 54321"]
    assert f("Registergericht: Amtsgericht Kiel HRB 1234 KI, Genossenschaft GnR 123") == [
        "Amtsgericht Kiel HRB 1234 KI", "GnR 123"]
    # a suffix is the court's one or two letters, never a word of an all-caps text
    assert f("EINGETRAGEN UNTER HRB 24680 UND HRA 13579") == ["HRB 24680", "HRA 13579"]
    for text in ("HRB 1234567", "HRBX 123", "XHRB 123", "hrb 12345", "HRB 12.345", "HR 12345", "PLZ 12345",
                 "HRB 0815"):
        assert f(text) == [], text


def test_hard_iban():
    f = rre.de.iban
    assert f("DE91100000000123456789") == ["DE91100000000123456789"]
    assert f("IBAN: DE44 5001 0517 5407 3249 31.") == ["DE44 5001 0517 5407 3249 31"]
    assert f("(DE18120300000012345678)") == ["DE18120300000012345678"]
    assert f("„DE20 7002 0270 0000 1234 56“") == ["DE20 7002 0270 0000 1234 56"]
    assert f("Bitte auf DE33200400000611223344 überweisen, nicht DE10 7605 0101 0001 2345 67") == [
        "DE33200400000611223344", "DE10 7605 0101 0001 2345 67"]
    for text in ("DE91100000000123456788", "DE9110000000012345678", "DE911000000001234567890",
                 "de91100000000123456789", "XDE91100000000123456789", "AT611904300234573201",
                 "DE91-1000-0000-0123-4567-89"):
        assert f(text) == [], text


def test_hard_bic():
    f = rre.de.bic
    assert f("MUSTDEFFXXX") == ["MUSTDEFFXXX"]
    assert f("BIC: BEISDEM1.") == ["BEISDEM1"]
    assert f("(QRSTDE3S)") == ["QRSTDE3S"]
    assert f("„ABCDDE12345“ oder ZYXWDEBB100") == ["ABCDDE12345", "ZYXWDEBB100"]
    assert f("Die Bank TESTDE2H zahlt") == ["TESTDE2H"]
    for text in ("MUSTDEF", "MUSTDEFFXX", "MUSTDEFFXXXX", "mustdeff", "XMUSTDEFF", "MUSTFRPP", "MU5TDEFF",
                 "DE89370400440532013000"):
        assert f(text) == [], text


def test_hard_phone_number():
    # Bundesnetzagentur drama numbers (030 23125, 040 66969, 069 90009, 089 99998, 0221 4710)
    f = rre.de.phone_number
    assert f("Tel.: 030 23125456.") == ["030 23125456"]
    assert f("+49 69 90009 321") == ["+49 69 90009 321"]
    assert f("Zentrale (089) 99998 765, Fax 0049 40 66969 001") == ["(089) 99998 765", "0049 40 66969 001"]
    assert f("„0221/4710 456“ oder +49 (0)221 4710-789") == ["0221/4710 456", "+49 (0)221 4710-789"]
    assert f("Büro 06990009123, Fax folgt") == ["06990009123"]
    # an area code is never split: 020 is no area code (0201 is), Frankfurt is 069 and not 0694
    for text in ("AWB 020-12345675", "070 22 33 44", "0694 20 12 34", "0301 2345678", "(0301) 2345678",
                 "030 23125000 12", "am 12.03.2024 um 14:30", "+33 1 23 45 67 89", "030 2312"):
        assert f(text) == [], text


def test_hard_mobile_number():
    # Bundesnetzagentur drama numbers (0152 28817386-99, 0171 39200xx, 0176 040690xx)
    f = rre.de.mobile_number
    assert f("0152 28817390") == ["0152 28817390"]
    assert f("Handy: 01713920048.") == ["01713920048"]
    assert f("(0171 3920045) oder 0049 171 3920046") == ["0171 3920045", "0049 171 3920046"]
    assert f("„0152/28817392“, +49 152 28817391") == ["0152/28817392", "+49 152 28817391"]
    assert f("Ruf 0176-04069012 an, sonst +49 (0)176 04069013") == ["0176-04069012", "+49 (0)176 04069013"]
    for text in ("030 23125000", "0152 2881738", "0152 28817386 12", "DPD 0150 1234 5678 90 S", "0800 1234567",
                 "4915228817386", "+43 664 1234567"):
        assert f(text) == [], text


def test_hard_msisdn():
    f = rre.de.msisdn
    assert f("4915228817393") == ["4915228817393"]
    assert f("A-Nummer: 491713920049.") == ["491713920049"]
    assert f("(4917604069021)") == ["4917604069021"]
    assert f("msisdn=4915228817394; b=491713920050") == ["4915228817394", "491713920050"]
    for text in ("+4915228817386", "49152288173860", "49171392001", "004915228817386", "x4915228817386",
                 "4930231250000", "4380012345678"):
        assert f(text) == [], text


def test_hard_premium_number():
    f = rre.de.premium_number
    assert f("+49 900 1 234567") == ["+49 900 1 234567"]
    assert f("Hotline: 0900-5 654321.") == ["0900-5 654321"]
    assert f("(0180 6 123456)") == ["0180 6 123456"]
    assert f("„0137 1 234567“ oder 0049 180 3 123456") == ["0137 1 234567", "0049 180 3 123456"]
    assert f("Wählen Sie 0900/1234567 jetzt") == ["0900/1234567"]
    for text in ("0800 1234567", "0700 12345678", "0900 5 12345", "0900 5 1234567", "0900 5 123456 7",
                 "0190 123456", "030 23125000"):
        assert f(text) == [], text


def test_hard_imsi():
    f = rre.de.imsi
    assert f("262021234567890") == ["262021234567890"]
    assert f("IMSI: 262079876543210.") == ["262079876543210"]
    assert f("(262031122334456)") == ["262031122334456"]
    assert f("„262110000000001“ und 262200123456789") == ["262110000000001", "262200123456789"]
    assert f("Die SIM 262016543210987 war aktiv") == ["262016543210987"]
    for text in ("26201123456789", "2620112345678901", "214011234567890", "x262011234567890",
                 "262 01 1234567890", "IMEI 352099001761481"):
        assert f(text) == [], text


def test_hard_iccid():
    f = rre.de.iccid
    assert f("894902000012345679") == ["894902000012345679"]
    assert f("ICCID: 89490112345678901233.") == ["89490112345678901233"]
    assert f("(8949220000000000012)") == ["8949220000000000012"]
    assert f("„89490700112233445561“ und 894911000000000079") == ["89490700112233445561", "894911000000000079"]
    assert f("Die Karte 8949020000123456788 lag bei") == ["8949020000123456788"]
    for text in ("894902000012345678", "89490200001234567", "894901123456789012334", "8934011234567890128",
                 "x8949020000123456788", "8949 0200 0012 3456 788"):
        assert f(text) == [], text


def test_hard_license_plate():
    f = rre.de.license_plate
    assert f("ABC-DE 123") == ["ABC-DE 123"]
    assert f("(K-ZZ 4711)") == ["K-ZZ 4711"]
    assert f("„S-AB 12H“") == ["S-AB 12H"]
    assert f("Kennzeichen: HB-XY 5.") == ["HB-XY 5"]
    assert f("Der Wagen B-MW-1234 parkte vor AB-CD 1234") == ["B-MW-1234", "AB-CD 1234"]
    # at most eight characters, so a three-letter district has no two letters and four digits
    for text in ("ABC-DE 1234", "VW ID 3", "B-MW 12345", "BMW 1234", "b-mw 123", "B-MW 123X", "B-ÄB 12",
                 "B-MWX 12"):
        assert f(text) == [], text


def test_hard_postal_code_city():
    f = rre.de.postal_code_city
    assert f("01067 Dresden") == ["01067 Dresden"]
    assert f("(04109 Leipzig)") == ["04109 Leipzig"]
    assert f("„20095 Hamburg“") == ["20095 Hamburg"]
    assert f("Anschrift: Kurallee 1, 53173 Bad Godesberg.") == ["53173 Bad Godesberg"]
    assert f("66111 St. Ingbert, 79098 Freiburg im Breisgau und 50667 Köln-Altstadt") == [
        "66111 St. Ingbert", "79098 Freiburg im Breisgau", "50667 Köln-Altstadt"]
    for text in ("In 10115 Fällen wurde ermittelt", "00123 Berlin", "1011 Berlin", "101150 Berlin", "80331 münchen",
                 "nach 10000 Stunden", "seit 12000 Jahren"):
        assert f(text) == [], text


def test_hard_street_address():
    f = rre.de.street_address
    assert f("Friedrichstraße 123a") == ["Friedrichstraße 123a"]
    assert f("(Goethestraße 7)") == ["Goethestraße 7"]
    assert f("„Schillerplatz 2“") == ["Schillerplatz 2"]
    assert f("Er wohnt Rosenweg 12 b, vorher Hauptstr.12") == ["Rosenweg 12 b", "Hauptstr.12"]
    assert f("Kurfürstendamm 21; Bahnhofstraße 5/7; Lindenstrasse 5") == [
        "Kurfürstendamm 21", "Bahnhofstraße 5/7", "Lindenstrasse 5"]
    assert f("Hamburger Ring 12, Neuer Weg 3, Kirchgasse 3 und Mainufer 4") == [
        "Hamburger Ring 12", "Neuer Weg 3", "Kirchgasse 3", "Mainufer 4"]
    for text in ("Hauptstraße 1234", "hauptstraße 12", "Stellplatz 12", "Ring 3", "Ringstraße ohne Nummer",
                 "Platz 3 im Ranking", "Tabellenplatz 1",
                 "Lagerplatz 12-04"):
        assert f(text) == [], text


def test_hard_company_name():
    f = rre.de.company_name
    assert f("Muster AG") == ["Muster AG"]
    assert f("(Schmidt & Partner PartG mbB)") == ["Schmidt & Partner PartG mbB"]
    assert f("„Bäckerei Krause e.K.“, Wohnbau Nord eG") == ["Bäckerei Krause e.K.", "Wohnbau Nord eG"]
    assert f("Meier & Söhne OHG, Kanzlei Weber GbR und Muster KGaA.") == [
        "Meier & Söhne OHG", "Kanzlei Weber GbR", "Muster KGaA"]
    assert f("Dr. Klein GmbH beliefert Gemeinnützige Hilfe gGmbH") == ["Dr. Klein GmbH", "Gemeinnützige Hilfe gGmbH"]
    # a capitalised word that starts the sentence is not part of the name
    assert f("Gegen Muster Logistik GmbH wird ermittelt. Über Nordlicht Solar SE kam das Geld.") == [
        "Muster Logistik GmbH", "Nordlicht Solar SE"]
    for text in ("muster gmbh", "Hans Meier GmbHs", "Das ist eine GmbH", "Er gründete eine GmbH.", "GmbH",
                 "Muster Ag", "XY AGB"):
        assert f(text) == [], text


def test_hard_aircraft_registration():
    f = rre.de.aircraft_registration
    assert f("D-EXYZ") == ["D-EXYZ"]
    assert f("Die Maschine (D-HABC) landete.") == ["D-HABC"]
    assert f("Kennung „D-KOOL“, dann D-MZZZ.") == ["D-KOOL", "D-MZZZ"]
    assert f("Halter von D-IBCD und D-OFFA") == ["D-IBCD", "D-OFFA"]
    for text in ("D-ABC", "D-ABCDE", "D-abcd", "AD-ABCD", "D-ABCD1", "D-AB 123", "OO-ABC", "D-10115", "D ABCD"):
        assert f(text) == [], text


def test_hard_ecli():
    f = rre.de.ecli
    assert f("ECLI:DE:BFH:2021:B.150421.IXB12.20.0") == ["ECLI:DE:BFH:2021:B.150421.IXB12.20.0"]
    assert f("(ECLI:DE:BAG:2019:110219.U.1AZR123.18.0)") == ["ECLI:DE:BAG:2019:110219.U.1AZR123.18.0"]
    assert f("„ECLI:DE:OLGK:2020:0101.1U12.19.00“") == ["ECLI:DE:OLGK:2020:0101.1U12.19.00"]
    assert f("siehe ECLI:DE:BVerwG:2016:270716U1C1.16.0, ECLI:DE:LGHH:2022:1234.5O67.21.00.") == [
        "ECLI:DE:BVerwG:2016:270716U1C1.16.0", "ECLI:DE:LGHH:2022:1234.5O67.21.00"]
    assert f("Urteil ECLI:DE:BSG:2018:X1: rechtskräftig") == ["ECLI:DE:BSG:2018:X1"]
    for text in ("ecli:de:bgh:2017:x1", "ECLI:DE:BGH:17:x1", "ECLI:DE::2017:X1", "ECLI:DE:BGH:2017:",
                 "XECLI:DE:BGH:2017:X1", "ECLI:AT:OGH0002:2017:0010OB00001.17A.0101.000", "ECLI DE BGH 2017 X1"):
        assert f(text) == [], text
