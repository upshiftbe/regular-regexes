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
