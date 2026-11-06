from regular_regexes import rre


def test_national_number():
    assert rre.lu.national_number("matricule 1983 0819 012 52 et 1983081901252") == [
        "1983 0819 012 52", "1983081901252"]
    assert rre.lu.national_number("jour inconnu: 1983 0800 123 10") == ["1983 0800 123 10"]
    assert rre.lu.national_number("2000 0229 007 62") == ["2000 0229 007 62"]
    assert rre.lu.national_number("1983081901253") == []  # check digit changed
    # check digits right, but 30 February and 29 February 1900 don't exist
    assert rre.lu.national_number("1983 0230 123 12 1900 0229 007 94") == []


def test_vat_number():
    assert rre.lu.vat_number("TVA LU 123 456 13 et LU12345613") == ["LU 123 456 13", "LU12345613"]
    assert rre.lu.vat_number("LU12345614") == []


def test_rcs_number():
    assert rre.lu.rcs_number("Lux Invest S.à r.l., R.C.S. Luxembourg B 123.456") == ["R.C.S. Luxembourg B 123.456"]
    assert rre.lu.rcs_number(
        "immatriculée au Registre de Commerce et des Sociétés de Luxembourg sous le numéro B 98765, RCS: F1234") == [
        "Registre de Commerce et des Sociétés de Luxembourg sous le numéro B 98765", "RCS: F1234"]
    assert rre.lu.rcs_number("numéro B 123456") == []  # no RCS context
    assert rre.lu.rcs_number("RCS Paris B 552 100 554") == []


def test_court_case_number():
    assert rre.lu.court_case_number("N° TAL-2021-01234 du rôle, appel CAL-2022-00567") == [
        "TAL-2021-01234", "CAL-2022-00567"]
    assert rre.lu.court_case_number("TAL-21-01234") == []


def test_iban():
    # example from the SWIFT IBAN registry
    assert rre.lu.iban("virement sur LU28 0019 4006 4475 0000 svp") == ["LU28 0019 4006 4475 0000"]
    assert rre.lu.iban("LU280019400644750001") == []


def test_bic():
    assert rre.lu.bic("BIC BCEELULL ou BILLLULLXXX") == ["BCEELULL", "BILLLULLXXX"]
    assert rre.lu.bic("GEBABEBB") == []


def test_passport_number():
    # numbers from the PRADO specimens
    assert rre.lu.passport_number("son passeport n° JC3L7T2H, Pass-Nr. LCNTVUT2") == ["JC3L7T2H", "LCNTVUT2"]
    assert rre.lu.passport_number("N° du passeport: G2A0312") == ["G2A0312"]
    assert rre.lu.passport_number("passport LUXEMBOURG, boarding pass 12345678") == []


def test_id_card_number():
    # numbers from the PRADO specimens
    assert rre.lu.id_card_number("N° carte d'identité 7D9IB9OLK et identity card no. SPEC07347") == [
        "7D9IB9OLK", "SPEC07347"]
    assert rre.lu.id_card_number("carte d'identité valable, Personalausweis 123456789") == []


def test_mrz_id_card():
    # PRADO specimens LUX-BO-03001 (2021) and LUX-BO-02005 (2014)
    lines = ["IDLUXSPEC073476210715<<<<<<<<<", "IDLUX7D9IB9OLK6140701<<<<<<<<<"]
    assert rre.lu.mrz_id_card("\n".join(lines)) == lines
    assert rre.lu.mrz_id_card("IDLUXSPEC073486210715<<<<<<<<<") == []


def test_mrz_passport():
    # PRADO specimens LUX-AO-04001, LUX-AO-02005 and LUX-AO-03001
    lines = [
        "LCNTVUT2<1LUX9106019F360415501260000053<<<16",
        "JC3L7T2H<4LUX9303092F200122901150000542<<<88",
        "G2A0312<<2LUX8806231F160616601110011397<<<88",
    ]
    assert rre.lu.mrz_passport("\n".join(lines)) == lines
    assert rre.lu.mrz_passport(lines[1].replace("9303092", "9303093")) == []


def test_phone_number():
    # libphonenumber's example numbers
    assert rre.lu.phone_number("tél +352 27 12 34 56 ou 00352 628 123 456") == ["+352 27 12 34 56", "00352 628 123 456"]
    assert rre.lu.phone_number("Tel. (+352) 27 12 34 56") == ["(+352) 27 12 34 56"]
    assert rre.lu.phone_number("+353 1 234 5678 et 352 82 12 34") == []


def test_mobile_number():
    assert rre.lu.mobile_number("gsm 628 123 456 ou +352 698 12 34 56") == ["628 123 456", "+352 698 12 34 56"]
    assert rre.lu.mobile_number("12 628 123 456 et 6281234567 et 26 12 34 56") == []


def test_msisdn():
    assert rre.lu.msisdn("msisdn 352628123456") == ["352628123456"]
    assert rre.lu.msisdn("35226123456") == []


def test_imsi():
    assert rre.lu.imsi("imsi 270011234567890") == ["270011234567890"]
    assert rre.lu.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.lu.iccid("sim 8935201123456789011") == ["8935201123456789011"]
    assert rre.lu.iccid("sim 8935201123456789012") == []


def test_license_plate():
    assert rre.lu.license_plate("voiture ZZ 1234 et ZZ1234") == ["ZZ 1234", "ZZ1234"]
    # a Swiss postal code, the end of a German plate, letters I and O are not used
    assert rre.lu.license_plate("CH-8000 Zürich, B-ZZ 1234, IO 1234") == []


def test_postal_code():
    assert rre.lu.postal_code("L-2449 Luxembourg") == ["L-2449"]
    assert rre.lu.postal_code("L-12345 et AL-1234") == []


def test_street_address():
    assert rre.lu.street_address("12, rue de la Gare, L-1234 Luxembourg") == ["12, rue de la Gare"]
    assert rre.lu.street_address("5 avenue de la Liberté à Esch et 12A, avenue J.F. Kennedy.") == [
        "5 avenue de la Liberté", "12A, avenue J.F. Kennedy"]
    assert rre.lu.street_address("3, Haaptstrooss, Kierchestrooss 7 et 7, Grand-Rue") == [
        "3, Haaptstrooss", "Kierchestrooss 7", "7, Grand-Rue"]
    assert rre.lu.street_address("3 places libres sur la route") == []


def test_company_name():
    assert rre.lu.company_name("contrat entre Lux Invest S.à r.l. et Beta Holding S.A. SPF") == [
        "Lux Invest S.à r.l.", "Beta Holding S.A. SPF"]
    assert rre.lu.company_name("Gamma Fund SICAV-RAIF et Delta Partners SCSp") == [
        "Gamma Fund SICAV-RAIF", "Delta Partners SCSp"]
    assert rre.lu.company_name("la sàrl de Jean") == []


def test_aircraft_registration():
    assert rre.lu.aircraft_registration("avion LX-ABC et LX-N90442") == ["LX-ABC", "LX-N90442"]
    assert rre.lu.aircraft_registration("LX-AB et vol LX 1234") == []


# Hardened tests: every regex gets at least six written forms that match and six near misses that don't. Apart from
# the PRADO specimens, the numbers below are made up in the right shape, with valid check digits where there are any.


def test_hard_aircraft_registration():
    assert rre.lu.aircraft_registration("LX-QZX") == ["LX-QZX"]
    assert rre.lu.aircraft_registration("avion (LX-ZZQ)") == ["LX-ZZQ"]
    assert rre.lu.aircraft_registration("immatriculation 'LX-QXV'.") == ["LX-QXV"]
    assert rre.lu.aircraft_registration("AWACS LX-N90443 au-dessus") == ["LX-N90443"]
    assert rre.lu.aircraft_registration("LXQZA ohne Bindestrich") == ["LXQZA"]
    assert rre.lu.aircraft_registration("reg:LX-ZQZ,") == ["LX-ZQZ"]
    assert rre.lu.aircraft_registration("LX-QZ") == []  # too short
    assert rre.lu.aircraft_registration("LX-QZXA") == []  # too long
    assert rre.lu.aircraft_registration("LX-N9044") == []  # four digits
    assert rre.lu.aircraft_registration("LX-N904421") == []  # six
    assert rre.lu.aircraft_registration("lx-qzx") == []
    assert rre.lu.aircraft_registration("LUX-QZX") == []
    assert rre.lu.aircraft_registration("OO-QZX") == []  # Belgian


def test_hard_bic():
    assert rre.lu.bic("(BIC: ABCDLULL)") == ["ABCDLULL"]
    assert rre.lu.bic("SWIFT/BIC ZYXWLU2X.") == ["ZYXWLU2X"]
    assert rre.lu.bic("QWERLULLXXX") == ["QWERLULLXXX"]
    assert rre.lu.bic("bic=ABCDLU22;") == ["ABCDLU22"]
    assert rre.lu.bic("'ABCDLULL123'") == ["ABCDLULL123"]
    assert rre.lu.bic("BIC-Code QWERLU2L der Bank") == ["QWERLU2L"]
    assert rre.lu.bic("ABCDLUL") == []  # seven characters
    assert rre.lu.bic("ABCDLULLX") == []  # nine
    assert rre.lu.bic("ABCDLULLXXXX") == []  # twelve
    assert rre.lu.bic("ABC1LULL") == []  # a digit in the bank code
    assert rre.lu.bic("ABCDBELL") == []  # Belgian
    assert rre.lu.bic("XABCDLULL") == []
    assert rre.lu.bic("LU28 0019 4006 4475 0000") == []  # an IBAN


def test_hard_company_name():
    assert rre.lu.company_name("Epsilon SARL-S") == ["Epsilon SARL-S"]
    assert rre.lu.company_name("bail avec Zeta Immo SCI") == ["Zeta Immo SCI"]
    assert rre.lu.company_name("Omega Capital SE, Kappa S.e.n.c.") == ["Omega Capital SE", "Kappa S.e.n.c."]
    assert rre.lu.company_name("(Sigma Real Estate S.à r.l.)") == ["Sigma Real Estate S.à r.l."]
    assert rre.lu.company_name("« Rho Ventures S.A. »") == ["Rho Ventures S.A."]
    assert rre.lu.company_name("Theta S.A.R.L. et Lambda SCA") == ["Theta S.A.R.L.", "Lambda SCA"]
    # de, du, la, d' in the name
    assert rre.lu.company_name("Les Amis du Vin ASBL") == ["Amis du Vin ASBL"]
    assert rre.lu.company_name("Café d'Europe SàRL et Pierre de la Fontaine S.A.") == [
        "Café d'Europe SàRL", "Pierre de la Fontaine S.A."]
    # an article or possessive alone is no name
    assert rre.lu.company_name("Le S.A. de Jean") == []
    assert rre.lu.company_name("La SARL a déménagé") == []
    assert rre.lu.company_name("Une SA de droit luxembourgeois") == []
    assert rre.lu.company_name("Cette SICAV est fermée") == []
    assert rre.lu.company_name("Notre ASBL organise") == []
    assert rre.lu.company_name("Die SE wurde gegründet") == []
    assert rre.lu.company_name("Jean S A") == []  # S A without dots
    assert rre.lu.company_name("AlphaSA") == []


def test_hard_court_case_number():
    assert rre.lu.court_case_number("TAD-2020-00123") == ["TAD-2020-00123"]
    assert rre.lu.court_case_number("(TAL-2019-12345)") == ["TAL-2019-12345"]
    assert rre.lu.court_case_number("n° CAL-2023-00001.") == ["CAL-2023-00001"]
    assert rre.lu.court_case_number("rôle:TAL-2024-00042,") == ["TAL-2024-00042"]
    assert rre.lu.court_case_number("'CAL-1999-98765'") == ["CAL-1999-98765"]
    assert rre.lu.court_case_number("Az. TAD-2021-04567 vom 3. März") == ["TAD-2021-04567"]
    assert rre.lu.court_case_number("TAL-2021-1234") == []  # four digits
    assert rre.lu.court_case_number("TAL-2021-012345") == []  # six
    assert rre.lu.court_case_number("TAX-2021-01234") == []  # no such court
    assert rre.lu.court_case_number("TAL-1821-01234") == []
    assert rre.lu.court_case_number("XTAL-2021-01234") == []
    assert rre.lu.court_case_number("tal-2021-01234") == []
    assert rre.lu.court_case_number("TAL 2021 01234") == []


def test_hard_iban():
    assert rre.lu.iban("LU390010001234567890") == ["LU390010001234567890"]
    assert rre.lu.iban("IBAN: LU72 0141 2345 6789 0123.") == ["LU72 0141 2345 6789 0123"]
    assert rre.lu.iban("(LU2800190000000123AB)") == ["LU2800190000000123AB"]
    assert rre.lu.iban("LU58 0030 1234 5678 9012 au nom de") == ["LU58 0030 1234 5678 9012"]
    assert rre.lu.iban("Konto:LU39 0010 0012 3456 7890") == ["LU39 0010 0012 3456 7890"]
    assert rre.lu.iban("'LU720141234567890123'") == ["LU720141234567890123"]
    assert rre.lu.iban("LU28 0019 4006 4475 000") == []  # one character short
    assert rre.lu.iban("LU2800194006447500001") == []  # one too many
    assert rre.lu.iban("LU28-0019-4006-4475-0000") == []
    assert rre.lu.iban("XLU280019400644750000") == []
    assert rre.lu.iban("LU39 0010 0012 3456 7891") == []  # check digits fail
    assert rre.lu.iban("BE68 5390 0754 7034") == []


def test_hard_iccid():
    assert rre.lu.iccid("ICCID 893520100000123452") == ["893520100000123452"]  # 18 digits
    assert rre.lu.iccid("(8935201000001234562)") == ["8935201000001234562"]  # 19
    assert rre.lu.iccid("iccid: 89352770123456789012.") == ["89352770123456789012"]  # 20
    assert rre.lu.iccid("8935299123456789014") == ["8935299123456789014"]
    assert rre.lu.iccid("sim=8935201000001234562;") == ["8935201000001234562"]
    assert rre.lu.iccid("'893520100000123452'") == ["893520100000123452"]
    assert rre.lu.iccid("8935201000001234") == []  # 16 digits
    assert rre.lu.iccid("893520100000123456789") == []  # 21
    assert rre.lu.iccid("8935 2011 2345 6789 011") == []
    assert rre.lu.iccid("89310412345678901230") == []  # Dutch
    assert rre.lu.iccid("x8935201123456789011") == []
    assert rre.lu.iccid("893520100000123453") == []  # Luhn fails


def test_hard_id_card_number():
    assert rre.lu.id_card_number("K8X2M4P7Q") == ["K8X2M4P7Q"]
    assert rre.lu.id_card_number("(SPEC07347)") == ["SPEC07347"]
    assert rre.lu.id_card_number("carte n° '7D9IB9OLK'.") == ["7D9IB9OLK"]
    assert rre.lu.id_card_number("Ausweis-Nr. X1Y2Z3W4V") == ["X1Y2Z3W4V"]
    assert rre.lu.id_card_number("ID:Q7W8E9R0T,") == ["Q7W8E9R0T"]
    assert rre.lu.id_card_number("Nummer P3K9Z2M8X op de kaart") == ["P3K9Z2M8X"]
    assert rre.lu.id_card_number("SPEC0734") == []  # eight characters
    assert rre.lu.id_card_number("SPEC073471") == []  # ten
    assert rre.lu.id_card_number("123456789") == []  # digits only
    assert rre.lu.id_card_number("ABCDEFGHI") == []  # letters only
    assert rre.lu.id_card_number("spec07347") == []
    assert rre.lu.id_card_number("SPEC-07347") == []


def test_hard_imsi():
    assert rre.lu.imsi("IMSI: 270771234567890.") == ["270771234567890"]
    assert rre.lu.imsi("(270991234567890)") == ["270991234567890"]
    assert rre.lu.imsi("imsi=270011234567890;") == ["270011234567890"]
    assert rre.lu.imsi("270781234567890 est l'IMSI") == ["270781234567890"]
    assert rre.lu.imsi("'270021234567890'") == ["270021234567890"]
    assert rre.lu.imsi("IMSI 270 01 1234567890") == []  # not written with spaces
    assert rre.lu.imsi("27001123456789") == []  # 14 digits
    assert rre.lu.imsi("2700112345678901") == []  # 16
    assert rre.lu.imsi("A270011234567890") == []
    assert rre.lu.imsi("0270011234567890") == []
    assert rre.lu.imsi("270-01-1234567890") == []
    assert rre.lu.imsi("208011234567890") == []  # French


def test_hard_license_plate():
    assert rre.lu.license_plate("AB 1234") == ["AB 1234"]
    assert rre.lu.license_plate("(XY 9876)") == ["XY 9876"]
    assert rre.lu.license_plate("immatriculée ZZ 0001 au Luxembourg.") == ["ZZ 0001"]
    assert rre.lu.license_plate('"TZ 4567"') == ["TZ 4567"]
    assert rre.lu.license_plate("Kennzeichen:KM5678") == ["KM5678"]
    assert rre.lu.license_plate("GH 4321 und PR 1111") == ["GH 4321", "PR 1111"]
    assert rre.lu.license_plate("ZZ 123") == []  # three digits
    assert rre.lu.license_plate("ZZ 12345") == []  # five
    assert rre.lu.license_plate("ZZZ 1234") == []
    assert rre.lu.license_plate("AI 1234") == []  # no I or O
    assert rre.lu.license_plate("M-AB 1234") == []  # a German plate
    assert rre.lu.license_plate("B ZZ 1234") == []
    assert rre.lu.license_plate("zz 1234") == []
    assert rre.lu.license_plate("ZZ-1234") == []


def test_hard_mobile_number():
    assert rre.lu.mobile_number("00352 621 123 456") == ["00352 621 123 456"]
    assert rre.lu.mobile_number("(+352) 661 123 456") == ["(+352) 661 123 456"]
    assert rre.lu.mobile_number("691123456") == ["691123456"]
    assert rre.lu.mobile_number("+352.671.123.456") == ["+352.671.123.456"]
    assert rre.lu.mobile_number("GSM: 691/12 34 56.") == ["691/12 34 56"]
    assert rre.lu.mobile_number("Handy +352-655-123-456") == ["+352-655-123-456"]
    assert rre.lu.mobile_number("628 123 45") == []  # one digit short
    assert rre.lu.mobile_number("628 123 4567") == []  # one too many
    assert rre.lu.mobile_number("+352 27 12 34 56") == []  # a landline
    assert rre.lu.mobile_number("+353 628 123 456") == []  # Irish prefix
    assert rre.lu.mobile_number("0628 123 456") == []
    assert rre.lu.mobile_number("638 123 456") == []  # no such range
    assert rre.lu.mobile_number("628.123.456.7") == []


def test_hard_mrz_id_card():
    assert rre.lu.mrz_id_card("IDLUXK8X2M4P7Q3<<<<<<<<<<<<<<<") == ["IDLUXK8X2M4P7Q3<<<<<<<<<<<<<<<"]
    assert rre.lu.mrz_id_card("MRZ: IRLUXAB12345671<<<<<<<<<<<<<<<.") == ["IRLUXAB12345671<<<<<<<<<<<<<<<"]
    assert rre.lu.mrz_id_card("'IDLUXSPEC073476<<<<<<<<<<<<<<<'") == ["IDLUXSPEC073476<<<<<<<<<<<<<<<"]
    assert rre.lu.mrz_id_card("IDLUXK8X2M4P7Q3<<<<<<<<<<<<<<<\n9001011M3001019LUX<<<<<<<<<<<6") == [
        "IDLUXK8X2M4P7Q3<<<<<<<<<<<<<<<"]
    assert rre.lu.mrz_id_card("zone IDLUX7D9IB9OLK6140701<<<<<<<<<") == ["IDLUX7D9IB9OLK6140701<<<<<<<<<"]
    assert rre.lu.mrz_id_card("I<LUXK8X2M4P7Q3<<<<<<<<<<<<<<<") == ["I<LUXK8X2M4P7Q3<<<<<<<<<<<<<<<"]
    assert rre.lu.mrz_id_card("IDLUXK8X2M4P7Q4<<<<<<<<<<<<<<<") == []  # check digit
    assert rre.lu.mrz_id_card("IDBELK8X2M4P7Q3<<<<<<<<<<<<<<<") == []  # Belgian
    assert rre.lu.mrz_id_card("IDLUXK8X2M4P7Q3<<<<<<<<<<<<<<") == []  # 29 characters
    assert rre.lu.mrz_id_card("IDLUXK8X2M4P7Q3<<<<<<<<<<<<<<<<") == []  # 31
    assert rre.lu.mrz_id_card("PDLUXK8X2M4P7Q3<<<<<<<<<<<<<<<") == []  # a passport's type
    assert rre.lu.mrz_id_card("idluxk8x2m4p7q3<<<<<<<<<<<<<<<") == []


def test_hard_mrz_passport():
    lines = [
        "KB7Z3M2P<5LUX9001011M3001019<<<<<<<<<<<<<<<6",
        "LX12345<<9LUX7512249F2512244<<<<<<<<<<<<<<<0",
        "ZZ9Y8X7W<9LUX0202022X3202023<<<<<<<<<<<<<<<8",
    ]
    assert rre.lu.mrz_passport(lines[0]) == [lines[0]]
    assert rre.lu.mrz_passport(f"MRZ: {lines[1]}.") == [lines[1]]
    assert rre.lu.mrz_passport(f"'{lines[2]}'") == [lines[2]]
    assert rre.lu.mrz_passport("P<LUXMUSTER<<ANNA<<<<<<<<<<<<<<<<<<<<<<<<<<<\n" + lines[0]) == [lines[0]]
    assert rre.lu.mrz_passport("\n".join(lines[1:])) == lines[1:]
    assert rre.lu.mrz_passport(lines[2] + "\n") == [lines[2]]
    assert rre.lu.mrz_passport(lines[0].replace("<5LUX", "<6LUX")) == []  # document number check digit
    assert rre.lu.mrz_passport(lines[0].replace("9001011", "9001012")) == []  # birth date check digit
    assert rre.lu.mrz_passport(lines[0].replace("3001019", "3001018")) == []  # expiry date check digit
    assert rre.lu.mrz_passport(lines[1].replace("LUX", "BEL")) == []
    assert rre.lu.mrz_passport(lines[1][:-1]) == []  # 43 characters
    assert rre.lu.mrz_passport(lines[1] + "<") == []  # 45


def test_hard_msisdn():
    assert rre.lu.msisdn("MSISDN: 352621123456.") == ["352621123456"]
    assert rre.lu.msisdn("(352661123456)") == ["352661123456"]
    assert rre.lu.msisdn("msisdn=352691123456;") == ["352691123456"]
    assert rre.lu.msisdn("352671123456,352698123456") == ["352671123456", "352698123456"]
    assert rre.lu.msisdn("'352655123456'") == ["352655123456"]
    assert rre.lu.msisdn("a_party 352628654321 b_party") == ["352628654321"]
    assert rre.lu.msisdn("35262812345") == []  # eleven digits
    assert rre.lu.msisdn("3526281234567") == []  # thirteen
    assert rre.lu.msisdn("0352628123456") == []
    assert rre.lu.msisdn("352638123456") == []  # no such range
    assert rre.lu.msisdn("x352628123456") == []
    assert rre.lu.msisdn("+352628123456") == []  # international format: mobile_number finds it
    assert rre.lu.msisdn("32628123456") == []


def test_hard_national_number():
    assert rre.lu.national_number("matricule: 1975 0314 100 86") == ["1975 0314 100 86"]
    assert rre.lu.national_number("(1990123110078)") == ["1990123110078"]
    assert rre.lu.national_number("2004.07.01.100.23") == ["2004.07.01.100.23"]
    assert rre.lu.national_number("Sozialversicherungsnummer 1961-0000-100-38") == ["1961-0000-100-38"]
    assert rre.lu.national_number("né le 28/02/1999, matricule 1999 02 28 100 53.") == ["1999 02 28 100 53"]
    assert rre.lu.national_number("'2012110510027'") == ["2012110510027"]
    assert rre.lu.national_number("198308190125") == []  # twelve digits
    assert rre.lu.national_number("19830819012521") == []  # fourteen
    assert rre.lu.national_number("1983 1319 012 52") == []  # month 13
    assert rre.lu.national_number("1883 0819 012 52") == []
    assert rre.lu.national_number("1975031410096") == []  # Luhn digit wrong
    assert rre.lu.national_number("1975031410087") == []  # Verhoeff digit wrong
    assert rre.lu.national_number("1983/08/19/012/52") == []


def test_hard_passport_number():
    assert rre.lu.passport_number("KB7Z3M2P") == ["KB7Z3M2P"]
    assert rre.lu.passport_number("(LX12345)") == ["LX12345"]
    assert rre.lu.passport_number("passeport n°: 'ZZ9Y8X7W'.") == ["ZZ9Y8X7W"]
    assert rre.lu.passport_number("Reisepass Q2W3E4R5 gültig") == ["Q2W3E4R5"]
    assert rre.lu.passport_number("pass=P9Z8Y7X;") == ["P9Z8Y7X"]
    assert rre.lu.passport_number("Pass-Nr.:M4N5B6V7") == ["M4N5B6V7"]
    assert rre.lu.passport_number("LX1234") == []  # six characters
    assert rre.lu.passport_number("LX1234567") == []  # nine
    assert rre.lu.passport_number("12345678") == []  # digits only
    assert rre.lu.passport_number("PASSPORT") == []  # letters only
    assert rre.lu.passport_number("kb7z3m2p") == []
    assert rre.lu.passport_number("KB7Z-3M2P") == []


def test_hard_phone_number():
    assert rre.lu.phone_number("+352 4796 1") == ["+352 4796 1"]
    assert rre.lu.phone_number("+352.26.12.34.56") == ["+352.26.12.34.56"]
    assert rre.lu.phone_number("+352/27 12 34 56") == ["+352/27 12 34 56"]
    assert rre.lu.phone_number("+35227123456") == ["+35227123456"]
    assert rre.lu.phone_number("Tél.: 00352-42-42-42.") == ["00352-42-42-42"]
    assert rre.lu.phone_number("gratuit (+352) 8002 1234") == ["(+352) 8002 1234"]
    assert rre.lu.phone_number("+352 0 27 12 34 56") == []
    assert rre.lu.phone_number("+352 27") == []  # too short
    assert rre.lu.phone_number("+3522712345678901") == []  # too long
    assert rre.lu.phone_number("352 27 12 34 56") == []  # no + or 00
    assert rre.lu.phone_number("+32 2 123 45 67") == []  # Belgian
    assert rre.lu.phone_number("00353 1 234 5678") == []  # Irish
    assert rre.lu.phone_number("+352 12 34") == []  # no such number


def test_hard_postal_code():
    assert rre.lu.postal_code("L-1234 Luxembourg") == ["L-1234"]
    assert rre.lu.postal_code("(L-4002 Esch-sur-Alzette)") == ["L-4002"]
    assert rre.lu.postal_code("L-9999") == ["L-9999"]
    assert rre.lu.postal_code("adresse: 12, rue de la Gare, L-1010.") == ["L-1010"]
    assert rre.lu.postal_code("'L-5555'") == ["L-5555"]
    assert rre.lu.postal_code("PLZ:L-8009 Strassen") == ["L-8009"]
    assert rre.lu.postal_code("L-0123") == []
    assert rre.lu.postal_code("L-123") == []
    assert rre.lu.postal_code("L-12345") == []
    assert rre.lu.postal_code("B-1234") == []  # Belgian
    assert rre.lu.postal_code("XL-1234") == []
    assert rre.lu.postal_code("L 2449") == []
    assert rre.lu.postal_code("l-2449") == []


def test_hard_rcs_number():
    assert rre.lu.rcs_number("RCS Luxembourg B123456") == ["RCS Luxembourg B123456"]
    assert rre.lu.rcs_number("R.C.S. Luxembourg: B 12.345") == ["R.C.S. Luxembourg: B 12.345"]
    assert rre.lu.rcs_number("Trade and Companies Register number B 123456") == [
        "Trade and Companies Register number B 123456"]
    assert rre.lu.rcs_number("RCS Diekirch n° F 1234") == ["RCS Diekirch n° F 1234"]
    assert rre.lu.rcs_number("(RCS B 98765)") == ["RCS B 98765"]
    assert rre.lu.rcs_number("R.C.S. Lux. B 123.456.") == ["R.C.S. Lux. B 123.456"]  # abbreviated
    assert rre.lu.rcs_number("RCS Luxembourg B 1234567") == []  # seven digits
    assert rre.lu.rcs_number("RCS Luxembourg Z 123456") == []  # no such section
    assert rre.lu.rcs_number("RCS Luxembourg B 12") == []
    assert rre.lu.rcs_number("RCS Luxembourg B 123 456 789") == []
    assert rre.lu.rcs_number("rcs luxembourg b 123456") == []
    assert rre.lu.rcs_number("RCS Luxembourg B 123.4567") == []


def test_hard_street_address():
    assert rre.lu.street_address("2, boulevard Royal") == ["2, boulevard Royal"]
    assert rre.lu.street_address("15, route d'Arlon, L-8009 Strassen") == ["15, route d'Arlon"]
    assert rre.lu.street_address("(4, Rue du Fort Wallis)") == ["4, Rue du Fort Wallis"]
    assert rre.lu.street_address("8-10, montée de la Pétrusse") == ["8-10, montée de la Pétrusse"]
    assert rre.lu.street_address("wunnt 21, Hauptstraße") == ["21, Hauptstraße"]
    assert rre.lu.street_address("12, RUE DE LA GARE") == ["12, RUE DE LA GARE"]
    assert rre.lu.street_address("Habite au 3, côte d'Eich.") == ["3, côte d'Eich"]
    assert rre.lu.street_address("12 rue") == []  # no name
    assert rre.lu.street_address("rue de la Gare") == []  # no number
    assert rre.lu.street_address("1234, rue de la Gare") == []
    assert rre.lu.street_address("12 avenues plus loin") == []
    assert rre.lu.street_address("En 2 routes différentes") == []
    assert rre.lu.street_address("Il habite au 12 rue de la paix") == []
    assert rre.lu.street_address("15 Rue") == []


def test_hard_vat_number():
    assert rre.lu.vat_number("LU10000356") == ["LU10000356"]
    assert rre.lu.vat_number("(LU 100 003 56)") == ["LU 100 003 56"]
    assert rre.lu.vat_number("TVA: LU 234.567.52.") == ["LU 234.567.52"]
    assert rre.lu.vat_number("n° TVA LU98765421") == ["LU98765421"]
    assert rre.lu.vat_number("USt-IdNr.:LU55555517") == ["LU55555517"]
    assert rre.lu.vat_number("'LU23456752'") == ["LU23456752"]
    assert rre.lu.vat_number("LU1234561") == []  # seven digits
    assert rre.lu.vat_number("LU123456133") == []  # nine
    assert rre.lu.vat_number("LU 1234 5613") == []
    assert rre.lu.vat_number("LU28 0019 4006 4475 0000") == []  # an IBAN
    assert rre.lu.vat_number("LU00000000") == []  # a placeholder
    assert rre.lu.vat_number("XLU12345613") == []
    assert rre.lu.vat_number("BE0123456749") == []
