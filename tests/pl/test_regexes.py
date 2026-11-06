from regular_regexes import rre

# Numbers below are published specimens or computed with the check digit algorithm. Poland reserves no phone
# numbers for fiction: the phone tests use placeholder digits.


def test_pesel():
    # born 14 May 2101: the month is raised by 40
    assert rre.pl.pesel("PESEL 01451401354") == ["01451401354"]
    assert rre.pl.pesel("PESEL 01451401355") == []
    assert rre.pl.pesel("01130101353") == []  # checksum fine, month 13


def test_nip():
    assert rre.pl.nip("NIP: 123-456-32-18, NIP 1234563218") == ["NIP: 123-456-32-18", "NIP 1234563218"]
    assert rre.pl.nip("firma 123-456-32-18, osoba 123-45-63-218") == ["123-456-32-18", "123-45-63-218"]
    assert rre.pl.nip("NIP 123-456-32-19") == []
    assert rre.pl.nip("nr 1234563218") == []  # ten bare digits need the keyword


def test_vat_number():
    assert rre.pl.vat_number("VAT PL1234563218 / PL 123-456-32-18") == ["PL1234563218", "PL 123-456-32-18"]
    assert rre.pl.vat_number("PL1234563219") == []


def test_regon():
    assert rre.pl.regon("REGON: 123456785, REGON 12345678512347") == ["REGON: 123456785", "REGON 12345678512347"]
    assert rre.pl.regon("REGON 123456786") == []
    assert rre.pl.regon("REGON 12345678612342") == []  # last digit fine, but the first nine are no REGON
    assert rre.pl.regon("123456785") == []


def test_krs_number():
    assert rre.pl.krs_number("KRS 0000123456, nr KRS: 0000654321") == ["KRS 0000123456", "KRS: 0000654321"]
    assert rre.pl.krs_number("nr 0000123456") == []


def test_id_card_number():
    # specimen numbers of the 2001 and 2019 cards
    assert rre.pl.id_card_number("dowód ABA300000 i ZZC 108201") == ["ABA300000", "ZZC 108201"]
    assert rre.pl.id_card_number("ABA300001") == []


def test_passport_number():
    assert rre.pl.passport_number("paszport ZZ3000001") == ["ZZ3000001"]
    assert rre.pl.passport_number("ZZ4000001") == []


def test_mrz_id_card():
    line = "IDPOLZZC1082012" + "<" * 15
    assert rre.pl.mrz_id_card(f"mrz {line}") == [line]
    assert rre.pl.mrz_id_card("IDPOLZZC1082013" + "<" * 15) == []


def test_mrz_passport():
    # ICAO 9303 specimen with POL nationality
    line = "L898902C36POL7408122F1204159ZE184226B<<<<<10"
    assert rre.pl.mrz_passport(line) == [line]
    assert rre.pl.mrz_passport(line.replace("C36", "C37")) == []


def test_iban():
    # IBAN registry example
    assert rre.pl.iban("konto PL61 1090 1014 0000 0712 1981 2874") == ["PL61 1090 1014 0000 0712 1981 2874"]
    assert rre.pl.iban("PL61109010140000071219812875") == []


def test_nrb():
    assert rre.pl.nrb("nr rachunku 61 1090 1014 0000 0712 1981 2874") == ["61 1090 1014 0000 0712 1981 2874"]
    assert rre.pl.nrb("61 1090 1014 0000 0712 1981 2875") == []


def test_bic():
    assert rre.pl.bic("BIC PKOPPLPW lub BREXPLPWXXX") == ["PKOPPLPW", "BREXPLPWXXX"]
    assert rre.pl.bic("GEBABEBB") == []


def test_phone_number():
    assert rre.pl.phone_number("tel. +48 22 123 45 67, (22) 123 45 67 lub 600 123 456") == [
        "+48 22 123 45 67", "(22) 123 45 67", "600 123 456"]
    assert rre.pl.phone_number("nr 221234567 i 1234 5678") == []


def test_mobile_number():
    assert rre.pl.mobile_number("kom. 600-123-456 lub +48 512 345 678") == ["600-123-456", "+48 512 345 678"]
    assert rre.pl.mobile_number("22 123 45 67 i 600 123 456 789") == []


def test_msisdn():
    assert rre.pl.msisdn("msisdn 48600123456") == ["48600123456"]
    assert rre.pl.msisdn("48221234567") == []


def test_imsi():
    assert rre.pl.imsi("imsi 260021234567890") == ["260021234567890"]
    assert rre.pl.imsi("imsi 206011234567890") == []


def test_iccid():
    assert rre.pl.iccid("sim 8948021234567890126") == ["8948021234567890126"]
    assert rre.pl.iccid("sim 8948021234567890127") == []


def test_license_plate():
    assert rre.pl.license_plate("auto WA 12345, KR 1234A i KRA 1C34") == ["WA 12345", "KR 1234A", "KRA 1C34"]
    assert rre.pl.license_plate("norma ISO 14001, WA 1234, KR 1234B") == []


def test_postal_code_city():
    assert rre.pl.postal_code_city("00-950 Warszawa i 43-300 Bielsko-Biała") == [
        "00-950 Warszawa", "43-300 Bielsko-Biała"]
    assert rre.pl.postal_code_city("od 10-100 osób") == []


def test_street_address():
    assert rre.pl.street_address("mieszka ul. Jana Pawła II 12/34, Kraków") == ["ul. Jana Pawła II 12/34"]
    assert rre.pl.street_address("os. Kościuszkowskie 5 m. 12") == ["os. Kościuszkowskie 5 m. 12"]
    assert rre.pl.street_address("www.onet.pl. Zobacz 5 razy") == []


def test_company_name():
    assert rre.pl.company_name("umowa z Kowalski Budownictwo Sp. z o.o. i Nowak sp.j.") == [
        "Kowalski Budownictwo Sp. z o.o.", "Nowak sp.j."]
    assert rre.pl.company_name("Budex S.A. oraz Alfa Sp. z o.o. sp.k.") == ["Budex S.A.", "Alfa Sp. z o.o. sp.k."]
    assert rre.pl.company_name("ta sp. z o.o. ma") == []


def test_aircraft_registration():
    assert rre.pl.aircraft_registration("SP-ABC, szybowiec SP-3456") == ["SP-ABC", "SP-3456"]
    assert rre.pl.aircraft_registration("SP-AB i SP-4567") == []


def test_hard_aircraft_registration():
    assert rre.pl.aircraft_registration("SP-SABC") == ["SP-SABC"]  # ultralight
    assert rre.pl.aircraft_registration("(SP-XABC)") == ["SP-XABC"]
    assert rre.pl.aircraft_registration("samolot SP-ABX wylądował") == ["SP-ABX"]
    assert rre.pl.aircraft_registration('"SP-8123".') == ["SP-8123"]
    assert rre.pl.aircraft_registration("SP-QQQ,SP-0001") == ["SP-QQQ", "SP-0001"]
    assert rre.pl.aircraft_registration("szybowiec\nSP-2345") == ["SP-2345"]
    assert rre.pl.aircraft_registration("SP-AB") == []
    assert rre.pl.aircraft_registration("SP-ABCDE") == []
    assert rre.pl.aircraft_registration("SP-AABC") == []  # four letters only after S or X
    assert rre.pl.aircraft_registration("SP-5678") == []
    assert rre.pl.aircraft_registration("XSP-ABC") == []
    assert rre.pl.aircraft_registration("sp-abc") == []
    assert rre.pl.aircraft_registration("SP-12345") == []
    assert rre.pl.aircraft_registration("OK-ABC") == []


def test_hard_bic():
    assert rre.pl.bic("ABCDPLPW.") == ["ABCDPLPW"]
    assert rre.pl.bic("(WXYZPLP2)") == ["WXYZPLP2"]
    assert rre.pl.bic('SWIFT: "QWERPLPWXXX"') == ["QWERPLPWXXX"]
    assert rre.pl.bic("kod BIC ABCDPL22, IBAN") == ["ABCDPL22"]
    assert rre.pl.bic("ZZZZPLPR") == ["ZZZZPLPR"]
    assert rre.pl.bic("BIC:ABCDPLPWXXX/WXYZPLP2") == ["ABCDPLPWXXX", "WXYZPLP2"]
    assert rre.pl.bic("PKOPPLP") == []
    assert rre.pl.bic("PKOPPLPWX") == []
    assert rre.pl.bic("PKOPPLPWXX") == []
    assert rre.pl.bic("PKOPPLPWXXXX") == []
    assert rre.pl.bic("PKOPDEPW") == []
    assert rre.pl.bic("PK0PPLPW") == []
    assert rre.pl.bic("pkopplpw") == []


def test_hard_company_name():
    assert rre.pl.company_name("„Kowalski” Sp. z o.o.") == ["„Kowalski” Sp. z o.o."]
    assert rre.pl.company_name("(Nowak Sp. z o.o.)") == ["Nowak Sp. z o.o."]
    assert rre.pl.company_name("Kowalski i Wspólnicy sp.k.") == ["Kowalski i Wspólnicy sp.k."]
    assert rre.pl.company_name("Alfa spółka z ograniczoną odpowiedzialnością") == [
        "Alfa spółka z ograniczoną odpowiedzialnością"]
    # the legal form written out with capitals, as in the register
    assert rre.pl.company_name("Beta Spółka Akcyjna") == ["Beta Spółka Akcyjna"]
    assert rre.pl.company_name("GAMMA SPÓŁKA KOMANDYTOWO-AKCYJNA") == ["GAMMA SPÓŁKA KOMANDYTOWO-AKCYJNA"]
    assert rre.pl.company_name("Delta S.K.A.") == ["Delta S.K.A."]
    assert rre.pl.company_name("ALFA SP. Z O.O.") == ["ALFA SP. Z O.O."]
    assert rre.pl.company_name("Umowa z Kowalski Sp. z o.o. zawarta") == ["Kowalski Sp. z o.o."]
    assert rre.pl.company_name("kowalski sp. z o.o.") == []
    assert rre.pl.company_name("Sp. z o.o.") == []
    assert rre.pl.company_name("Kowalski Sp. z o.") == []
    assert rre.pl.company_name("Kowalski SAS") == []
    assert rre.pl.company_name("Kowalski Spółka") == []
    assert rre.pl.company_name("Ala ma kota SA") == []
    assert rre.pl.company_name("Kowalski SAB") == []


def test_hard_iban():
    assert rre.pl.iban("PL19123456781234567890123456") == ["PL19123456781234567890123456"]
    assert rre.pl.iban("IBAN: PL10 9876 5432 0000 0000 0000 0042.") == ["PL10 9876 5432 0000 0000 0000 0042"]
    assert rre.pl.iban("(PL61 1090 1014 0000 0712 1981 2874)") == ["PL61 1090 1014 0000 0712 1981 2874"]
    assert rre.pl.iban('"PL19 1234 5678 1234 5678 9012 3456"') == ["PL19 1234 5678 1234 5678 9012 3456"]
    assert rre.pl.iban("przelew na PL61109010140000071219812874 dziś") == ["PL61109010140000071219812874"]
    assert rre.pl.iban("PL10987654320000000000000042,PL19123456781234567890123456") == [
        "PL10987654320000000000000042", "PL19123456781234567890123456"]
    assert rre.pl.iban("PL61 1090 1014 0000 0712 1981 2875") == []
    assert rre.pl.iban("PL61 1090 1014 0000 0712 1981 287") == []
    assert rre.pl.iban("PL61 1090 1014 0000 0712 1981 28741") == []
    assert rre.pl.iban("DE61 1090 1014 0000 0712 1981 2874") == []
    assert rre.pl.iban("XPL61109010140000071219812874") == []
    assert rre.pl.iban("pl61109010140000071219812874") == []


def test_hard_iccid():
    assert rre.pl.iccid("ICCID: 8948031111222233330") == ["8948031111222233330"]
    assert rre.pl.iccid("(89480698765432101239)") == ["89480698765432101239"]
    assert rre.pl.iccid("sim 894801555566667770.") == ["894801555566667770"]
    assert rre.pl.iccid('"8948021234567890126"') == ["8948021234567890126"]
    assert rre.pl.iccid("karta SIM 8948031111222233330 aktywna") == ["8948031111222233330"]
    assert rre.pl.iccid("8948031111222233330;89480698765432101239") == [
        "8948031111222233330", "89480698765432101239"]
    assert rre.pl.iccid("8948031111222233331") == []
    assert rre.pl.iccid("89480311112222333") == []
    assert rre.pl.iccid("894803111122223333012") == []
    assert rre.pl.iccid("8939031111222233330") == []
    assert rre.pl.iccid("x8948031111222233330") == []
    assert rre.pl.iccid("18948031111222233330") == []


def test_hard_id_card_number():
    assert rre.pl.id_card_number("AYZ723456") == ["AYZ723456"]
    assert rre.pl.id_card_number("dowód osobisty nr CAA 423456, ważny") == ["CAA 423456"]
    assert rre.pl.id_card_number("(DEF823456)") == ["DEF823456"]
    assert rre.pl.id_card_number('"XYZ 823456".') == ["XYZ 823456"]
    assert rre.pl.id_card_number("AYZ723456/DEF823456") == ["AYZ723456", "DEF823456"]
    assert rre.pl.id_card_number("seria i numer:\nCAA423456") == ["CAA423456"]
    assert rre.pl.id_card_number("AYZ723457") == []
    assert rre.pl.id_card_number("AYZ72345") == []
    assert rre.pl.id_card_number("AYZ7234567") == []
    assert rre.pl.id_card_number("AY723456") == []
    assert rre.pl.id_card_number("AAYZ723456") == []
    assert rre.pl.id_card_number("ayz723456") == []
    assert rre.pl.id_card_number("AYZ-723456") == []


def test_hard_imsi():
    assert rre.pl.imsi("IMSI 260011234567890") == ["260011234567890"]
    assert rre.pl.imsi("imsi:260031234567890") == ["260031234567890"]
    assert rre.pl.imsi("(260061234567890)") == ["260061234567890"]
    assert rre.pl.imsi('"260021234567890".') == ["260021234567890"]
    assert rre.pl.imsi("numer IMSI 260989876543210 karty") == ["260989876543210"]
    assert rre.pl.imsi("260011234567890,260031234567890") == ["260011234567890", "260031234567890"]
    assert rre.pl.imsi("26002123456789") == []
    assert rre.pl.imsi("2600212345678901") == []
    assert rre.pl.imsi("262021234567890") == []
    assert rre.pl.imsi("1260021234567890") == []
    assert rre.pl.imsi("x260021234567890") == []
    assert rre.pl.imsi("260021234567890x") == []


def test_hard_krs_number():
    assert rre.pl.krs_number("KRS nr 0000012345") == ["KRS nr 0000012345"]
    assert rre.pl.krs_number("KRS:0000098765") == ["KRS:0000098765"]
    assert rre.pl.krs_number("(KRS 0000111222)") == ["KRS 0000111222"]
    assert rre.pl.krs_number("wpisana do KRS pod numerem 0000222333") == ["KRS pod numerem 0000222333"]
    assert rre.pl.krs_number("Nr KRS 0000333444.") == ["KRS 0000333444"]
    assert rre.pl.krs_number("KRS pod nr. 0000444555") == ["KRS pod nr. 0000444555"]
    assert rre.pl.krs_number("KRS 000012345") == []
    assert rre.pl.krs_number("KRS 00001234567") == []
    assert rre.pl.krs_number("KRS-0000123456") == []
    assert rre.pl.krs_number("XKRS 0000123456") == []
    assert rre.pl.krs_number("REGON 0000123456") == []
    assert rre.pl.krs_number("KRS pod 0000123456") == []


def test_hard_license_plate():
    assert rre.pl.license_plate("PO-1234A") == ["PO-1234A"]
    assert rre.pl.license_plate("(GD 123AC)") == ["GD 123AC"]
    assert rre.pl.license_plate('"KR 1A234".') == ["KR 1A234"]
    assert rre.pl.license_plate("nr rej. DW 1AC23, kolor czarny") == ["DW 1AC23"]
    assert rre.pl.license_plate("WPI A123") == ["WPI A123"]
    assert rre.pl.license_plate("ZS12345") == ["ZS12345"]
    assert rre.pl.license_plate("WA 1234") == []
    assert rre.pl.license_plate("WA 123456") == []
    assert rre.pl.license_plate("SK 12AC") == []  # two-letter districts take five characters
    # A, I, M and X start no voivodeship code
    assert rre.pl.license_plate("XA 12345") == []
    # an autonomous system number and a camera file name
    assert rre.pl.license_plate("AS64496") == []
    assert rre.pl.license_plate("DSC01234.JPG") == []
    assert rre.pl.license_plate("IMG12345") == []
    assert rre.pl.license_plate("EN 12345") == []
    assert rre.pl.license_plate("wa 12345") == []
    assert rre.pl.license_plate("KRA 1C34X") == []


def test_hard_mobile_number():
    assert rre.pl.mobile_number("+48512345678") == ["+48512345678"]
    assert rre.pl.mobile_number("0048 600 123 456") == ["0048 600 123 456"]
    assert rre.pl.mobile_number("tel. kom. 790 123 456, dzwoń") == ["790 123 456"]
    assert rre.pl.mobile_number("(+48) 600 123 456") == ["600 123 456"]
    assert rre.pl.mobile_number("881-234-567") == ["881-234-567"]
    assert rre.pl.mobile_number('"+48 600-123-456".') == ["+48 600-123-456"]
    assert rre.pl.mobile_number("600123456") == []  # nine bare digits
    assert rre.pl.mobile_number("400 123 456") == []
    assert rre.pl.mobile_number("+48 22 123 45 67") == []
    assert rre.pl.mobile_number("1600 123 456") == []
    # foreign numbers whose national part looks Polish
    assert rre.pl.mobile_number("+49 600 123 456") == []
    assert rre.pl.mobile_number("+596 696 20 12 34") == []
    assert rre.pl.mobile_number("+40 722 123 456") == []
    assert rre.pl.mobile_number("0034 600 123 456") == []
    assert rre.pl.mobile_number("+40 (0) 722 123 456") == []  # Poland has no trunk 0


def test_hard_mrz_id_card():
    assert rre.pl.mrz_id_card("IDPOLAYZ1234562<<<<<<<<<<<<<<<") == ["IDPOLAYZ1234562<<<<<<<<<<<<<<<"]
    assert rre.pl.mrz_id_card('MRZ: "I<POLDEF1234563<<<<<<<<<<<<<<<"') == ["I<POLDEF1234563<<<<<<<<<<<<<<<"]
    assert rre.pl.mrz_id_card("(IDPOLZZC1082012<<<<<<<<<<<<<<<)") == ["IDPOLZZC1082012<<<<<<<<<<<<<<<"]
    assert rre.pl.mrz_id_card("IDPOLAYZ1234562<<<<<<<<<<<<<<<\n9005156F3105157POL<<<<<<<<<<<8") == [
        "IDPOLAYZ1234562<<<<<<<<<<<<<<<"]
    assert rre.pl.mrz_id_card("dowód: IDPOLZZC1082012<<<<<<<<<<<<<<<.") == ["IDPOLZZC1082012<<<<<<<<<<<<<<<"]
    assert rre.pl.mrz_id_card("IDPOLAYZ1234562<<<<<<<<<<<<<<<\nI<POLDEF1234563<<<<<<<<<<<<<<<") == [
        "IDPOLAYZ1234562<<<<<<<<<<<<<<<", "I<POLDEF1234563<<<<<<<<<<<<<<<"]
    assert rre.pl.mrz_id_card("IDPOLAYZ1234563<<<<<<<<<<<<<<<") == []
    assert rre.pl.mrz_id_card("IDPOLAYZ1234562<<<<<<<<<<<<<<") == []
    assert rre.pl.mrz_id_card("IDPOLAYZ1234562<<<<<<<<<<<<<<<<") == []
    assert rre.pl.mrz_id_card("IDDEUAYZ1234562<<<<<<<<<<<<<<<") == []
    assert rre.pl.mrz_id_card("PDPOLAYZ1234562<<<<<<<<<<<<<<<") == []
    assert rre.pl.mrz_id_card("idpolayz1234562<<<<<<<<<<<<<<<") == []


def test_hard_mrz_passport():
    line = "EA12345676POL9005156F3105157<<<<<<<<<<<<<<<8"
    assert rre.pl.mrz_passport(line) == [line]
    assert rre.pl.mrz_passport(f"P<POLKOWALSKA<<ANNA<<<<<<<<<<<<<<<<<<<<<<<<<\n{line}") == [line]
    # the specimen's PESEL in the personal number field
    assert rre.pl.mrz_passport("(ZZ30000014POL0101011M320101501210101354<<<64)") == [
        "ZZ30000014POL0101011M320101501210101354<<<64"]
    assert rre.pl.mrz_passport(f'mrz "{line}".') == [line]
    assert rre.pl.mrz_passport(f"strona 2: {line}, koniec") == [line]
    assert rre.pl.mrz_passport(line.replace("F31", "M31")) == [line.replace("F31", "M31")]
    assert rre.pl.mrz_passport(line.replace("76POL", "77POL")) == []
    assert rre.pl.mrz_passport(line.replace("9005156", "9005157")) == []
    assert rre.pl.mrz_passport(line.replace("3105157", "3105158")) == []
    assert rre.pl.mrz_passport(line.replace("POL", "CZE")) == []
    assert rre.pl.mrz_passport(line[:-1]) == []
    assert rre.pl.mrz_passport(line + "8") == []


def test_hard_msisdn():
    assert rre.pl.msisdn("MSISDN: 48512345678") == ["48512345678"]
    assert rre.pl.msisdn("(48790123456)") == ["48790123456"]
    assert rre.pl.msisdn('"48881234567".') == ["48881234567"]
    assert rre.pl.msisdn("48451234567") == ["48451234567"]
    assert rre.pl.msisdn("48600123456,48512345678") == ["48600123456", "48512345678"]
    assert rre.pl.msisdn("abonent 48530123456 dzwonił") == ["48530123456"]
    assert rre.pl.msisdn("+48600123456") == []
    assert rre.pl.msisdn("486001234567") == []
    assert rre.pl.msisdn("4860012345") == []
    assert rre.pl.msisdn("0048600123456") == []
    assert rre.pl.msisdn("48400123456") == []
    assert rre.pl.msisdn("x48600123456") == []
    assert rre.pl.msisdn("48 600 123 456") == []


def test_hard_nip():
    assert rre.pl.nip("NIP PL 5551234564") == ["NIP PL 5551234564"]
    assert rre.pl.nip("NIP: 987 654 32 10") == ["NIP: 987 654 32 10"]
    assert rre.pl.nip("(NIP 777-000-00-05)") == ["NIP 777-000-00-05"]
    assert rre.pl.nip('"987-654-32-10".') == ["987-654-32-10"]
    assert rre.pl.nip("NIP:9876543210") == ["NIP:9876543210"]
    assert rre.pl.nip("NIP nr 555-12-34-564") == ["NIP nr 555-12-34-564"]
    assert rre.pl.nip("firma 987-65-43-210 z siedzibą") == ["987-65-43-210"]
    assert rre.pl.nip("NIP 987654321") == []
    assert rre.pl.nip("NIP 98765432101") == []
    assert rre.pl.nip("987-654-32-10-1") == []
    assert rre.pl.nip("1-987-654-32-10") == []
    assert rre.pl.nip("9876543210") == []
    assert rre.pl.nip("NIP 987-654-32-11") == []
    assert rre.pl.nip("tel. 987-654-321") == []
    assert rre.pl.nip("2024-01-12-15") == []


def test_hard_nrb():
    assert rre.pl.nrb("19 1234 5678 1234 5678 9012 3456") == ["19 1234 5678 1234 5678 9012 3456"]
    assert rre.pl.nrb("nr rachunku: 10987654320000000000000042.") == ["10987654320000000000000042"]
    assert rre.pl.nrb("(61 1090 1014 0000 0712 1981 2874)") == ["61 1090 1014 0000 0712 1981 2874"]
    assert rre.pl.nrb('"61109010140000071219812874"') == ["61109010140000071219812874"]
    assert rre.pl.nrb("konto 19123456781234567890123456 w banku") == ["19123456781234567890123456"]
    assert rre.pl.nrb("10987654320000000000000042;61109010140000071219812874") == [
        "10987654320000000000000042", "61109010140000071219812874"]
    assert rre.pl.nrb("61 1090 1014 0000 0712 1981 2875") == []
    assert rre.pl.nrb("61 1090 1014 0000 0712 1981 287") == []
    assert rre.pl.nrb("611090101400000712198128741") == []
    assert rre.pl.nrb("PL61 1090 1014 0000 0712 1981 2874") == []  # an IBAN, not a bare NRB
    assert rre.pl.nrb("61 109 010 140 000 071 219 812 874") == []
    assert rre.pl.nrb("161 1090 1014 0000 0712 1981 2874") == []


def test_hard_passport_number():
    assert rre.pl.passport_number("EA1234567") == ["EA1234567"]
    assert rre.pl.passport_number("paszport nr EB 4234567, ważny") == ["EB 4234567"]
    assert rre.pl.passport_number("(AA3234567)") == ["AA3234567"]
    assert rre.pl.passport_number('"XY6234567".') == ["XY6234567"]
    assert rre.pl.passport_number("EA1234567/ZZ3000001") == ["EA1234567", "ZZ3000001"]
    assert rre.pl.passport_number("Paszport:\nEB4234567") == ["EB4234567"]
    assert rre.pl.passport_number("EA1234568") == []
    assert rre.pl.passport_number("EA123456") == []
    assert rre.pl.passport_number("EA12345678") == []
    assert rre.pl.passport_number("E1234567") == []
    assert rre.pl.passport_number("EAB1234567") == []
    assert rre.pl.passport_number("ea1234567") == []
    assert rre.pl.passport_number("EA-1234567") == []


def test_hard_pesel():
    assert rre.pl.pesel("PESEL: 44051401359") == ["44051401359"]
    assert rre.pl.pesel("(02210100121)") == ["02210100121"]  # born 1 January 2002
    assert rre.pl.pesel('"85091501230".') == ["85091501230"]
    assert rre.pl.pesel("nr PESEL 97810100019, ur. 1897") == ["97810100019"]  # month raised by 80
    assert rre.pl.pesel("00891234566") == ["00891234566"]
    assert rre.pl.pesel("99123112343,44051401359") == ["99123112343", "44051401359"]
    assert rre.pl.pesel("44051401358") == []
    assert rre.pl.pesel("4405140135") == []
    assert rre.pl.pesel("440514013591") == []
    assert rre.pl.pesel("00022900003") == []  # checksum fine, 29 February 1900
    assert rre.pl.pesel("85023000006") == []  # checksum fine, 30 February
    assert rre.pl.pesel("x44051401359") == []
    assert rre.pl.pesel("440 514 013 59") == []


def test_hard_phone_number():
    assert rre.pl.phone_number("0048 12 345 67 89") == ["0048 12 345 67 89"]
    assert rre.pl.phone_number("22-123-45-67") == ["22-123-45-67"]
    assert rre.pl.phone_number("+48221234567") == ["+48221234567"]
    assert rre.pl.phone_number("tel. (12) 345-67-89, fax") == ["(12) 345-67-89"]
    assert rre.pl.phone_number('"58 123 45 67".') == ["58 123 45 67"]
    assert rre.pl.phone_number("+48 600 123 456") == ["+48 600 123 456"]
    assert rre.pl.phone_number("221234567") == []
    assert rre.pl.phone_number("10 123 45 67") == []  # no area code 10
    assert rre.pl.phone_number("22 123 45 6") == []
    assert rre.pl.phone_number("22 123 45 678") == []
    # foreign numbers whose national part looks Polish
    assert rre.pl.phone_number("+49 22 123 45 67") == []
    assert rre.pl.phone_number("0034 81 012 34 56") == []
    assert rre.pl.phone_number("+352 698 12 34 56") == []
    assert rre.pl.phone_number("+40 (0) 722 123 456") == []
    assert rre.pl.phone_number("12-03-2024 22 123") == []


def test_hard_postal_code_city():
    assert rre.pl.postal_code_city("31-000 Kraków") == ["31-000 Kraków"]
    assert rre.pl.postal_code_city("(80-001 Gdańsk)") == ["80-001 Gdańsk"]
    assert rre.pl.postal_code_city("90-001 Łódź, ul. Piotrkowska") == ["90-001 Łódź"]
    assert rre.pl.postal_code_city("65-001 Zielona Góra") == ["65-001 Zielona Góra"]
    assert rre.pl.postal_code_city("adres: 33-300 Nowy Sącz.") == ["33-300 Nowy Sącz"]
    assert rre.pl.postal_code_city("77-400 Złotów") == ["77-400 Złotów"]
    assert rre.pl.postal_code_city("00-950 warszawa") == []
    assert rre.pl.postal_code_city("00950 Warszawa") == []
    assert rre.pl.postal_code_city("1-950 Warszawa") == []
    assert rre.pl.postal_code_city("000-950 Warszawa") == []
    assert rre.pl.postal_code_city("00-9500 Warszawa") == []
    assert rre.pl.postal_code_city("12-03-2024 Warszawa") == []
    assert rre.pl.postal_code_city("cena 10-100 PLN") == []
    assert rre.pl.postal_code_city("koszt 20-300 Zł") == []


def test_hard_regon():
    assert rre.pl.regon("REGON:012345675") == ["REGON:012345675"]
    assert rre.pl.regon("(REGON 987654326)") == ["REGON 987654326"]
    assert rre.pl.regon("REGON nr 555000119.") == ["REGON nr 555000119"]
    assert rre.pl.regon("REGON: 01234567500015, NIP") == ["REGON: 01234567500015"]
    assert rre.pl.regon('"REGON 98765432600029"') == ["REGON 98765432600029"]
    assert rre.pl.regon("REGON nr. 123456785") == ["REGON nr. 123456785"]
    assert rre.pl.regon("REGON 012345676") == []
    assert rre.pl.regon("REGON 01234567500016") == []
    assert rre.pl.regon("012345675") == []
    assert rre.pl.regon("REGON 1234567850") == []
    assert rre.pl.regon("REGON 12345678") == []
    assert rre.pl.regon("REGON 1234567851234") == []
    assert rre.pl.regon("XREGON 123456785") == []


def test_hard_street_address():
    assert rre.pl.street_address("al. Jerozolimskie 123A") == ["al. Jerozolimskie 123A"]
    assert rre.pl.street_address("pl. Defilad 1") == ["pl. Defilad 1"]
    assert rre.pl.street_address("Al. Solidarności 82 lok. 5") == ["Al. Solidarności 82 lok. 5"]
    assert rre.pl.street_address("ul. 3 Maja 10") == ["ul. 3 Maja 10"]
    assert rre.pl.street_address("ul. gen. Andersa 15") == ["ul. gen. Andersa 15"]
    assert rre.pl.street_address("UL. DŁUGA 5") == ["UL. DŁUGA 5"]
    assert rre.pl.street_address("(ul. Polna 7/2)") == ["ul. Polna 7/2"]
    assert rre.pl.street_address("adres: ul. Krakowska 12, 31-000 Kraków") == ["ul. Krakowska 12"]
    assert rre.pl.street_address("ul.Długa 5") == ["ul.Długa 5"]
    assert rre.pl.street_address("ul. Długa") == []
    assert rre.pl.street_address("Kowalski et al. 2019") == []
    assert rre.pl.street_address("dla 5 os. 3 pokoje") == []
    assert rre.pl.street_address("jan@onet.pl. Zobacz 5") == []
    assert rre.pl.street_address("ul. długa 5") == []
    assert rre.pl.street_address("ul. Długa 5/") == []
    assert rre.pl.street_address("formularz ul 5") == []


def test_hard_vat_number():
    assert rre.pl.vat_number("VAT-UE: PL9876543210") == ["PL9876543210"]
    assert rre.pl.vat_number("(PL5551234564)") == ["PL5551234564"]
    assert rre.pl.vat_number("NIP UE PL 9876543210.") == ["PL 9876543210"]
    assert rre.pl.vat_number('"PL 987-65-43-210"') == ["PL 987-65-43-210"]
    assert rre.pl.vat_number("PL777-000-00-05") == ["PL777-000-00-05"]
    assert rre.pl.vat_number("PL9876543210,PL5551234564") == ["PL9876543210", "PL5551234564"]
    assert rre.pl.vat_number("PL9876543211") == []
    assert rre.pl.vat_number("PL987654321") == []
    assert rre.pl.vat_number("PL98765432101") == []
    assert rre.pl.vat_number("PL61109010140000071219812874") == []
    assert rre.pl.vat_number("XPL9876543210") == []
    assert rre.pl.vat_number("pl9876543210") == []
    assert rre.pl.vat_number("DE9876543210") == []
