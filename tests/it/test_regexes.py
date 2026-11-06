from regular_regexes import rre


def test_codice_fiscale():
    assert rre.it.codice_fiscale("CF RSSMRA85T10A562S e RCCMNL83S18D969H") == ["RSSMRA85T10A562S", "RCCMNL83S18D969H"]
    # omocodia: the last digit replaced by a letter (9 -> V)
    assert rre.it.codice_fiscale("RCCMNL83S18D96VW") == ["RCCMNL83S18D96VW"]
    assert rre.it.codice_fiscale("RSSMRA85T10A562T") == []
    # right check letter, but 31 November does not exist
    assert rre.it.codice_fiscale("RCCMNL83S31D969Q") == []


def test_partita_iva():
    assert rre.it.partita_iva("P.IVA 07643520567 e 00743110157") == ["07643520567", "00743110157"]
    assert rre.it.partita_iva("07643520568") == []
    assert rre.it.partita_iva("12345675002") == []  # Luhn is right, office code 500 does not exist


def test_vat_number():
    assert rre.it.vat_number("IT07643520567 o IT 00743110157") == ["IT07643520567", "IT 00743110157"]
    assert rre.it.vat_number("IT07643520568") == []


def test_iban():
    assert rre.it.iban("IBAN IT60 X054 2811 1010 0000 0123 456 o IT60X0542811101000000123456") == [
        "IT60 X054 2811 1010 0000 0123 456", "IT60X0542811101000000123456"]
    assert rre.it.iban("IT60 X054 2811 1010 0000 0123 457") == []


def test_bic():
    assert rre.it.bic("BIC UNCRITMM o BCITITMMXXX") == ["UNCRITMM", "BCITITMMXXX"]
    assert rre.it.bic("BNPAFRPP") == []


def test_id_card_number():
    assert rre.it.id_card_number("CIE n. CA00000AA") == ["CA00000AA"]
    assert rre.it.id_card_number("CA0000AA e CA000000AA") == []


def test_passport_number():
    assert rre.it.passport_number("passaporto n. YA1234567 e PASSPORT: YB7654321") == ["YA1234567", "YB7654321"]
    assert rre.it.passport_number("passaporto YA123456 e YAB1234567") == []


def test_mrz_id_card():
    line = "CIITACA00000AA4" + "<" * 15
    assert rre.it.mrz_id_card(f"mrz {line}") == [line]
    assert rre.it.mrz_id_card("CIITACA00000AA5" + "<" * 15) == []


def test_mrz_passport():
    # ICAO 9303 specimen with ITA nationality
    line = "L898902C36ITA7408122F1204159ZE184226B<<<<<10"
    assert rre.it.mrz_passport(line) == [line]
    assert rre.it.mrz_passport(line.replace("C36", "C37")) == []


def test_phone_number():
    # example numbers from libphonenumber's metadata: Italy has no range reserved for fiction
    assert rre.it.phone_number("tel 02 1234 5678, +39 02 12345678, 312 345 6789 o 0571 123456") == [
        "02 1234 5678", "+39 02 12345678", "312 345 6789", "0571 123456"]
    assert rre.it.phone_number("il 01/02/2024, orario 08.30-12.30, +3531234567") == []
    # a Belgian KBO number and the digit groups of an IBAN
    assert rre.it.phone_number("KBO 0123.456.749, IBAN DE89 3704 0044 0532 0130 00") == []


def test_mobile_number():
    assert rre.it.mobile_number("cell +39 312 345 6789, 3123456789 o 312/3456789") == [
        "+39 312 345 6789", "3123456789", "312/3456789"]
    assert rre.it.mobile_number("02 1234 5678 e 32470123456") == []


def test_premium_number():
    assert rre.it.premium_number("chiama 899 123 456 o 899123456") == ["899 123 456", "899123456"]
    assert rre.it.premium_number("verde 800 123 456, € 899.000") == []


def test_msisdn():
    assert rre.it.msisdn("msisdn 393123456789") == ["393123456789"]
    assert rre.it.msisdn("390212345678") == []


def test_imsi():
    assert rre.it.imsi("imsi 222011234567890") == ["222011234567890"]
    assert rre.it.imsi("imsi 214011234567890") == []


def test_iccid():
    assert rre.it.iccid("sim 8939011234567890127") == ["8939011234567890127"]
    assert rre.it.iccid("sim 8939011234567890128") == []


def test_license_plate():
    assert rre.it.license_plate("targa AB 123 CD ed EF456GH") == ["AB 123 CD", "EF456GH"]
    assert rre.it.license_plate("AI 123 CD, AB 1234 CD") == []


def test_postal_code_city():
    assert rre.it.postal_code_city("00184 Roma e 20121 Milano (MI)") == ["00184 Roma", "20121 Milano (MI)"]
    assert rre.it.postal_code_city("40017 San Giovanni in Persiceto (BO), 42121 Reggio nell'Emilia") == [
        "40017 San Giovanni in Persiceto (BO)", "42121 Reggio nell'Emilia"]
    assert rre.it.postal_code_city("10000 Euro, 2024 Roma") == []


def test_street_address():
    assert rre.it.street_address("abita in Via Roma 1, Milano") == ["Via Roma 1"]
    assert rre.it.street_address("Via Giuseppe Garibaldi, 12/A e Piazza della Repubblica n. 5") == [
        "Via Giuseppe Garibaldi, 12/A", "Piazza della Repubblica n. 5"]
    assert rre.it.street_address("Corso Vittorio Emanuele II 23") == ["Corso Vittorio Emanuele II 23"]
    assert rre.it.street_address("via email 3 volte, Via libera a 2 decreti") == []


def test_company_name():
    assert rre.it.company_name("tra Rossi Costruzioni S.r.l. e Fiat S.p.A.") == ["Rossi Costruzioni S.r.l.", "Fiat S.p.A."]
    assert rre.it.company_name("Bianchi & C. S.n.c. e ROSSI SRL") == ["Bianchi & C. S.n.c.", "ROSSI SRL"]
    assert rre.it.company_name("la srl di Mario") == []


def test_ecli():
    assert rre.it.ecli("vedi ECLI:IT:CASS:2016:12345CIV.") == ["ECLI:IT:CASS:2016:12345CIV"]
    assert rre.it.ecli("ECLI:ES:TS:2015:1234") == []


def test_aircraft_registration():
    assert rre.it.aircraft_registration("aereo I-ABCD") == ["I-ABCD"]
    assert rre.it.aircraft_registration("I-ABC e HI-ABCD") == []


def test_hard_aircraft_registration():
    assert rre.it.aircraft_registration("I-EIXM") == ["I-EIXM"]
    assert rre.it.aircraft_registration("l'aereo I-ADJK è atterrato a Linate") == ["I-ADJK"]
    assert rre.it.aircraft_registration("(I-DEMO)") == ["I-DEMO"]
    assert rre.it.aircraft_registration('marche "I-BIXA".') == ["I-BIXA"]
    assert rre.it.aircraft_registration("I-AAAA,I-ZZZZ") == ["I-AAAA", "I-ZZZZ"]
    assert rre.it.aircraft_registration("elicottero\nI-HELI") == ["I-HELI"]
    assert rre.it.aircraft_registration("I-ABC") == []
    assert rre.it.aircraft_registration("I-ABCDE") == []
    assert rre.it.aircraft_registration("HI-ABCD") == []  # Dominican Republic
    assert rre.it.aircraft_registration("I-ABC1") == []
    assert rre.it.aircraft_registration("IABCD") == []
    assert rre.it.aircraft_registration("i-abcd") == []
    assert rre.it.aircraft_registration("D-ABCD") == []


def test_hard_bic():
    assert rre.it.bic("ABCDIT22XXX") == ["ABCDIT22XXX"]
    assert rre.it.bic("(WXYZIT2P)") == ["WXYZIT2P"]
    assert rre.it.bic('bic: "QWERIT21"') == ["QWERIT21"]
    assert rre.it.bic("UNCRITMM.") == ["UNCRITMM"]
    assert rre.it.bic("SWIFT ABCDITMMXXX, IBAN") == ["ABCDITMMXXX"]
    assert rre.it.bic("codice BIC:ZZZZITRR del conto") == ["ZZZZITRR"]
    assert rre.it.bic("UNCRITM") == []
    assert rre.it.bic("UNCRITMMX") == []
    assert rre.it.bic("UNCRITMMXX") == []
    assert rre.it.bic("UNCRITMMXXXX") == []
    assert rre.it.bic("UNCRFRMM") == []
    assert rre.it.bic("UNC1ITMM") == []
    assert rre.it.bic("uncritmm") == []


def test_hard_codice_fiscale():
    # also written in lowercase, as in e-mail addresses and forms
    assert rre.it.codice_fiscale("rssmra85t10a562s") == ["rssmra85t10a562s"]
    # a woman: 40 added to the day
    assert rre.it.codice_fiscale("CF: BNCLRA70A41H501B.") == ["BNCLRA70A41H501B"]
    assert rre.it.codice_fiscale("(VRDGPP80E52F205P)") == ["VRDGPP80E52F205P"]
    assert rre.it.codice_fiscale('"RSSMRA85T10A56NH"') == ["RSSMRA85T10A56NH"]
    assert rre.it.codice_fiscale("codice fiscale RSSMRA85T10A5S2E, nato a Roma") == ["RSSMRA85T10A5S2E"]
    assert rre.it.codice_fiscale("RSSMRA85T31A562T;BNCLRA70A41H501B") == ["RSSMRA85T31A562T", "BNCLRA70A41H501B"]
    assert rre.it.codice_fiscale("RSSMRA85T10A562") == []
    assert rre.it.codice_fiscale("RSSMRA85T10A562SX") == []
    assert rre.it.codice_fiscale("XRSSMRA85T10A562S") == []
    assert rre.it.codice_fiscale("RSSMRA85F10A562S") == []  # F is no month
    assert rre.it.codice_fiscale("BNCLRA70A72H501B") == []  # day 72: a woman born on the 32nd
    assert rre.it.codice_fiscale("BNCLRA70B70H501E") == []  # right check letter, 30 February
    assert rre.it.codice_fiscale("RSSMRA85T10A562Z") == []
    assert rre.it.codice_fiscale("RSSMRA8XT10A562S") == []  # X is no omocodia letter


def test_hard_company_name():
    assert rre.it.company_name("Rossi Srl") == ["Rossi Srl"]
    assert rre.it.company_name("(Bianchi S.p.A.)") == ["Bianchi S.p.A."]
    assert rre.it.company_name('"Verdi Costruzioni s.r.l."') == ["Verdi Costruzioni s.r.l."]
    assert rre.it.company_name("Mario Rossi & C. S.a.s.") == ["Mario Rossi & C. S.a.s."]
    assert rre.it.company_name("Rossi e figli S.n.c.") == ["Rossi e figli S.n.c."]
    assert rre.it.company_name("Cooperativa Agricola Soc. Coop.") == ["Cooperativa Agricola Soc. Coop."]
    assert rre.it.company_name("Alfa Servizi S.c.a.r.l., con sede a Roma") == ["Alfa Servizi S.c.a.r.l."]
    assert rre.it.company_name("Banca di Roma S.p.A.") == ["Banca di Roma S.p.A."]
    assert rre.it.company_name("Rossi Spazio") == []
    assert rre.it.company_name("rossi s.r.l.") == []
    assert rre.it.company_name("S.r.l.") == []
    assert rre.it.company_name("Rossi Srlx") == []
    assert rre.it.company_name("Rossi S.r") == []
    assert rre.it.company_name("una spa di lusso") == []
    assert rre.it.company_name("La società Rossi è una srl") == []


def test_hard_ecli():
    assert rre.it.ecli("ECLI:IT:COST:2015:1") == ["ECLI:IT:COST:2015:1"]
    assert rre.it.ecli("(ECLI:IT:CDS:2019:1234SENT)") == ["ECLI:IT:CDS:2019:1234SENT"]
    assert rre.it.ecli("sentenza ECLI:IT:CASS:2020:98765PEN, depositata") == ["ECLI:IT:CASS:2020:98765PEN"]
    assert rre.it.ecli('"ECLI:IT:TARLAZ:2018:123."') == ["ECLI:IT:TARLAZ:2018:123"]
    assert rre.it.ecli("ECLI:IT:CASS:2016:12345.CIV") == ["ECLI:IT:CASS:2016:12345.CIV"]
    assert rre.it.ecli("ECLI:IT:COST:2015:1;ECLI:IT:COST:2015:2") == ["ECLI:IT:COST:2015:1", "ECLI:IT:COST:2015:2"]
    assert rre.it.ecli("ECLI:IT:CASS:16:12345") == []
    assert rre.it.ecli("ECLI:FR:CC:2016:123") == []
    assert rre.it.ecli("ECLI:IT::2016:1") == []
    assert rre.it.ecli("ECLI:IT:CASS:2016:") == []
    assert rre.it.ecli("ECLI IT CASS 2016 1") == []
    assert rre.it.ecli("XECLI:IT:CASS:2016:1") == []
    assert rre.it.ecli("ECLI:IT:CASS:20161:1") == []


def test_hard_iban():
    assert rre.it.iban("IBAN: IT13X1234567890000012345678") == ["IT13X1234567890000012345678"]
    assert rre.it.iban("IT36 Q111 1122 2220 0000 0098 765") == ["IT36 Q111 1122 2220 0000 0098 765"]
    # grouped as CIN, ABI, CAB and account number
    assert rre.it.iban("(IT13 X 12345 67890 000012345678)") == ["IT13 X 12345 67890 000012345678"]
    assert rre.it.iban("conto IT60X0542811101000000123456.") == ["IT60X0542811101000000123456"]
    assert rre.it.iban('"IT36Q1111122222000000098765"') == ["IT36Q1111122222000000098765"]
    assert rre.it.iban("IT13X1234567890000012345678 BIC ABCDITMM") == ["IT13X1234567890000012345678"]
    assert rre.it.iban("IT60 X054 2811 1010 0000 0123 45") == []
    assert rre.it.iban("IT60 X054 2811 1010 0000 0123 4567") == []
    assert rre.it.iban("IT61 X054 2811 1010 0000 0123 456") == []
    assert rre.it.iban("SM60 X054 2811 1010 0000 0123 456") == []
    assert rre.it.iban("XIT60X0542811101000000123456") == []
    assert rre.it.iban("IT60 1054 2811 1010 0000 0123 456") == []  # the CIN is a letter
    assert rre.it.iban("IT60X05428111010000001234567890") == []


def test_hard_iccid():
    assert rre.it.iccid("ICCID: 8939019876543210986") == ["8939019876543210986"]
    assert rre.it.iccid("(89391022334455667786)") == ["89391022334455667786"]
    assert rre.it.iccid("sim 893988112233445565.") == ["893988112233445565"]
    assert rre.it.iccid('"8939019876543210986"') == ["8939019876543210986"]
    assert rre.it.iccid("8939011234567890127,8939019876543210986") == ["8939011234567890127", "8939019876543210986"]
    assert rre.it.iccid("la SIM 89391022334455667786 è attiva") == ["89391022334455667786"]
    assert rre.it.iccid("8939019876543210985") == []
    assert rre.it.iccid("89390198765432109") == []
    assert rre.it.iccid("893901987654321098612") == []
    assert rre.it.iccid("8949019876543210986") == []
    assert rre.it.iccid("x8939019876543210986") == []
    assert rre.it.iccid("98939019876543210986") == []


def test_hard_id_card_number():
    assert rre.it.id_card_number("CA12345AB") == ["CA12345AB"]
    assert rre.it.id_card_number("carta d'identità n. CB98765ZZ, rilasciata") == ["CB98765ZZ"]
    assert rre.it.id_card_number("(CA00000AA)") == ["CA00000AA"]
    assert rre.it.id_card_number('"CC11111DD".') == ["CC11111DD"]
    assert rre.it.id_card_number("CIE:CA54321XY") == ["CA54321XY"]
    assert rre.it.id_card_number("CA12345AB/CB98765ZZ") == ["CA12345AB", "CB98765ZZ"]
    assert rre.it.id_card_number("C00000AA") == []
    assert rre.it.id_card_number("CA00000A") == []
    assert rre.it.id_card_number("CA00000AAA") == []
    assert rre.it.id_card_number("XCA00000AA") == []
    assert rre.it.id_card_number("ca00000aa") == []
    assert rre.it.id_card_number("CA0000AAA") == []
    assert rre.it.id_card_number("CA000000A") == []


def test_hard_imsi():
    assert rre.it.imsi("IMSI 222101234567890") == ["222101234567890"]
    assert rre.it.imsi("imsi:222881234567890") == ["222881234567890"]
    assert rre.it.imsi("(222501234567890)") == ["222501234567890"]
    assert rre.it.imsi('"222011234567890".') == ["222011234567890"]
    assert rre.it.imsi("l'IMSI 222019876543210 risulta attivo") == ["222019876543210"]
    assert rre.it.imsi("222101234567890;222881234567890") == ["222101234567890", "222881234567890"]
    assert rre.it.imsi("22201123456789") == []
    assert rre.it.imsi("2220112345678901") == []
    assert rre.it.imsi("226011234567890") == []
    assert rre.it.imsi("1222011234567890") == []
    assert rre.it.imsi("x222011234567890") == []
    assert rre.it.imsi("222011234567890x") == []


def test_hard_license_plate():
    assert rre.it.license_plate("AB-123-CD") == ["AB-123-CD"]
    assert rre.it.license_plate("targa: ZZ 999 ZZ") == ["ZZ 999 ZZ"]
    assert rre.it.license_plate("(FG 210 KL)") == ["FG 210 KL"]
    assert rre.it.license_plate('"GH789JK".') == ["GH789JK"]
    assert rre.it.license_plate("rimorchio XA 123 BC") == ["XA 123 BC"]
    assert rre.it.license_plate("auto AB 123 CD e moto") == ["AB 123 CD"]
    assert rre.it.license_plate("AB 12 CD") == []
    assert rre.it.license_plate("AO 123 CD") == []  # no O
    assert rre.it.license_plate("AB 123 CU") == []  # no U
    assert rre.it.license_plate("AQ 123 CD") == []  # no Q
    assert rre.it.license_plate("AB123CDE") == []
    assert rre.it.license_plate("XAB123CD") == []
    assert rre.it.license_plate("AB 123 C") == []
    assert rre.it.license_plate("ab123cd") == []


def test_hard_mobile_number():
    assert rre.it.mobile_number("0039 333 1234567") == ["0039 333 1234567"]
    assert rre.it.mobile_number("+39.347.123.4567") == ["+39.347.123.4567"]
    assert rre.it.mobile_number("(+39) 333 1234567") == ["333 1234567"]
    assert rre.it.mobile_number("333-123 4567") == ["333-123 4567"]
    assert rre.it.mobile_number("cell. 320 12 34 567, ore pasti") == ["320 12 34 567"]
    assert rre.it.mobile_number("sms al 3331234567.") == ["3331234567"]
    assert rre.it.mobile_number("333 123456") == ["333 123456"]  # nine digits
    assert rre.it.mobile_number("300 123 4567") == []
    assert rre.it.mobile_number("312 345 678") == []
    assert rre.it.mobile_number("312 345 67890") == []
    assert rre.it.mobile_number("+41 312 345 6789") == []
    assert rre.it.mobile_number("x3123456789") == []
    assert rre.it.mobile_number("13123456789") == []
    # an amount in euro
    assert rre.it.mobile_number("€ 333.456.789,00") == []
    assert rre.it.mobile_number("31/12/2024 10:30") == []


def test_hard_mrz_id_card():
    assert rre.it.mrz_id_card("CIITACA12345AB8<<<<<<<<<<<<<<<") == ["CIITACA12345AB8<<<<<<<<<<<<<<<"]
    assert rre.it.mrz_id_card('MRZ: "CIITACB98765ZZ4<<<<<<<<<<<<<<<"') == ["CIITACB98765ZZ4<<<<<<<<<<<<<<<"]
    assert rre.it.mrz_id_card("C<ITACA00000AA4<<<<<<<<<<<<<<<") == ["C<ITACA00000AA4<<<<<<<<<<<<<<<"]
    assert rre.it.mrz_id_card("IDITAAB12345671<<<<<<<<<<<<<<<") == ["IDITAAB12345671<<<<<<<<<<<<<<<"]
    assert rre.it.mrz_id_card("CIITACA12345AB8<<<<<<<<<<<<<<<\n8501019M3001019ITA<<<<<<<<<<<0") == [
        "CIITACA12345AB8<<<<<<<<<<<<<<<"]
    assert rre.it.mrz_id_card("(CIITACB98765ZZ4<<<<<<<<<<<<<<<)") == ["CIITACB98765ZZ4<<<<<<<<<<<<<<<"]
    assert rre.it.mrz_id_card("CIITACA12345AB9<<<<<<<<<<<<<<<") == []
    assert rre.it.mrz_id_card("CIITACA12345AB8<<<<<<<<<<<<<<") == []
    assert rre.it.mrz_id_card("CIITACA12345AB8<<<<<<<<<<<<<<<<") == []
    assert rre.it.mrz_id_card("CIFRACA12345AB8<<<<<<<<<<<<<<<") == []
    assert rre.it.mrz_id_card("PIITACA12345AB8<<<<<<<<<<<<<<<") == []
    assert rre.it.mrz_id_card("ciitaca12345ab8<<<<<<<<<<<<<<<") == []
    assert rre.it.mrz_id_card("<CIITACA12345AB8<<<<<<<<<<<<<<<") == []


def test_hard_mrz_passport():
    line = "YA12345676ITA8501019M3001019<<<<<<<<<<<<<<<0"
    assert rre.it.mrz_passport(line) == [line]
    assert rre.it.mrz_passport(f"P<ITAROSSI<<MARIO<<<<<<<<<<<<<<<<<<<<<<<<<<<\n{line}") == [line]
    assert rre.it.mrz_passport("YB76543217ITA9212314F3206308<<<<<<<<<<<<<<<2") == [
        "YB76543217ITA9212314F3206308<<<<<<<<<<<<<<<2"]
    # sex unspecified, birth date with unknown month and day, codice fiscale in the personal number field
    assert rre.it.mrz_passport("(AA00000011ITA0002299<2912316RSSMRA85T10A5668)") == [
        "AA00000011ITA0002299<2912316RSSMRA85T10A5668"]
    assert rre.it.mrz_passport(f'mrz "{line}".') == [line]
    assert rre.it.mrz_passport(f"{line}\nYB76543217ITA9212314F3206308<<<<<<<<<<<<<<<2") == [
        line, "YB76543217ITA9212314F3206308<<<<<<<<<<<<<<<2"]
    assert rre.it.mrz_passport(line.replace("76ITA", "77ITA")) == []  # document number check digit
    assert rre.it.mrz_passport(line.replace("8501019", "8501018")) == []  # birth date check digit
    assert rre.it.mrz_passport(line.replace("3001019", "3001018")) == []  # expiry date check digit
    assert rre.it.mrz_passport(line.replace("ITA", "FRA")) == []
    assert rre.it.mrz_passport(line[:-1]) == []
    assert rre.it.mrz_passport(line + "1") == []
    assert rre.it.mrz_passport(line.replace("9M", "9Z")) == []


def test_hard_msisdn():
    assert rre.it.msisdn("MSISDN: 393331234567") == ["393331234567"]
    assert rre.it.msisdn("(393471234567)") == ["393471234567"]
    assert rre.it.msisdn("39333123456") == ["39333123456"]  # nine-digit mobile number
    assert rre.it.msisdn('"393201234567".') == ["393201234567"]
    assert rre.it.msisdn("393123456789,393331234567") == ["393123456789", "393331234567"]
    assert rre.it.msisdn("chiamante 393401234567 alle 10:15") == ["393401234567"]
    # with a + it is an E.164 number, not an MSISDN
    assert rre.it.msisdn("+393123456789") == []
    assert rre.it.msisdn("39312345678") == []
    assert rre.it.msisdn("3931234567890") == []
    assert rre.it.msisdn("0039312345678") == []
    assert rre.it.msisdn("39 312 345 6789") == []
    assert rre.it.msisdn("x393123456789") == []
    assert rre.it.msisdn("393001234567") == []


def test_hard_partita_iva():
    assert rre.it.partita_iva("P.IVA: 12345670017") == ["12345670017"]
    assert rre.it.partita_iva("(00000011007)") == ["00000011007"]
    assert rre.it.partita_iva("C.F./P.IVA 98765431204.") == ["98765431204"]
    assert rre.it.partita_iva('"55555558885"') == ["55555558885"]
    assert rre.it.partita_iva("partita IVA n. 01234569992 del cliente") == ["01234569992"]
    assert rre.it.partita_iva("07654320881,00743110157") == ["07654320881", "00743110157"]
    assert rre.it.partita_iva("12345670018") == []
    assert rre.it.partita_iva("1234567001") == []
    assert rre.it.partita_iva("123456700171") == []
    assert rre.it.partita_iva("00000000000") == []
    assert rre.it.partita_iva("12345675008") == []  # Luhn fine, office code 500
    assert rre.it.partita_iva("12345670009") == []  # Luhn fine, office code 000
    assert rre.it.partita_iva("x12345670017") == []
    assert rre.it.partita_iva("123 4567 0017") == []


def test_hard_passport_number():
    assert rre.it.passport_number("AA0000001") == ["AA0000001"]
    assert rre.it.passport_number("passaporto n. YC1112223, scadenza 2030") == ["YC1112223"]
    assert rre.it.passport_number("(YD7654321)") == ["YD7654321"]
    assert rre.it.passport_number('"YA9876543".') == ["YA9876543"]
    assert rre.it.passport_number("PASSAPORTO:YB0000123") == ["YB0000123"]
    assert rre.it.passport_number("YA1234567/YB7654321") == ["YA1234567", "YB7654321"]
    assert rre.it.passport_number("YA123456") == []
    assert rre.it.passport_number("YA12345678") == []
    assert rre.it.passport_number("Y1234567") == []
    assert rre.it.passport_number("YAB1234567") == []
    assert rre.it.passport_number("ya1234567") == []
    assert rre.it.passport_number("XYA1234567") == []
    assert rre.it.passport_number("YA1234567X") == []


def test_hard_phone_number():
    assert rre.it.phone_number("0039 06 6982 1234") == ["0039 06 6982 1234"]
    assert rre.it.phone_number("06/1234567") == ["06/1234567"]
    assert rre.it.phone_number("011.1234567") == ["011.1234567"]
    assert rre.it.phone_number("(02) 1234 5678") == ["(02) 1234 5678"]
    assert rre.it.phone_number("tel. 055-123456, fax 055-654321") == ["055-123456", "055-654321"]
    assert rre.it.phone_number("+39 0571 123456.") == ["+39 0571 123456"]
    assert rre.it.phone_number("+39 3123456789") == ["+39 3123456789"]
    assert rre.it.phone_number("800 123 456") == []  # toll free
    assert rre.it.phone_number("02 1234") == []
    assert rre.it.phone_number("02 1234 5678 9012") == []
    assert rre.it.phone_number("+41 02 1234 5678") == []
    assert rre.it.phone_number("x0212345678") == []
    # eleven digits in a row: a partita IVA or a Belgian national number rather than a landline
    assert rre.it.phone_number("05073003326") == []
    # the bank code and digits of a Dutch IBAN
    assert rre.it.phone_number("NL91 ABNA 0417 1643 00") == []
    assert rre.it.phone_number("€ 333.456.789,00") == []
    assert rre.it.phone_number("ore 10.30-12.30 del 12/03/2024") == []


def test_hard_postal_code_city():
    assert rre.it.postal_code_city("Via Roma 1, 00184 Roma RM") == ["00184 Roma RM"]
    assert rre.it.postal_code_city("(10121 Torino)") == ["10121 Torino"]
    assert rre.it.postal_code_city("CAP 34121 Trieste.") == ["34121 Trieste"]
    assert rre.it.postal_code_city("I-20121 Milano") == ["20121 Milano"]
    assert rre.it.postal_code_city("00184 ROMA (RM)") == ["00184 ROMA (RM)"]
    assert rre.it.postal_code_city("00120 Città del Vaticano") == ["00120 Città del Vaticano"]
    assert rre.it.postal_code_city("20121 Milano Tel. 02 1234 5678") == ["20121 Milano"]
    assert rre.it.postal_code_city("50000 USD") == []
    assert rre.it.postal_code_city("15000 Lire") == []
    assert rre.it.postal_code_city("123456 Roma") == []
    assert rre.it.postal_code_city("00184 roma") == []
    assert rre.it.postal_code_city("00184Roma") == []
    assert rre.it.postal_code_city("00184 EUR") == []
    assert rre.it.postal_code_city("1234 Roma") == []


def test_hard_premium_number():
    assert rre.it.premium_number("899.123.456") == ["899.123.456"]
    assert rre.it.premium_number("(899-123-456)") == ["899-123-456"]
    assert rre.it.premium_number("chiama l'899 12 34 56 ora") == ["899 12 34 56"]
    assert rre.it.premium_number("8945 1234") == ["8945 1234"]
    assert rre.it.premium_number("895 512 3456") == ["895 512 3456"]
    assert rre.it.premium_number("8955123456") == ["8955123456"]
    assert rre.it.premium_number("894 123 4567") == []
    assert rre.it.premium_number("899 12 345") == []
    assert rre.it.premium_number("899 123 4567") == []
    assert rre.it.premium_number("1899 123 456") == []
    assert rre.it.premium_number("+899123456") == []
    assert rre.it.premium_number("892 123 456") == []
    assert rre.it.premium_number("899123456789") == []


def test_hard_street_address():
    # the street word is written in lowercase in running text, in capitals in some registers
    assert rre.it.street_address("abito in via Roma 12") == ["via Roma 12"]
    assert rre.it.street_address("VIA ROMA 12") == ["VIA ROMA 12"]
    assert rre.it.street_address("V.le Monza 120") == ["V.le Monza 120"]
    assert rre.it.street_address("C.so Buenos Aires, 33") == ["C.so Buenos Aires, 33"]
    assert rre.it.street_address("Via dell'Indipendenza 12") == ["Via dell'Indipendenza 12"]
    assert rre.it.street_address("(Largo Augusto 3)") == ["Largo Augusto 3"]
    assert rre.it.street_address('"Vicolo Stretto 5/B".') == ["Vicolo Stretto 5/B"]
    assert rre.it.street_address("Via 20 Settembre 5 bis") == ["Via 20 Settembre 5 bis"]
    assert rre.it.street_address("piazza 1° Maggio 4") == ["piazza 1° Maggio 4"]
    assert rre.it.street_address("Via Roma, 20121 Milano") == []  # no house number
    assert rre.it.street_address("Via Roma") == []
    assert rre.it.street_address("Via Roma 12345") == []
    assert rre.it.street_address("Viabilità 12") == []
    assert rre.it.street_address("Corso di inglese 3") == []
    assert rre.it.street_address("inviato via WhatsApp 3 volte") == []
    assert rre.it.street_address("via e-mail 2 volte") == []
    assert rre.it.street_address("andato via 3 volte in 2 anni") == []


def test_hard_vat_number():
    assert rre.it.vat_number("P.IVA IT00743110157") == ["IT00743110157"]
    assert rre.it.vat_number("(IT07643520567)") == ["IT07643520567"]
    assert rre.it.vat_number("VAT: IT 12345670017.") == ["IT 12345670017"]
    assert rre.it.vat_number('"IT98765431204"') == ["IT98765431204"]
    assert rre.it.vat_number("partita IVA IT01234569992 del fornitore") == ["IT01234569992"]
    assert rre.it.vat_number("IT55555558885,IT00000011007") == ["IT55555558885", "IT00000011007"]
    assert rre.it.vat_number("IT12345670018") == []
    assert rre.it.vat_number("IT1234567001") == []
    assert rre.it.vat_number("IT123456700171") == []
    assert rre.it.vat_number("IT12345675008") == []  # office code 500
    assert rre.it.vat_number("XIT12345670017") == []
    assert rre.it.vat_number("FR12345670017") == []
    assert rre.it.vat_number("it12345670017") == []
    assert rre.it.vat_number("IT 123 4567 0017") == []
