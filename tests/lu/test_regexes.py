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
