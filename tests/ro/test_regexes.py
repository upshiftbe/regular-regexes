from regular_regexes import rre

# Numbers below are published specimens or computed with the check digit algorithm. Romania reserves no phone
# numbers for fiction: the phone tests use placeholder digits.


def test_cnp():
    # born 1 January 2090 in Cluj (12)
    assert rre.ro.cnp("CNP 5900101123454") == ["5900101123454"]
    assert rre.ro.cnp("5900101123455") == []
    assert rre.ro.cnp("5900101993451") == []  # checksum fine, county 99


def test_cui():
    assert rre.ro.cui("CUI 12345674, C.I.F.: RO 12345674") == ["CUI 12345674", "C.I.F.: RO 12345674"]
    assert rre.ro.cui("CUI 12345675") == []
    assert rre.ro.cui("nr 12345674") == []


def test_vat_number():
    assert rre.ro.vat_number("TVA RO12345674") == ["RO12345674"]
    assert rre.ro.vat_number("RO12345675") == []


def test_trade_register_number():
    assert rre.ro.trade_register_number("J40/1234/2020 si J2025000001004") == ["J40/1234/2020", "J2025000001004"]
    assert rre.ro.trade_register_number("J2025000001005") == []
    assert rre.ro.trade_register_number("J41/1234/2020 J40/1234/2025") == []  # county 41, old format after 2024


def test_id_card_number():
    assert rre.ro.id_card_number("CI seria RX nr. 123456, C.I. KX 654321, XB123456") == [
        "RX nr. 123456", "KX 654321", "XB123456"]
    assert rre.ro.id_card_number("seria QQ 123456") == []  # no such series


def test_passport_number():
    assert rre.ro.passport_number("pașaport nr. 051234567") == ["pașaport nr. 051234567"]
    assert rre.ro.passport_number("nr. 051234567") == []


def test_mrz_id_card():
    td2 = "RX123456<9ROU9001011M300101914000108"  # line 2 of the older card
    td1 = "IDROUMB12345675" + "<" * 15  # line 1 of the electronic card
    assert rre.ro.mrz_id_card(f"{td2}\n{td1}") == [td2, td1]
    assert rre.ro.mrz_id_card(td2.replace("<9", "<8")) == []


def test_mrz_passport():
    # ICAO 9303 specimen with ROU nationality
    line = "L898902C36ROU7408122F1204159ZE184226B<<<<<10"
    assert rre.ro.mrz_passport(line) == [line]
    assert rre.ro.mrz_passport(line.replace("C36", "C37")) == []


def test_iban():
    # IBAN registry example
    assert rre.ro.iban("cont RO49 AAAA 1B31 0075 9384 0000") == ["RO49 AAAA 1B31 0075 9384 0000"]
    assert rre.ro.iban("RO49AAAA1B31007593840001") == []


def test_bic():
    assert rre.ro.bic("BIC RNCBROBU sau BTRLRO22") == ["RNCBROBU", "BTRLRO22"]
    assert rre.ro.bic("PKOPPLPW") == []


def test_phone_number():
    assert rre.ro.phone_number("tel 021 123 4567, (0264) 123 456, +40 722 123 456") == [
        "021 123 4567", "(0264) 123 456", "+40 722 123 456"]
    assert rre.ro.phone_number("data 02.03.2024 15:30, 0123456789") == []


def test_mobile_number():
    assert rre.ro.mobile_number("mobil 0722.123.456 sau +40722123456") == ["0722.123.456", "+40722123456"]
    assert rre.ro.mobile_number("021 123 4567") == []


def test_premium_number():
    assert rre.ro.premium_number("suna la 0900 123 456") == ["0900 123 456"]
    assert rre.ro.premium_number("0800 123 456") == []


def test_msisdn():
    assert rre.ro.msisdn("msisdn 40722123456") == ["40722123456"]
    assert rre.ro.msisdn("40212345678") == []


def test_imsi():
    assert rre.ro.imsi("imsi 226011234567890") == ["226011234567890"]
    assert rre.ro.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.ro.iccid("sim 8940011234567890125") == ["8940011234567890125"]
    assert rre.ro.iccid("sim 8940011234567890126") == []


def test_license_plate():
    assert rre.ro.license_plate("masina B 123 ABC, CJ-12-XYZ") == ["B 123 ABC", "CJ-12-XYZ"]
    assert rre.ro.license_plate("CJ 123 ABC, B 12 IAB, XX 12 ABC") == []


def test_postal_code_city():
    assert rre.ro.postal_code_city("400001 Cluj-Napoca, 010011 București") == [
        "400001 Cluj-Napoca", "010011 București"]
    assert rre.ro.postal_code_city("comanda 400001 livrata") == []


def test_street_address():
    assert rre.ro.street_address("Str. Mihai Eminescu nr. 5, bl. A2, sc. 1, ap. 12, Cluj") == [
        "Str. Mihai Eminescu nr. 5, bl. A2, sc. 1, ap. 12"]
    assert rre.ro.street_address("Calea Victoriei 155 si Șos. Kiseleff nr. 1") == [
        "Calea Victoriei 155", "Șos. Kiseleff nr. 1"]
    assert rre.ro.street_address("strada noastra") == []


def test_company_name():
    assert rre.ro.company_name("intre S.C. Alfa Beta S.R.L. si Popescu Ion PFA") == [
        "S.C. Alfa Beta S.R.L.", "Popescu Ion PFA"]
    assert rre.ro.company_name("PFA Popescu Ion") == ["PFA Popescu Ion"]
    assert rre.ro.company_name("un srl mic") == []


def test_ecli():
    # e-Justice portal example
    assert rre.ro.ecli("vezi ECLI:RO:JDS4B:2017:001.004053.") == ["ECLI:RO:JDS4B:2017:001.004053"]


def test_aircraft_registration():
    assert rre.ro.aircraft_registration("YR-ABC, YR-1234, drona YR-D0012") == ["YR-ABC", "YR-1234", "YR-D0012"]
    assert rre.ro.aircraft_registration("YR-AB YR-0123") == []


def test_hard_aircraft_registration():
    assert rre.ro.aircraft_registration("(YR-BMA)") == ["YR-BMA"]
    assert rre.ro.aircraft_registration("avionul YR-BGF a aterizat") == ["YR-BGF"]
    assert rre.ro.aircraft_registration('"YR-ATA".') == ["YR-ATA"]
    assert rre.ro.aircraft_registration("YR-9876,YR-D1234") == ["YR-9876", "YR-D1234"]
    assert rre.ro.aircraft_registration("YR-QQQ") == ["YR-QQQ"]
    assert rre.ro.aircraft_registration("planor\nYR-1001") == ["YR-1001"]
    assert rre.ro.aircraft_registration("YR-AB") == []
    assert rre.ro.aircraft_registration("YR-ABCD") == []
    assert rre.ro.aircraft_registration("YR-D001") == []
    assert rre.ro.aircraft_registration("YR-D00123") == []
    assert rre.ro.aircraft_registration("XYR-ABC") == []
    assert rre.ro.aircraft_registration("yr-abc") == []
    assert rre.ro.aircraft_registration("YR-12345") == []


def test_hard_bic():
    assert rre.ro.bic("ABCDROBU.") == ["ABCDROBU"]
    assert rre.ro.bic("(WXYZROB2)") == ["WXYZROB2"]
    assert rre.ro.bic('SWIFT: "QWERROBUXXX"') == ["QWERROBUXXX"]
    assert rre.ro.bic("cod BIC ABCDRO22, IBAN") == ["ABCDRO22"]
    assert rre.ro.bic("ZZZZROBC") == ["ZZZZROBC"]
    assert rre.ro.bic("BIC:ABCDROBUXXX/WXYZROB2") == ["ABCDROBUXXX", "WXYZROB2"]
    assert rre.ro.bic("RNCBROB") == []
    assert rre.ro.bic("RNCBROBUX") == []
    assert rre.ro.bic("RNCBROBUXX") == []
    assert rre.ro.bic("RNCBROBUXXXX") == []
    assert rre.ro.bic("RNCBHUBU") == []
    assert rre.ro.bic("RNC8ROBU") == []
    assert rre.ro.bic("rncbrobu") == []


def test_hard_cnp():
    assert rre.ro.cnp("1850715401236") == ["1850715401236"]
    assert rre.ro.cnp("CNP: 2981231123455, născută") == ["2981231123455"]
    assert rre.ro.cnp("(7900615700046)") == ["7900615700046"]  # resident, county code 70
    assert rre.ro.cnp('"8920101070091".') == ["8920101070091"]
    assert rre.ro.cnp("6000229400010") == ["6000229400010"]  # 29 February 2000
    assert rre.ro.cnp("5020228520011;9020301700017") == ["5020228520011", "9020301700017"]
    assert rre.ro.cnp("1850715401237") == []
    assert rre.ro.cnp("6100229520016") == []  # checksum fine, 29 February 2010
    assert rre.ro.cnp("1900230123454") == []  # checksum fine, 30 February
    assert rre.ro.cnp("1990101991235") == []  # checksum fine, county 99
    assert rre.ro.cnp("185071540123") == []
    assert rre.ro.cnp("18507154012361") == []
    assert rre.ro.cnp("0850715401236") == []
    assert rre.ro.cnp("x1850715401236") == []


def test_hard_company_name():
    assert rre.ro.company_name("Gamma SRL") == ["Gamma SRL"]
    assert rre.ro.company_name("(Delta S.A.)") == ["Delta S.A."]
    assert rre.ro.company_name("Ionescu Maria I.I.") == ["Ionescu Maria I.I."]
    assert rre.ro.company_name("Familia Pop I.F.") == ["Familia Pop I.F."]
    assert rre.ro.company_name("Omega SRL-D") == ["Omega SRL-D"]
    assert rre.ro.company_name("SC Exemplu SRL, CUI") == ["SC Exemplu SRL"]
    # the name in quotes, as contracts write it
    assert rre.ro.company_name("S.C. „ALFA” S.R.L.") == ["S.C. „ALFA” S.R.L."]
    assert rre.ro.company_name('contract cu SC "ALFA BETA" SRL') == ['SC "ALFA BETA" SRL']
    assert rre.ro.company_name("Popa & Asociații S.N.C.") == ["Popa & Asociații S.N.C."]
    assert rre.ro.company_name("Alfa srl") == []
    assert rre.ro.company_name("Alfa SRLX") == []
    assert rre.ro.company_name("SRL") == []
    assert rre.ro.company_name("alfa beta SRL") == []
    assert rre.ro.company_name("PFA") == []
    assert rre.ro.company_name("PFA popescu") == []


def test_hard_cui():
    assert rre.ro.cui("CIF RO18547290") == ["CIF RO18547290"]
    assert rre.ro.cui("cod fiscal 31856705") == ["cod fiscal 31856705"]
    assert rre.ro.cui("Codul fiscal: 40123452.") == ["Codul fiscal: 40123452"]
    assert rre.ro.cui("(C.U.I. 9876544)") == ["C.U.I. 9876544"]
    assert rre.ro.cui("CUI:1234567897, sediul") == ["CUI:1234567897"]
    assert rre.ro.cui("CIF: 124") == ["CIF: 124"]
    assert rre.ro.cui("CUI 18547291") == []
    assert rre.ro.cui("CUI 0123456") == []
    assert rre.ro.cui("CUI 1") == []
    assert rre.ro.cui("CUI 12345678901") == []
    assert rre.ro.cui("CUIX 18547290") == []
    assert rre.ro.cui("ACUI 18547290") == []
    assert rre.ro.cui("cui 18547290") == []
    assert rre.ro.cui("al cui 2 copii") == []


def test_hard_ecli():
    assert rre.ro.ecli("ECLI:RO:ICCJ:2019:123") == ["ECLI:RO:ICCJ:2019:123"]
    assert rre.ro.ecli("(ECLI:RO:CCR:2020:456)") == ["ECLI:RO:CCR:2020:456"]
    assert rre.ro.ecli("decizia ECLI:RO:CAB:2018:001.002345, publicată") == ["ECLI:RO:CAB:2018:001.002345"]
    assert rre.ro.ecli('"ECLI:RO:TBCJ:2021:12.3".') == ["ECLI:RO:TBCJ:2021:12.3"]
    assert rre.ro.ecli("ECLI:RO:JDS4B:2017:001.004053") == ["ECLI:RO:JDS4B:2017:001.004053"]
    assert rre.ro.ecli("ECLI:RO:ICCJ:2019:A1") == ["ECLI:RO:ICCJ:2019:A1"]
    assert rre.ro.ecli("ECLI:IT:ICCJ:2019:123") == []
    assert rre.ro.ecli("ECLI:RO::2017:1") == []
    assert rre.ro.ecli("ECLI:RO:ICCJ:17:1") == []
    assert rre.ro.ecli("ECLI:RO:ICCJ:2019:") == []
    assert rre.ro.ecli("XECLI:RO:ICCJ:2019:123") == []
    assert rre.ro.ecli("ECLI RO ICCJ 2019 123") == []
    assert rre.ro.ecli("ECLI:RO:iccj:2019:123") == []


def test_hard_iban():
    assert rre.ro.iban("RO93ABCD1234567890123456") == ["RO93ABCD1234567890123456"]
    assert rre.ro.iban("IBAN: RO94 WXYZ 0000 0000 AB12 CD34.") == ["RO94 WXYZ 0000 0000 AB12 CD34"]
    assert rre.ro.iban("(RO49 AAAA 1B31 0075 9384 0000)") == ["RO49 AAAA 1B31 0075 9384 0000"]
    assert rre.ro.iban('"RO49AAAA1B31007593840000"') == ["RO49AAAA1B31007593840000"]
    assert rre.ro.iban("cont RO93 ABCD 1234 5678 9012 3456 deschis") == ["RO93 ABCD 1234 5678 9012 3456"]
    assert rre.ro.iban("RO94WXYZ00000000AB12CD34,RO93ABCD1234567890123456") == [
        "RO94WXYZ00000000AB12CD34", "RO93ABCD1234567890123456"]
    assert rre.ro.iban("RO49 AAAA 1B31 0075 9384 0001") == []
    assert rre.ro.iban("RO49 AAAA 1B31 0075 9384 000") == []
    assert rre.ro.iban("RO49 AAAA 1B31 0075 9384 00001") == []
    assert rre.ro.iban("RO49 1234 1B31 0075 9384 0000") == []
    assert rre.ro.iban("XRO49AAAA1B31007593840000") == []
    assert rre.ro.iban("ro49aaaa1b31007593840000") == []
    assert rre.ro.iban("BG49 AAAA 1B31 0075 9384 0000") == []


def test_hard_iccid():
    assert rre.ro.iccid("ICCID: 8940034444555566669") == ["8940034444555566669"]
    assert rre.ro.iccid("(89401076543210987659)") == ["89401076543210987659"]
    assert rre.ro.iccid("sim 894005121212121219.") == ["894005121212121219"]
    assert rre.ro.iccid('"8940011234567890125"') == ["8940011234567890125"]
    assert rre.ro.iccid("cartela SIM 8940034444555566669 activă") == ["8940034444555566669"]
    assert rre.ro.iccid("8940034444555566669;89401076543210987659") == [
        "8940034444555566669", "89401076543210987659"]
    assert rre.ro.iccid("8940034444555566668") == []
    assert rre.ro.iccid("89400344445555666") == []
    assert rre.ro.iccid("894003444455556666912") == []
    assert rre.ro.iccid("8939034444555566669") == []
    assert rre.ro.iccid("x8940034444555566669") == []
    assert rre.ro.iccid("18940034444555566669") == []


def test_hard_id_card_number():
    assert rre.ro.id_card_number("seria RT nr 123456") == ["RT nr 123456"]
    assert rre.ro.id_card_number("seria MZ numărul 654321") == ["MZ numărul 654321"]
    assert rre.ro.id_card_number("(SV 123456)") == ["SV 123456"]
    assert rre.ro.id_card_number('"TZ123456".') == ["TZ123456"]
    assert rre.ro.id_card_number("CI: AX, nr. 123456") == ["AX, nr. 123456"]
    assert rre.ro.id_card_number("Seria IF Nr. 987654") == ["IF Nr. 987654"]
    assert rre.ro.id_card_number("RX 12345") == []
    assert rre.ro.id_card_number("RX 1234567") == []
    assert rre.ro.id_card_number("rx 123456") == []
    assert rre.ro.id_card_number("XRX123456") == []
    assert rre.ro.id_card_number("RO 123456") == []  # no such series
    assert rre.ro.id_card_number("RX-123456") == []
    assert rre.ro.id_card_number("B 123456") == []


def test_hard_imsi():
    assert rre.ro.imsi("IMSI 226011234567890") == ["226011234567890"]
    assert rre.ro.imsi("imsi:226101234567890") == ["226101234567890"]
    assert rre.ro.imsi("(226051234567890)") == ["226051234567890"]
    assert rre.ro.imsi('"226031234567890".') == ["226031234567890"]
    assert rre.ro.imsi("codul IMSI 226109876543210 al cartelei") == ["226109876543210"]
    assert rre.ro.imsi("226011234567890,226101234567890") == ["226011234567890", "226101234567890"]
    assert rre.ro.imsi("22601123456789") == []
    assert rre.ro.imsi("2260112345678901") == []
    assert rre.ro.imsi("262011234567890") == []
    assert rre.ro.imsi("1226011234567890") == []
    assert rre.ro.imsi("x226011234567890") == []
    assert rre.ro.imsi("226011234567890x") == []


def test_hard_license_plate():
    assert rre.ro.license_plate("B 12 ABC") == ["B 12 ABC"]
    assert rre.ro.license_plate("CJ12XYZ") == ["CJ12XYZ"]
    assert rre.ro.license_plate("(AG 10 BCD)") == ["AG 10 BCD"]
    assert rre.ro.license_plate('"PH-05-MNP".') == ["PH-05-MNP"]
    assert rre.ro.license_plate("mașina B-101-RST a fost") == ["B-101-RST"]
    assert rre.ro.license_plate("TM 99 ZZZ") == ["TM 99 ZZZ"]
    assert rre.ro.license_plate("b 123 abc") == []
    assert rre.ro.license_plate("B 1234 ABC") == []
    assert rre.ro.license_plate("CJ 12 AB") == []
    assert rre.ro.license_plate("CJ 12 ABCD") == []
    assert rre.ro.license_plate("CJ 12 ABQ") == []
    assert rre.ro.license_plate("B 12 OAB") == []
    assert rre.ro.license_plate("XB 12 ABC") == []
    assert rre.ro.license_plate("CJ 1 ABC") == []


def test_hard_mobile_number():
    assert rre.ro.mobile_number("0722 123 456") == ["0722 123 456"]
    assert rre.ro.mobile_number("+40 (0) 722 123 456") == ["+40 (0) 722 123 456"]
    assert rre.ro.mobile_number("0040 744 123 456") == ["0040 744 123 456"]
    assert rre.ro.mobile_number("(0744-123-456)") == ["0744-123-456"]
    assert rre.ro.mobile_number("sună la 0722/123456, mulțumesc") == ["0722/123456"]
    assert rre.ro.mobile_number('"+40 722 123 456".') == ["+40 722 123 456"]
    assert rre.ro.mobile_number("0722 123 45") == []
    assert rre.ro.mobile_number("0722 123 4567") == []
    assert rre.ro.mobile_number("0702 123 456") == []
    assert rre.ro.mobile_number("40722123456") == []
    assert rre.ro.mobile_number("+40 21 123 4567") == []
    assert rre.ro.mobile_number("0722 123 456 789") == []
    assert rre.ro.mobile_number("+41 722 123 456") == []
    assert rre.ro.mobile_number("10722123456") == []


def test_hard_mrz_id_card():
    assert rre.ro.mrz_id_card("IDROUXB12345672<<<<<<<<<<<<<<<") == ["IDROUXB12345672<<<<<<<<<<<<<<<"]
    assert rre.ro.mrz_id_card("(IDROUCJ76543217<<<<<<<<<<<<<<<)") == ["IDROUCJ76543217<<<<<<<<<<<<<<<"]
    td2 = "KX654321<2ROU8503150F250315828503158"
    assert rre.ro.mrz_id_card(f"IDROUBUCUR<<IOANA<<<<<<<<<<<<<<<<<<<\n{td2}") == [td2]
    assert rre.ro.mrz_id_card('MRZ: "MZ111222<2ROU0112318M311231950112311"') == [
        "MZ111222<2ROU0112318M311231950112311"]
    assert rre.ro.mrz_id_card("IDROUXB12345672<<<<<<<<<<<<<<<\n9001011M3001019ROU<<<<<<<<<<<0") == [
        "IDROUXB12345672<<<<<<<<<<<<<<<"]
    assert rre.ro.mrz_id_card(f"{td2}.") == [td2]
    assert rre.ro.mrz_id_card(td2.replace("<2ROU", "<3ROU")) == []  # card number check digit
    assert rre.ro.mrz_id_card(td2.replace("8503150", "8503151")) == []  # birth date check digit
    assert rre.ro.mrz_id_card(td2.replace("2503158", "2503159")) == []  # expiry date check digit
    assert rre.ro.mrz_id_card(td2.replace("ROU", "HUN")) == []
    assert rre.ro.mrz_id_card(td2[:-1]) == []
    assert rre.ro.mrz_id_card("IDROUXB12345673<<<<<<<<<<<<<<<") == []
    assert rre.ro.mrz_id_card("IDROUXB12345672<<<<<<<<<<<<<<<<") == []


def test_hard_mrz_passport():
    line = "0512345673ROU9001011M3001019<<<<<<<<<<<<<<<0"
    assert rre.ro.mrz_passport(line) == [line]
    # an eight-digit number and the CNP in the personal number field
    assert rre.ro.mrz_passport(
        "P<ROUPOPESCU<<ANA<<<<<<<<<<<<<<<<<<<<<<<<<<<\n05123456<6ROU7512319F28123132751231123459<92") == [
        "05123456<6ROU7512319F28123132751231123459<92"]
    assert rre.ro.mrz_passport("(L898902C36ROU7408122F1204159ZE184226B<<<<<10)") == [
        "L898902C36ROU7408122F1204159ZE184226B<<<<<10"]
    assert rre.ro.mrz_passport(f'mrz "{line}".') == [line]
    assert rre.ro.mrz_passport(f"pagina 2: {line}, sfârșit") == [line]
    assert rre.ro.mrz_passport(line.replace("1M30", "1<30")) == [line.replace("1M30", "1<30")]
    assert rre.ro.mrz_passport(line.replace("73ROU", "74ROU")) == []
    assert rre.ro.mrz_passport(line.replace("9001011", "9001012")) == []
    assert rre.ro.mrz_passport(line.replace("3001019", "3001018")) == []
    assert rre.ro.mrz_passport(line.replace("ROU", "MDA")) == []
    assert rre.ro.mrz_passport(line[:-1]) == []
    assert rre.ro.mrz_passport(line + "0") == []


def test_hard_msisdn():
    assert rre.ro.msisdn("MSISDN: 40744123456") == ["40744123456"]
    assert rre.ro.msisdn("(40766123456)") == ["40766123456"]
    assert rre.ro.msisdn('"40733123456".') == ["40733123456"]
    assert rre.ro.msisdn("40722123456,40744123456") == ["40722123456", "40744123456"]
    assert rre.ro.msisdn("40712034567") == ["40712034567"]
    assert rre.ro.msisdn("apelant 40755123456 la ora 10") == ["40755123456"]
    assert rre.ro.msisdn("+40722123456") == []
    assert rre.ro.msisdn("4072212345") == []
    assert rre.ro.msisdn("407221234567") == []
    assert rre.ro.msisdn("0040722123456") == []
    assert rre.ro.msisdn("40702123456") == []
    assert rre.ro.msisdn("x40722123456") == []
    assert rre.ro.msisdn("40 722 123 456") == []


def test_hard_passport_number():
    assert rre.ro.passport_number("Pașaportul nr. 05123456") == ["Pașaportul nr. 05123456"]
    assert rre.ro.passport_number("PASAPORT: 051234567") == ["PASAPORT: 051234567"]
    assert rre.ro.passport_number("passport no. 051234567") == ["passport no. 051234567"]
    assert rre.ro.passport_number("pașaportul numărul 051234567") == ["pașaportul numărul 051234567"]
    assert rre.ro.passport_number("paşaport 051234567, emis") == ["paşaport 051234567"]  # ş with a cedilla
    assert rre.ro.passport_number("(pasaport nr 05987654)") == ["pasaport nr 05987654"]
    assert rre.ro.passport_number("Pașaport nr./Passport No. 051234567") == ["Passport No. 051234567"]
    assert rre.ro.passport_number("nr. 051234567") == []
    assert rre.ro.passport_number("pașaport nr. 0512345") == []
    assert rre.ro.passport_number("pașaport nr. 0512345678") == []
    assert rre.ro.passport_number("pașaport nr. AB123456") == []
    assert rre.ro.passport_number("pașapoarte 051234567") == []
    assert rre.ro.passport_number("pașaport valabil 051234567") == []


def test_hard_phone_number():
    assert rre.ro.phone_number("0040 21 123 4567") == ["0040 21 123 4567"]
    assert rre.ro.phone_number("+40 (0) 21 123 4567") == ["+40 (0) 21 123 4567"]
    assert rre.ro.phone_number("0264.123.456") == ["0264.123.456"]
    assert rre.ro.phone_number("(021) 123 4567") == ["(021) 123 4567"]
    assert rre.ro.phone_number("sunați la 0722123456, vă rog") == ["0722123456"]
    assert rre.ro.phone_number('"0256-123-456".') == ["0256-123-456"]
    assert rre.ro.phone_number("021 123 456") == []
    assert rre.ro.phone_number("021 123 45678") == []
    assert rre.ro.phone_number("+41 21 123 4567") == []
    assert rre.ro.phone_number("10264123456") == []
    assert rre.ro.phone_number("0264 123 456 789") == []
    assert rre.ro.phone_number("0464 123 456") == []
    assert rre.ro.phone_number("CNP 1850715401236") == []


def test_hard_postal_code_city():
    assert rre.ro.postal_code_city("700259 Iași") == ["700259 Iași"]
    assert rre.ro.postal_code_city("(300011 Timișoara)") == ["300011 Timișoara"]
    assert rre.ro.postal_code_city("540001 Târgu Mureș") == ["540001 Târgu Mureș"]
    assert rre.ro.postal_code_city("cod poștal 410001 Oradea.") == ["410001 Oradea"]
    assert rre.ro.postal_code_city("Str. Exemplu nr. 5, 550003 Sibiu") == ["550003 Sibiu"]
    assert rre.ro.postal_code_city("900001 Constanța") == ["900001 Constanța"]
    assert rre.ro.postal_code_city("40001 Cluj") == []
    assert rre.ro.postal_code_city("4000011 Cluj") == []
    assert rre.ro.postal_code_city("400001 cluj") == []
    assert rre.ro.postal_code_city("400001Cluj") == []
    # amounts
    assert rre.ro.postal_code_city("plătit 150000 Lei") == []
    assert rre.ro.postal_code_city("Total 123456 RON") == []
    assert rre.ro.postal_code_city("123456 EUR") == []


def test_hard_premium_number():
    assert rre.ro.premium_number("0906 123 456") == ["0906 123 456"]
    assert rre.ro.premium_number("0903.123.456") == ["0903.123.456"]
    assert rre.ro.premium_number("+40 900 123 456") == ["+40 900 123 456"]
    assert rre.ro.premium_number("0040 906 123 456") == ["0040 906 123 456"]
    assert rre.ro.premium_number("(0900123456)") == ["0900123456"]
    assert rre.ro.premium_number("sunați la 0903-123-456 acum") == ["0903-123-456"]
    assert rre.ro.premium_number("0900 123 45") == []
    assert rre.ro.premium_number("0900 123 4567") == []
    assert rre.ro.premium_number("0900 123 456 789") == []
    assert rre.ro.premium_number("0902 123 456") == []
    assert rre.ro.premium_number("10900 123 456") == []
    assert rre.ro.premium_number("+41 900 123 456") == []


def test_hard_street_address():
    assert rre.ro.street_address("Bd. Unirii nr. 10") == ["Bd. Unirii nr. 10"]
    assert rre.ro.street_address("Bulevardul Magheru 20") == ["Bulevardul Magheru 20"]
    assert rre.ro.street_address("Aleea Teilor 3") == ["Aleea Teilor 3"]
    assert rre.ro.street_address("Splaiul Independenței 313") == ["Splaiul Independenței 313"]
    assert rre.ro.street_address("locuiește pe strada Lungă 7, etaj 2") == ["strada Lungă 7"]
    assert rre.ro.street_address("B-dul Eroilor 5") == ["B-dul Eroilor 5"]
    assert rre.ro.street_address("STR. LUNGĂ NR. 7") == ["STR. LUNGĂ NR. 7"]
    assert rre.ro.street_address("(Str. Mare nr. 12A)") == ["Str. Mare nr. 12A"]
    assert rre.ro.street_address("Șoseaua Pipera 1, sc. B, et. 3, ap. 15") == [
        "Șoseaua Pipera 1, sc. B, et. 3, ap. 15"]
    assert rre.ro.street_address("Str. 5") == []
    assert rre.ro.street_address("str. mare 5") == []
    assert rre.ro.street_address("et al. 2019") == []
    assert rre.ro.street_address("strada 5 case") == []
    assert rre.ro.street_address("Strada Lungă") == []
    assert rre.ro.street_address("Calea ferată 5") == []
    assert rre.ro.street_address("stradal Mare 5") == []


def test_hard_trade_register_number():
    assert rre.ro.trade_register_number("J12/345/2005") == ["J12/345/2005"]
    assert rre.ro.trade_register_number("J 40 / 1234 / 2020") == ["J 40 / 1234 / 2020"]
    assert rre.ro.trade_register_number("(C1/1/2010)") == ["C1/1/2010"]
    assert rre.ro.trade_register_number("nr. ORC J40/12345/1995, CUI") == ["J40/12345/1995"]
    assert rre.ro.trade_register_number("J2023001234405") == ["J2023001234405"]
    assert rre.ro.trade_register_number('"F2024000012001".') == ["F2024000012001"]
    assert rre.ro.trade_register_number("C2025000099004 și F12/123/2015") == ["C2025000099004", "F12/123/2015"]
    assert rre.ro.trade_register_number("J40/1234/1989") == []
    assert rre.ro.trade_register_number("J40/123456/2020") == []
    assert rre.ro.trade_register_number("X40/1234/2020") == []
    assert rre.ro.trade_register_number("J2025000001") == []
    assert rre.ro.trade_register_number("J20250000010041") == []
    assert rre.ro.trade_register_number("j40/1234/2020") == []
    assert rre.ro.trade_register_number("J0/1234/2020") == []
    assert rre.ro.trade_register_number("J2023001234400") == []


def test_hard_vat_number():
    assert rre.ro.vat_number("RO 18547290") == ["RO 18547290"]
    assert rre.ro.vat_number("cod TVA: RO31856705.") == ["RO31856705"]
    assert rre.ro.vat_number("(RO40123452)") == ["RO40123452"]
    assert rre.ro.vat_number('"RO1234567897"') == ["RO1234567897"]
    assert rre.ro.vat_number("RO9876544, CUI") == ["RO9876544"]
    assert rre.ro.vat_number("RO123453") == ["RO123453"]
    assert rre.ro.vat_number("RO18547291") == []
    assert rre.ro.vat_number("RO 1234") == []
    assert rre.ro.vat_number("RO12345678901") == []
    assert rre.ro.vat_number("RO012345674") == []
    assert rre.ro.vat_number("XRO18547290") == []
    assert rre.ro.vat_number("RO49 AAAA 1B31 0075 9384 0000") == []
    assert rre.ro.vat_number("ro18547290") == []
    assert rre.ro.vat_number("BG18547290") == []


def test_overlap_postal_code_city():
    # a place name has no digits: not the middle of a UK driving licence number
    assert rre.ro.postal_code_city("MORGA 657054 SM9IJ") == []
    assert rre.ro.postal_code_city("010011 București, 400001 Cluj-Napoca") == ["010011 București", "400001 Cluj-Napoca"]
