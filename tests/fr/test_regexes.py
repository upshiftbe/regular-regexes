from regular_regexes import rre

# Phone numbers are from ARCEP's blocks for audiovisual works (01 99 00, 04 65 71, 06 39 98) or from the unallocated
# 079 range. Identity numbers are specimens or computed with impossible commune/serial codes.


def test_nir():
    assert rre.fr.nir("ss 1 85 07 75 000 000 80 ou 185077500000080") == ["1 85 07 75 000 000 80", "185077500000080"]
    # Corsica: 2A and 2B count as 19 and 18 for the key; 7 and 8 are temporary numbers (NIA)
    assert rre.fr.nir("2 75 05 2A 000 000 60, 275052B00000087, 7 85 07 99 000 000 05") == [
        "2 75 05 2A 000 000 60", "275052B00000087", "7 85 07 99 000 000 05"]
    assert rre.fr.nir("1 85 07 75 000 000 81") == []
    assert rre.fr.nir("3 85 07 75 000 000 80") == []


def test_siren():
    assert rre.fr.siren("SIREN 552 120 222, Siren : 356000000") == ["SIREN 552 120 222", "Siren : 356000000"]
    assert rre.fr.siren("RCS Paris B 552 120 222 et 552 120 222 R.C.S. Paris") == [
        "RCS Paris B 552 120 222", "552 120 222 R.C.S."]
    assert rre.fr.siren("SIREN 552 120 223") == []
    assert rre.fr.siren("552 120 222") == []  # no keyword


def test_siret():
    assert rre.fr.siret("SIRET 552 120 222 00013 et 552120222 00013") == ["SIRET 552 120 222 00013", "552120222 00013"]
    # La Poste: digits summing to a multiple of 5, except its head office (Luhn)
    assert rre.fr.siret("Siret: 35600000069588, siège 356 000 000 00048") == ["Siret: 35600000069588", "356 000 000 00048"]
    assert rre.fr.siret("SIRET 552 120 222 00014") == []
    assert rre.fr.siret("55212022200013") == []  # bare 14 digits need the keyword


def test_vat_number():
    assert rre.fr.vat_number("TVA FR 27 552 120 222 et FR39356000000") == ["FR 27 552 120 222", "FR39356000000"]
    assert rre.fr.vat_number("new style FRK7399859412") == ["FRK7399859412"]
    assert rre.fr.vat_number("FR 28 552 120 222, FRK8399859412") == []
    assert rre.fr.vat_number("FRIO334175221") == []  # no I or O in the key


def test_iban():
    assert rre.fr.iban("IBAN FR76 3000 6000 0112 3456 7890 189 BIC BNPAFRPP") == ["FR76 3000 6000 0112 3456 7890 189"]
    assert rre.fr.iban("FR1420041010050500013M02606") == ["FR1420041010050500013M02606"]
    assert rre.fr.iban("FR76 3000 6000 0112 3456 7890 188") == []
    assert rre.fr.iban("BE68 5390 0754 7034") == []


def test_bic():
    assert rre.fr.bic("BIC BNPAFRPP ou SOGEFRPPXXX") == ["BNPAFRPP", "SOGEFRPPXXX"]
    assert rre.fr.bic("GEBABEBB") == []


def test_rib():
    assert rre.fr.rib("RIB 12345 12345 1234567891A 16 et 30006000011234567890189") == [
        "12345 12345 1234567891A 16", "30006000011234567890189"]
    assert rre.fr.rib("12345 12345 1234567891A 17") == []


def test_numero_fiscal():
    # DGFiP's own example
    assert rre.fr.numero_fiscal("numéro fiscal 30 23 217 600 053 ou 3023217600053") == [
        "30 23 217 600 053", "3023217600053"]
    assert rre.fr.numero_fiscal("30 23 217 600 054") == []
    assert rre.fr.numero_fiscal("4023217600136") == []  # starts with 0-3


def test_passport_number():
    assert rre.fr.passport_number("passeport 00AA00000") == ["00AA00000"]
    assert rre.fr.passport_number("00AA0000 et AA00000000") == []


def test_id_card_number():
    # specimen numbers of the old card and the 2021 card
    assert rre.fr.id_card_number("CNI n° 880692310285, carte d'identité X4RTBPFW4") == [
        "CNI n° 880692310285", "X4RTBPFW4"]
    assert rre.fr.id_card_number("CARTE NATIONALE D'IDENTITE N°X4RTBPFW4") == ["X4RTBPFW4"]
    assert rre.fr.id_card_number("carte d'identité FRANCAISE, CNI valide, 123456789") == []
    # the old card's 12 digits only after their keyword, or any 12-digit number would match
    assert rre.fr.id_card_number("880692310285") == []


def test_mrz_id_card():
    # specimens: the 2021 card (TD1, line 1) and the older card (2 x 36, line 2)
    new = "IDFRAX4RTBPFW46<<<<<<<<<<<<<<<"
    old = "8806923102858CORINNE<<<<<<<6512068F6"
    assert rre.fr.mrz_id_card(f"{new}\n9007138F3002119FRA<<<<<<<<<<<6\nMARTIN<<MAELYS<GAELLE<MARIE<<<") == [new]
    assert rre.fr.mrz_id_card(f"IDFRABERTHIER<<<<<<<<<<<<<<<<<<<<<<<\n{old}") == [old]
    assert rre.fr.mrz_id_card(new.replace("46<", "47<")) == []
    assert rre.fr.mrz_id_card(old.replace("6512068", "6512078")) == []  # date of birth no longer matches its check


def test_mrz_passport():
    # ICAO 9303 specimen with FRA nationality
    line = "L898902C36FRA7408122F1204159ZE184226B<<<<<10"
    assert rre.fr.mrz_passport(line) == [line]
    assert rre.fr.mrz_passport(line.replace("C36", "C37")) == []


def test_phone_number():
    assert rre.fr.phone_number("tél 01 99 00 12 34, +33 (0)4 65 71 12 34 ou 06.12.34.56.78") == [
        "01 99 00 12 34", "+33 (0)4 65 71 12 34", "06.12.34.56.78"]
    assert rre.fr.phone_number("0470 12 34 56 et 01 99 00 12") == []  # Belgian grouping, too short


def test_mobile_number():
    assert rre.fr.mobile_number("06 12 34 56 78, +33 6 12 34 56 78, 0033612345678, 07 99 12 34 56") == [
        "06 12 34 56 78", "+33 6 12 34 56 78", "0033612345678", "07 99 12 34 56"]
    # overseas departments: Guyane and Martinique
    assert rre.fr.mobile_number("Cayenne 0694 20 12 34, Fort-de-France +596 696 20 12 34") == [
        "0694 20 12 34", "+596 696 20 12 34"]
    assert rre.fr.mobile_number("01 99 00 12 34 et 07 12 34 56 78") == []


def test_msisdn():
    assert rre.fr.msisdn("msisdn 33612345678, Guyane 594694201234") == ["33612345678", "594694201234"]
    assert rre.fr.msisdn("33199001234 et 33712345678") == []


def test_imsi():
    assert rre.fr.imsi("imsi 208011234567890, Antilles 340011234567890") == ["208011234567890", "340011234567890"]
    assert rre.fr.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.fr.iccid("sim 8933011234567890120") == ["8933011234567890120"]
    assert rre.fr.iccid("sim 8933011234567890121") == []


def test_license_plate():
    assert rre.fr.license_plate("AB-123-CD, AB123CD et l'ancienne 123 ABC 75 ou 1234-AB-2A") == [
        "AB-123-CD", "AB123CD", "123 ABC 75", "1234-AB-2A"]
    assert rre.fr.license_plate("AI-123-CD et 12 AB 00") == []  # no I/O/U in SIV plates, no department 00
    assert rre.fr.license_plate("vol du 15MAR24, né le 12 JAN 85") == []  # dates, not old plates


def test_postal_code_city():
    assert rre.fr.postal_code_city("75008 Paris, 13100 Aix-en-Provence, 76600 Le Havre") == [
        "75008 Paris", "13100 Aix-en-Provence", "76600 Le Havre"]
    assert rre.fr.postal_code_city("15000 EUR, 1000 Bruxelles") == []


def test_street_address():
    assert rre.fr.street_address("au 12 bis rue de la Paix, 75002 Paris") == ["12 bis rue de la Paix"]
    assert rre.fr.street_address("12 BIS RUE DU 4 SEPTEMBRE") == ["12 BIS RUE DU 4 SEPTEMBRE"]
    assert rre.fr.street_address("3, avenue Foch et 8 BOULEVARD HAUSSMANN 75009 PARIS") == [
        "3, avenue Foch", "8 BOULEVARD HAUSSMANN"]
    assert rre.fr.street_address("2 cours de maths, 3 places de parking") == []


def test_company_name():
    assert rre.fr.company_name("contrat entre la Boulangerie de la Gare SARL et Dupont SAS") == [
        "Boulangerie de la Gare SARL", "Dupont SAS"]
    assert rre.fr.company_name("bail de la SCI Les Lilas, géré par la SARL DUPONT & FILS") == [
        "SCI Les Lilas", "SARL DUPONT & FILS"]
    assert rre.fr.company_name("la sas de sécurité, SAS au capital de 1 000 €") == []


def test_aircraft_registration():
    assert rre.fr.aircraft_registration("avion F-ABCD au sol") == ["F-ABCD"]
    assert rre.fr.aircraft_registration("F-ABC, F-ABCDE") == []


def test_ecli():
    assert rre.fr.ecli("voir ECLI:FR:CCASS:2020:C100123.") == ["ECLI:FR:CCASS:2020:C100123"]
    assert rre.fr.ecli("ECLI:BE:CASS:2020:ARR.20200115.1") == []


# Hard tests: every written form and context of a value, and one near miss per call. SIRENs, account numbers and
# document numbers below are made up with valid check digits, or are the specimens used above.


def test_hard_aircraft_registration():
    assert rre.fr.aircraft_registration("F-GKXA") == ["F-GKXA"]
    assert rre.fr.aircraft_registration("l'avion immatriculé F-HBXA s'est posé.") == ["F-HBXA"]
    assert rre.fr.aircraft_registration("(F-OABC)") == ["F-OABC"]
    assert rre.fr.aircraft_registration("« F-BXYZ »") == ["F-BXYZ"]
    assert rre.fr.aircraft_registration("glider F-CDEF and microlight F-PQRS landed") == ["F-CDEF", "F-PQRS"]
    assert rre.fr.aircraft_registration("vol F-GZCP/F-HZZZ") == ["F-GZCP", "F-HZZZ"]
    for text in (
        "F-GKX",  # three letters
        "F-GKXAB",  # five letters
        "F-GKX4",  # a digit
        "f-gkxa",  # lower case
        "AF-GKXA",  # inside a longer token
        "F GKXA",  # no dash
        "G-ABCD",  # British
        "D-EABC",  # German
    ):
        assert rre.fr.aircraft_registration(text) == [], text


def test_hard_bic():
    assert rre.fr.bic("ABCDFRPP") == ["ABCDFRPP"]
    assert rre.fr.bic("BIC : EXMPFRPPXXX.") == ["EXMPFRPPXXX"]
    assert rre.fr.bic("(TESTFR21)") == ["TESTFR21"]
    assert rre.fr.bic("code « BANKFRP1ABC »") == ["BANKFRP1ABC"]
    assert rre.fr.bic("swift ZYXWFR2A, then IBAN") == ["ZYXWFR2A"]
    assert rre.fr.bic("ABCDFRPP/EXMPFRPPXXX") == ["ABCDFRPP", "EXMPFRPPXXX"]
    for text in (
        "ABCDFRP",  # seven characters
        "ABCDFRPPX",  # nine
        "ABCDFRPPXXXX",  # twelve
        "AB1DFRPP",  # a digit in the bank code
        "ABCDBEBB",  # Belgian
        "FRABCDPP",  # FR in the wrong place
        "abcdfrpp",  # lower case
        "ABCDFRPP_1",  # inside a longer token
    ):
        assert rre.fr.bic(text) == [], text


def test_hard_company_name():
    assert rre.fr.company_name("La Boulangerie Martin SARL a signé.") == ["La Boulangerie Martin SARL"]
    assert rre.fr.company_name("(SCI Les Tilleuls)") == ["SCI Les Tilleuls"]
    assert rre.fr.company_name("« Martin & Fils SA »") == ["Martin & Fils SA"]
    assert rre.fr.company_name("EURL d'Artagnan Conseil") == ["EURL d'Artagnan Conseil"]
    assert rre.fr.company_name("GAEC du Moulin Vert, EARL des Prés") == ["GAEC du Moulin Vert", "EARL des Prés"]
    assert rre.fr.company_name("Établissements Moreau SNC") == ["Établissements Moreau SNC"]
    assert rre.fr.company_name("paid to Durand Transports SASU last week") == ["Durand Transports SASU"]
    # a name does not run on from the line above
    assert rre.fr.company_name("Facture\nDurand Transports SASU") == ["Durand Transports SASU"]
    for text in (
        "Dupont sas",  # legal form in lower case
        "SARL",  # legal form alone
        "DupontSARL",  # glued to the name
        "dupont SARL",  # name in lower case
        "Dupont SASX",  # a longer word
        "Dupont GmbH",  # German
        "Dupont Ltd",  # British
        "Dupont BV",  # Dutch
    ):
        assert rre.fr.company_name(text) == [], text


def test_hard_ecli():
    assert rre.fr.ecli("ECLI:FR:CCASS:2020:C100123") == ["ECLI:FR:CCASS:2020:C100123"]
    assert rre.fr.ecli("arrêt ECLI:FR:CECHR:2019:425983.20190612.") == ["ECLI:FR:CECHR:2019:425983.20190612"]
    assert rre.fr.ecli("(ECLI:FR:CC:2020:2020.800.DC)") == ["ECLI:FR:CC:2020:2020.800.DC"]
    assert rre.fr.ecli("« ECLI:FR:CAPAR:2021:12345 »") == ["ECLI:FR:CAPAR:2021:12345"]
    assert rre.fr.ecli("the decision ECLI:FR:CCASS:2019:SO01234, cited") == ["ECLI:FR:CCASS:2019:SO01234"]
    assert rre.fr.ecli("ECLI:FR:CCASS:2020:C100123;ECLI:FR:CCASS:2021:C100456") == [
        "ECLI:FR:CCASS:2020:C100123", "ECLI:FR:CCASS:2021:C100456"]
    for text in (
        "ECLI:FR:CCASS:20:C100123",  # two-digit year
        "ecli:fr:ccass:2020:c100123",  # lower case
        "XECLI:FR:CCASS:2020:C100123",  # inside a longer token
        "ECLI:FR::2020:C100123",  # no court
        "ECLI:FR:CCASS:2020:",  # no number
        "ECLI FR CCASS 2020 C100123",  # spaces for colons
        "ECLI:DE:BGH:2020:120520UVZR123.19.0",  # German
    ):
        assert rre.fr.ecli(text) == [], text


def test_hard_iban():
    assert rre.fr.iban("FR7630006000011234567890189") == ["FR7630006000011234567890189"]
    assert rre.fr.iban("IBAN : FR76 1234 5678 9012 3456 7890 104.") == ["FR76 1234 5678 9012 3456 7890 104"]
    assert rre.fr.iban("(FR14 2004 1010 0505 0001 3M02 606)") == ["FR14 2004 1010 0505 0001 3M02 606"]
    assert rre.fr.iban("« FR7630006000 0112 3456 7890 189 »") == ["FR7630006000 0112 3456 7890 189"]
    assert rre.fr.iban("pay to FR76 3000 6000 0112 3456 7890 189 by Friday") == ["FR76 3000 6000 0112 3456 7890 189"]
    assert rre.fr.iban("FR7612345678901234567890104/FR1420041010050500013M02606") == [
        "FR7612345678901234567890104", "FR1420041010050500013M02606"]
    for text in (
        "FR76 1234 5678 9012 3456 7890 105",  # wrong check digits
        "FR76 3000 6000 0112 3456 7890 18",  # one character short
        "FR76 3000 6000 0112 3456 7890 1891",  # one too many
        "XFR7630006000011234567890189",  # inside a longer token
        "fr7630006000011234567890189",  # lower case
        "DE89370400440532013000",  # German
        "FR76-3000-6000-0112-3456-7890-189",  # dashes
    ):
        assert rre.fr.iban(text) == [], text


def test_hard_iccid():
    assert rre.fr.iccid("8933010000000000002") == ["8933010000000000002"]
    assert rre.fr.iccid("ICCID : 89332012345678901238.") == ["89332012345678901238"]
    assert rre.fr.iccid("(893301123456789019)") == ["893301123456789019"]
    assert rre.fr.iccid("« 8933011234567890120 »") == ["8933011234567890120"]
    assert rre.fr.iccid("the SIM 8933201234567890120 was in slot 2") == ["8933201234567890120"]
    assert rre.fr.iccid("8933010000000000002,8933011234567890120") == ["8933010000000000002", "8933011234567890120"]
    for text in (
        "8933010000000000003",  # wrong check digit
        "89330112345678901",  # 17 digits
        "893320123456789012380",  # 21 digits
        "8932011234567890123",  # Belgian
        "8933 0112 3456 7890 120",  # spaced
        "x8933010000000000002",  # inside a longer token
        "18933010000000000002",  # inside a longer number
    ):
        assert rre.fr.iccid(text) == [], text


def test_hard_id_card_number():
    assert rre.fr.id_card_number("carte nationale d'identité numéro 880692310285") == [
        "carte nationale d'identité numéro 880692310285"]
    assert rre.fr.id_card_number("CARTE D’IDENTITÉ N° : 880692310285.") == ["CARTE D’IDENTITÉ N° : 880692310285"]
    assert rre.fr.id_card_number("CNI: 880692310285") == ["CNI: 880692310285"]
    assert rre.fr.id_card_number("(X4RTBPFW4)") == ["X4RTBPFW4"]
    assert rre.fr.id_card_number("nouvelle carte « AB12CD34E »") == ["AB12CD34E"]
    assert rre.fr.id_card_number("ID card no. X4RTBPFW4, issued 2021") == ["X4RTBPFW4"]
    for text in (
        "X4RTBPFW",  # eight characters
        "X4RTBPFW4A",  # ten
        "ABCDEFGHI",  # letters only
        "x4rtbpfw4",  # lower case
        "https://example.com/files/X4RTBPFW4/scan.pdf",  # a folder in a URL
        "<@X4RTBPFW4>",  # a chat mention
        "CNI n° 88069231028",  # 11 digits after the keyword
        "CNI n° 8806923102851",  # 13 digits
    ):
        assert rre.fr.id_card_number(text) == [], text


def test_hard_imsi():
    assert rre.fr.imsi("208150123456789") == ["208150123456789"]
    assert rre.fr.imsi("IMSI : 208201234567890.") == ["208201234567890"]
    assert rre.fr.imsi("La Réunion (647001234567890)") == ["647001234567890"]
    assert rre.fr.imsi("imsi=742010123456789;") == ["742010123456789"]
    assert rre.fr.imsi("subscriber 208101234567890 roamed") == ["208101234567890"]
    assert rre.fr.imsi("340011234567890/340201234567890") == ["340011234567890", "340201234567890"]
    for text in (
        "20801123456789",  # 14 digits
        "2080112345678901",  # 16 digits
        "234150123456789",  # British
        "1208011234567890",  # inside a longer number
        "208-01-1234567890",  # separators
        "x208011234567890",  # inside a longer token
    ):
        assert rre.fr.imsi(text) == [], text


def test_hard_license_plate():
    assert rre.fr.license_plate("(GH-456-JK)") == ["GH-456-JK"]
    assert rre.fr.license_plate("plaque « LM 789 NP »") == ["LM 789 NP"]
    assert rre.fr.license_plate("the car EF-001-GH was seen") == ["EF-001-GH"]
    assert rre.fr.license_plate("Véhicule 12 ABC 971.") == ["12 ABC 971"]
    assert rre.fr.license_plate("56-XY-13") == ["56-XY-13"]
    assert rre.fr.license_plate("WW-123-AB, temporaire") == ["WW-123-AB"]
    for text in (
        "AB-000-CD",  # 000 is never issued
        "AB-12-CD",  # two digits
        "AB-1234-CD",  # four digits
        "ABC-123-CD",  # three letters in front
        "AB-123-CU",  # no U
        "123 ABC 96",  # no department 96
        "NPPR9-FWDCX-D2C8J-H872K-2YT43",  # last group of a product key
        "#33FF66",  # a colour
        "+32 470 12 34 56 AB12-CD34",  # a phone number and a code
    ):
        assert rre.fr.license_plate(text) == [], text


def test_hard_mobile_number():
    assert rre.fr.mobile_number("(06 12 34 56 78)") == ["06 12 34 56 78"]
    assert rre.fr.mobile_number("+33 (0)7 53 12 34 56") == ["+33 (0)7 53 12 34 56"]
    assert rre.fr.mobile_number("Portable : 06.12.34.56.78.") == ["06.12.34.56.78"]
    assert rre.fr.mobile_number("call 0612345678 tonight") == ["0612345678"]
    # La Réunion, Mayotte, Guadeloupe
    assert rre.fr.mobile_number("+262 692 12 34 56") == ["+262 692 12 34 56"]
    assert rre.fr.mobile_number("« 0639 20 12 34 »") == ["0639 20 12 34"]
    assert rre.fr.mobile_number("00590 690 20 12 34") == ["00590 690 20 12 34"]
    for text in (
        "06 12 34 56 7",  # nine digits
        "06 12 34 56 789",  # eleven
        "06 12.34 56 78",  # mixed separators
        "+33 1 99 00 12 34",  # landline
        "+32 470 12 34 56",  # Belgian
        "0612345678901",  # inside a longer number
        "2024-06-12-34-56-78",  # a date and time
        "06-12-34-56-78-90",  # a longer chain of pairs
    ):
        assert rre.fr.mobile_number(text) == [], text


def test_hard_mrz_id_card():
    new = "IDFRAX4RTBPFW46<<<<<<<<<<<<<<<"
    other = "IDFRAAB12CD34E4<<<<<<<<<<<<<<<"
    old = "9912751234566JEAN<<<<<<<<<<8001014M7"
    assert rre.fr.mrz_id_card(other) == [other]
    assert rre.fr.mrz_id_card("I<FRAX4RTBPFW46<<<<<<<<<<<<<<<") == ["I<FRAX4RTBPFW46<<<<<<<<<<<<<<<"]
    assert rre.fr.mrz_id_card(f"MRZ : {new} (ligne 1)") == [new]
    assert rre.fr.mrz_id_card(f"IDFRAMARTIN<<<<<<<<<<<<<<<<<<<<<<<<<\n{old}\n") == [old]
    assert rre.fr.mrz_id_card(f"the old card's second line {old}.") == [old]
    assert rre.fr.mrz_id_card(f"{new}\n{other}") == [new, other]
    for text in (
        other.replace("E4<", "E5<"),  # wrong check digit
        new[:-1],  # 29 characters
        new + "<",  # 31
        new.replace("IDFRA", "IDBEL"),  # Belgian
        new.lower(),  # lower case
        "P<FRAMARTIN<<MAELYS<<<<<<<<<<",  # a passport's first line
        old.replace("123456", "123457"),  # card number no longer matches its check
        old[1:],  # 35 characters
    ):
        assert rre.fr.mrz_id_card(text) == [], text


def test_hard_mrz_passport():
    a = "12AB345673FRA8501019M3001019<<<<<<<<<<<<<<<6"
    b = "18CD123457FRA9212314F3106154<<<<<<<<<<<<<<<2"
    specimen = "L898902C36FRA7408122F1204159ZE184226B<<<<<10"
    assert rre.fr.mrz_passport(a) == [a]
    assert rre.fr.mrz_passport(f"P<FRAMARTIN<<MAELYS<<<<<<<<<<<<<<<<<<<<<<<<<\n{b}") == [b]
    assert rre.fr.mrz_passport(f"({specimen})") == [specimen]
    assert rre.fr.mrz_passport(f"line 2: {a}.") == [a]
    assert rre.fr.mrz_passport(a.replace("9M", "9<")) == [a.replace("9M", "9<")]  # sex not given
    assert rre.fr.mrz_passport(f"{a} {b}") == [a, b]
    for text in (
        a.replace("673F", "674F"),  # wrong document number check
        a.replace("019M", "018M"),  # wrong birth date check
        a.replace("1019<", "1018<"),  # wrong expiry check
        a.replace("FRA", "GBR"),  # British
        a[:-1],  # 43 characters
        a + "0",  # 45
        a.replace("AB", "ab"),  # lower case
    ):
        assert rre.fr.mrz_passport(text) == [], text


def test_hard_msisdn():
    assert rre.fr.msisdn("msisdn=33753123456;") == ["33753123456"]
    assert rre.fr.msisdn("(262692123456)") == ["262692123456"]
    assert rre.fr.msisdn("Mayotte 262639201234.") == ["262639201234"]
    assert rre.fr.msisdn("Guadeloupe 590690201234") == ["590690201234"]
    assert rre.fr.msisdn("CDR: 596696201234, 33612345678") == ["596696201234", "33612345678"]
    assert rre.fr.msisdn("33612345678") == ["33612345678"]
    for text in (
        "+33612345678",  # international format, a phone number
        "0033612345678",  # with 00
        "3361234567",  # ten digits
        "336123456789",  # twelve
        "33 6 12 34 56 78",  # spaced
        "32470123456",  # Belgian
    ):
        assert rre.fr.msisdn(text) == [], text


def test_hard_nir():
    assert rre.fr.nir("NIR : 2 85 10 99 123 456 37.") == ["2 85 10 99 123 456 37"]  # born abroad
    assert rre.fr.nir("(169017512345617)") == ["169017512345617"]
    assert rre.fr.nir("n° sécu 1 72 01 97 112 345 08") == ["1 72 01 97 112 345 08"]
    assert rre.fr.nir("« 2 93 09 99 123 456 17 »") == ["2 93 09 99 123 456 17"]
    assert rre.fr.nir("social security number 1 69 01 75 123 456 17 on file") == ["1 69 01 75 123 456 17"]
    assert rre.fr.nir("NIA 8 90 12 99 001 001 50") == ["8 90 12 99 001 001 50"]
    for text in (
        "2 85 10 99 123 456 38",  # wrong key
        "18507750000008",  # 14 digits
        "1850775000000801",  # 16
        "2 75 05 2C 000 000 60",  # no Corsica 2C
        "1-85-07-75-000-000-80",  # dashes
        "X185077500000080",  # inside a longer token
        "4 85 07 75 000 000 80",  # starts with 4
    ):
        assert rre.fr.nir(text) == [], text


def test_hard_numero_fiscal():
    assert rre.fr.numero_fiscal("12 34 567 890 066") == ["12 34 567 890 066"]
    assert rre.fr.numero_fiscal("1234567890066") == ["1234567890066"]
    assert rre.fr.numero_fiscal("(0123456789211)") == ["0123456789211"]
    assert rre.fr.numero_fiscal("numéro fiscal : 29 99 999 999 248.") == ["29 99 999 999 248"]
    assert rre.fr.numero_fiscal("tax number 0123456789211 on the form") == ["0123456789211"]
    assert rre.fr.numero_fiscal("« 30 23 217 600 053 »") == ["30 23 217 600 053"]
    for text in (
        "12 34 567 890 067",  # wrong check
        "123456789006",  # twelve digits
        "12345678900660",  # fourteen
        "12-34-567-890-066",  # dashes
        "X1234567890066",  # inside a longer token
        "5234567890066",  # starts with 5
    ):
        assert rre.fr.numero_fiscal(text) == [], text


def test_hard_passport_number():
    assert rre.fr.passport_number("12AB34567") == ["12AB34567"]
    assert rre.fr.passport_number("passeport n° 18CD12345.") == ["18CD12345"]
    assert rre.fr.passport_number("(99XY88888)") == ["99XY88888"]
    assert rre.fr.passport_number("« 07FR12345 »") == ["07FR12345"]
    assert rre.fr.passport_number("passport 21ZZ54321, issued in Lyon") == ["21ZZ54321"]
    assert rre.fr.passport_number("12AB34567/18CD12345") == ["12AB34567", "18CD12345"]
    for text in (
        "123AB4567",  # three digits first
        "12ABC4567",  # three letters
        "12ab34567",  # lower case
        "X12AB34567",  # inside a longer token
        "12AB345678",  # ten characters
        "12-AB-34567",  # dashes
    ):
        assert rre.fr.passport_number(text) == [], text


def test_hard_phone_number():
    assert rre.fr.phone_number("+33 1 99 00 12 34") == ["+33 1 99 00 12 34"]
    assert rre.fr.phone_number("0033 4 65 71 12 34") == ["0033 4 65 71 12 34"]
    assert rre.fr.phone_number("(01 99 00 12 34)") == ["01 99 00 12 34"]
    assert rre.fr.phone_number("Tél. : 04-65-71-12-34.") == ["04-65-71-12-34"]
    assert rre.fr.phone_number("call +33199001234 now") == ["+33199001234"]
    # Guadeloupe and La Réunion
    assert rre.fr.phone_number("« 0590 12 34 56 »") == ["0590 12 34 56"]
    assert rre.fr.phone_number("+262 262 12 34 56") == ["+262 262 12 34 56"]
    for text in (
        "01 99 00 12 345",  # eleven digits
        "01 99.00 12 34",  # mixed separators
        "+32 2 555 12 12",  # Belgian
        "00 12 34 56 78",  # 00 is no area
        "Screenshot_2026-03-02-08-15-12-123.jpg",  # a date and time
        "10.01.23.45.67.89",  # a longer chain of numbers
        "le 01/02/2024",  # a date
    ):
        assert rre.fr.phone_number(text) == [], text


def test_hard_postal_code_city():
    assert rre.fr.postal_code_city("59650 Villeneuve d'Ascq") == ["59650 Villeneuve d'Ascq"]
    assert rre.fr.postal_code_city("64500 Saint Jean de Luz") == ["64500 Saint Jean de Luz"]
    assert rre.fr.postal_code_city("(97200 Fort-de-France)") == ["97200 Fort-de-France"]
    assert rre.fr.postal_code_city("F-67000 Strasbourg") == ["67000 Strasbourg"]
    assert rre.fr.postal_code_city("69370 ST DIDIER AU MONT D OR") == ["69370 ST DIDIER AU MONT D OR"]
    assert rre.fr.postal_code_city("sent to 20000 Ajaccio, Corsica") == ["20000 Ajaccio"]
    # the town ends with its line
    assert rre.fr.postal_code_city("12 rue de la Paix\n75002 Paris\nFrance") == ["75002 Paris"]
    for text in (
        "15000 USD",  # an amount
        "15000 Euros",
        "75001 paris",  # town in lower case
        "96000 Ville",  # no department 96
        "750 Paris",  # three digits
        "750081 Paris",  # six digits
        "22222-33333-44444-66666-77777 ABCDE",  # last group of a product key
        "RIB 11111 22222 ABCDEFGHIJK 96",  # bank and branch codes of a RIB
    ):
        assert rre.fr.postal_code_city(text) == [], text


def test_hard_rib():
    assert rre.fr.rib("RIB : 20041 01005 0500013M026 06.") == ["20041 01005 0500013M026 06"]
    assert rre.fr.rib("(11111 22222 ABCDEFGHIJK 96)") == ["11111 22222 ABCDEFGHIJK 96"]
    assert rre.fr.rib("bank details 10107 00175 00012345678 40 attached") == ["10107 00175 00012345678 40"]
    assert rre.fr.rib("12345678901234567890104") == ["12345678901234567890104"]
    assert rre.fr.rib("« 12345 67890 12345678901 04 »") == ["12345 67890 12345678901 04"]
    assert rre.fr.rib("20041010050500013M02606/30006000011234567890189") == [
        "20041010050500013M02606", "30006000011234567890189"]
    for text in (
        "12345 67890 12345678901 05",  # wrong key
        "12345 67890 1234567890 04",  # ten-character account
        "12345 67890 123456789012 04",  # twelve
        "11111 22222 abcdefghijk 96",  # lower case letters
        "30006-00001-12345678901-89",  # dashes
        "X30006000011234567890189",  # inside a longer token
        "FR7630006000011234567890189",  # inside an IBAN
    ):
        assert rre.fr.rib(text) == [], text


def test_hard_siren():
    assert rre.fr.siren("SIREN : 123 456 782.") == ["SIREN : 123 456 782"]
    assert rre.fr.siren("R.C.S. Nanterre 123 456 782") == ["R.C.S. Nanterre 123 456 782"]
    assert rre.fr.siren("(RCS Lyon B 987 654 324)") == ["RCS Lyon B 987 654 324"]
    assert rre.fr.siren("123 456 782 R.C.S. Paris") == ["123 456 782 R.C.S."]
    assert rre.fr.siren("registered under SIREN 111222337 in Lille") == ["SIREN 111222337"]
    assert rre.fr.siren("RCS de Bordeaux 909 090 904") == ["RCS de Bordeaux 909 090 904"]
    for text in (
        "SIREN 123 456 783",  # fails Luhn
        "SIREN 12345678",  # eight digits
        "SIREN 1234567820",  # ten
        "XSIREN 123456782",  # keyword inside a longer word
        "SIRET 123456782",  # another keyword
        "TVA 123 456 782",  # another keyword
    ):
        assert rre.fr.siren(text) == [], text


def test_hard_siret():
    assert rre.fr.siret("SIRET : 123 456 782 00010") == ["SIRET : 123 456 782 00010"]
    assert rre.fr.siret("(123 456 782 00028)") == ["123 456 782 00028"]
    assert rre.fr.siret("Siret n° 12345678200101.") == ["Siret n° 12345678200101"]
    assert rre.fr.siret("establishment 123456782 00010 in Lyon") == ["123456782 00010"]
    assert rre.fr.siret("« SIRET: 12345678212346 »") == ["SIRET: 12345678212346"]
    assert rre.fr.siret("siret 12345678200010/12345678200028") == ["siret 12345678200010"]
    for text in (
        "SIRET 123 456 782 00011",  # fails Luhn
        "SIRET 123 456 783 00000",  # Luhn over all 14 digits, not over the SIREN
        "SIRET 123 456 782 0001",  # 13 digits
        "SIRET 123 456 782 000100",  # 15
        "123 456 782 0001",  # four-digit establishment number
        "1234 5678 2000 10",  # card-like grouping
        "X123456782 00010",  # inside a longer token
    ):
        assert rre.fr.siret(text) == [], text


def test_hard_street_address():
    assert rre.fr.street_address("« 7 impasse des Lilas »") == ["7 impasse des Lilas"]
    assert rre.fr.street_address("(15 ter avenue Jean Jaurès)") == ["15 ter avenue Jean Jaurès"]
    assert rre.fr.street_address("1 place Bellecour, Lyon") == ["1 place Bellecour"]
    assert rre.fr.street_address("40 quai d'Orsay") == ["40 quai d'Orsay"]
    assert rre.fr.street_address("he lives at 3 rue du 11 Novembre now") == ["3 rue du 11 Novembre"]
    assert rre.fr.street_address("20 BD SAINT-GERMAIN") == ["20 BD SAINT-GERMAIN"]
    # the street ends with its line, and the town after à is not part of it
    assert rre.fr.street_address("12 rue de la Paix\nParis") == ["12 rue de la Paix"]
    assert rre.fr.street_address("au 5 avenue de la Liberté à Paris") == ["5 avenue de la Liberté"]
    for text in (
        "12 rue",  # no name
        "rue de la Paix",  # no number
        "12345 rue de la Paix",  # five-digit number
        "12 rues de Paris",  # plural
        "12 rue de la paix",  # name in lower case
        "12 Street Paris",  # English street type
    ):
        assert rre.fr.street_address(text) == [], text


def test_hard_vat_number():
    assert rre.fr.vat_number("FR14987654324") == ["FR14987654324"]
    assert rre.fr.vat_number("TVA intracom : FR 21 111 222 337.") == ["FR 21 111 222 337"]
    assert rre.fr.vat_number("(FRK7399859412)") == ["FRK7399859412"]
    assert rre.fr.vat_number("VAT FR09 404040404 on the invoice") == ["FR09 404040404"]
    assert rre.fr.vat_number("« FR 27 552 120 222 »") == ["FR 27 552 120 222"]
    assert rre.fr.vat_number("FR14987654324/FR09404040404") == ["FR14987654324", "FR09404040404"]
    for text in (
        "FR15987654324",  # wrong key
        "FR14987654325",  # SIREN fails Luhn
        "FR1498765432",  # eight-digit SIREN
        "FR149876543240",  # ten digits
        "BE0123456749",  # Belgian
        "fr14987654324",  # lower case
        "XFR14987654324",  # inside a longer token
    ):
        assert rre.fr.vat_number(text) == [], text
