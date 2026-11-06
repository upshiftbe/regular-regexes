from regular_regexes import rre


def test_dni():
    # 99999999R is the specimen DNI
    assert rre.es.dni("DNI 12345678Z, 12.345.678-Z y 99999999R") == ["12345678Z", "12.345.678-Z", "99999999R"]
    assert rre.es.dni("12345678A") == []
    assert rre.es.dni("123456789Z") == []


def test_nie():
    assert rre.es.nie("NIE X1234567L o Y-1234567-X") == ["X1234567L", "Y-1234567-X"]
    assert rre.es.nie("X1234567M") == []
    assert rre.es.nie("W1234567L") == []


def test_cif():
    assert rre.es.cif("CIF B-12345674 y J99216582") == ["B-12345674", "J99216582"]
    assert rre.es.cif("Q1234567D") == ["Q1234567D"]  # control as a letter
    assert rre.es.cif("B12345675") == []
    assert rre.es.cif("I12345674") == []


def test_vat_number():
    assert rre.es.vat_number("NIF-IVA ESB12345674, ES12345678Z, ESX1234567L") == [
        "ESB12345674", "ES12345678Z", "ESX1234567L"]
    assert rre.es.vat_number("ESB12345675") == []
    assert rre.es.vat_number("ES1234567Z") == []


def test_social_security_number():
    assert rre.es.social_security_number("NSS 28/12345678/40 y 281234567840") == ["28/12345678/40", "281234567840"]
    # a number below 10 000 000 is counted without its leading zero, also in the old 11-digit form
    assert rre.es.social_security_number("08 01234567 74 o 28/1234567/42") == ["08 01234567 74", "28/1234567/42"]
    assert rre.es.social_security_number("281234567841") == []
    assert rre.es.social_security_number("991234567840") == []  # no province 99


def test_iban():
    assert rre.es.iban("IBAN ES91 2100 0418 4502 0005 1332 o ES91 2100 0418 45 0200051332") == [
        "ES91 2100 0418 4502 0005 1332", "ES91 2100 0418 45 0200051332"]
    assert rre.es.iban("ES91 2100 0418 4502 0005 1333") == []
    assert rre.es.iban("NL91ABNA0417164300") == []


def test_bic():
    assert rre.es.bic("BIC CAIXESBBXXX o BSCHESMM") == ["CAIXESBBXXX", "BSCHESMM"]
    assert rre.es.bic("GEBABEBB") == []


def test_passport_number():
    assert rre.es.passport_number("nº de pasaporte PAA123456, Passport No. XDA654321") == ["PAA123456", "XDA654321"]
    assert rre.es.passport_number("pasaporte PA123456 y PAA1234567") == []


def test_mrz_id_card():
    # DNI 3.0 specimen: support number BAA000589, DNI 99999999R in the optional field
    line = "IDESPBAA000589599999999R<<<<<<"
    assert rre.es.mrz_id_card(f"mrz {line}") == [line]
    assert rre.es.mrz_id_card(line[:14] + "6" + line[15:]) == []  # check digit 5 changed
    assert rre.es.mrz_id_card(line.replace("ESP", "ITA")) == []


def test_mrz_passport():
    # ICAO 9303 specimen with ESP nationality
    line = "L898902C36ESP7408122F1204159ZE184226B<<<<<10"
    assert rre.es.mrz_passport(line) == [line]
    assert rre.es.mrz_passport(line.replace("C36", "C37")) == []


def test_phone_number():
    # example numbers from libphonenumber's metadata: Spain has no range reserved for fiction
    assert rre.es.phone_number("llama al +34 612 34 56 78, al 810 123 456 o al 0034 81 012 34 56") == [
        "+34 612 34 56 78", "810 123 456", "0034 81 012 34 56"]
    assert rre.es.phone_number("el 12/05/2024, ref 34612345678 y 6123456789") == []


def test_mobile_number():
    assert rre.es.mobile_number("móvil 612 345 678 o +34 712345678") == ["612 345 678", "+34 712345678"]
    assert rre.es.mobile_number("810 123 456 y 701 234 567") == []


def test_premium_number():
    assert rre.es.premium_number("llame al 803 123 456 o al 806 12 34 56") == ["803 123 456", "806 12 34 56"]
    assert rre.es.premium_number("gratis 800 123 456") == []


def test_msisdn():
    assert rre.es.msisdn("msisdn 34612345678") == ["34612345678"]
    assert rre.es.msisdn("34810123456 y 3461234567") == []


def test_imsi():
    assert rre.es.imsi("imsi 214011234567890") == ["214011234567890"]
    assert rre.es.imsi("imsi 222011234567890") == []


def test_iccid():
    assert rre.es.iccid("sim 8934011234567890128") == ["8934011234567890128"]
    assert rre.es.iccid("sim 8934011234567890127") == []


def test_license_plate():
    assert rre.es.license_plate("coche 1234 BCD, 1234-BCD y 5678BCD") == ["1234 BCD", "1234-BCD", "5678BCD"]
    assert rre.es.license_plate("antiguas M-1234-AB y MA 1234 B") == ["M-1234-AB", "MA 1234 B"]
    assert rre.es.license_plate("1234 ABC, 5000 GBP, M-1234 AB") == []


def test_postal_code_city():
    assert rre.es.postal_code_city("28013 Madrid y 28801 Alcalá de Henares (Madrid)") == [
        "28013 Madrid", "28801 Alcalá de Henares (Madrid)"]
    assert rre.es.postal_code_city("15001 A Coruña") == ["15001 A Coruña"]
    assert rre.es.postal_code_city("99999 Madrid, 10000 Euros") == []


def test_street_address():
    assert rre.es.street_address("vive en Calle Mayor 12, 3º B de Madrid") == ["Calle Mayor 12, 3º B"]
    assert rre.es.street_address("C/ Alcalá, 45 y Avda. de la Constitución nº 7") == [
        "C/ Alcalá, 45", "Avda. de la Constitución nº 7"]
    assert rre.es.street_address("Plaza Mayor s/n, Paseo de Gracia 92, 2º 1ª") == [
        "Plaza Mayor s/n", "Paseo de Gracia 92, 2º 1ª"]
    assert rre.es.street_address("Calle sin número, el paseo de 3 horas") == []


def test_company_name():
    assert rre.es.company_name("entre Construcciones García S.L. y Telefónica, S.A.") == [
        "Construcciones García S.L.", "Telefónica, S.A."]
    assert rre.es.company_name("Fomento de Construcciones y Contratas, S.A.U.") == [
        "Fomento de Construcciones y Contratas, S.A.U."]
    assert rre.es.company_name("la sa de Juan") == []


def test_ecli():
    assert rre.es.ecli("ver ECLI:ES:TS:2015:1234A.") == ["ECLI:ES:TS:2015:1234A"]
    assert rre.es.ecli("ECLI:BE:CASS:2020:ARR.20200115.1") == []


def test_aircraft_registration():
    assert rre.es.aircraft_registration("avión EC-XYZ") == ["EC-XYZ"]
    assert rre.es.aircraft_registration("EC-AB, EC-1234 y DEC-XYZ") == []


# hardened tests: every value made up or a documented specimen; each negative is one near-miss or look-alike


def test_hard_dni():
    f = rre.es.dni
    assert f("87654321X") == ["87654321X"]
    assert f("DNI: 11223344B.") == ["11223344B"]
    assert f("(50000001W)") == ["50000001W"]
    assert f("«31.415.926-L» y 27182818-S") == ["31.415.926-L", "27182818-S"]
    assert f("El titular del DNI 01234567L firmó") == ["01234567L"]
    for text in ("87654321A", "8765432X", "187654321X", "00000000T", "X87654321X", "87654321-XA", "87654321U",
                 "12-345-678-Z"):
        assert f(text) == [], text


def test_hard_nie():
    f = rre.es.nie
    assert f("X7654321J") == ["X7654321J"]
    assert f("NIE: Y2345678Z.") == ["Y2345678Z"]
    assert f("(Z9876543A)") == ["Z9876543A"]
    assert f("«X-1111111-G» y Y1000000C") == ["X-1111111-G", "Y1000000C"]
    assert f("La extranjera con NIE Z-1234567R declaró") == ["Z-1234567R"]
    for text in ("X7654321K", "X765432J", "X76543210J", "W7654321J", "XX7654321J", "X 7654321 J", "X0000000T",
                 "X.7654321.J"):
        assert f(text) == [], text


def test_hard_cif():
    f = rre.es.cif
    assert f("A28173615") == ["A28173615"]
    assert f("CIF: B87654323.") == ["B87654323"]
    assert f("(G1234567D)") == ["G1234567D"]  # control as a letter
    assert f("«S7654321D», E11122231") == ["S7654321D", "E11122231"]
    assert f("La sociedad H-31.415.92-0 y la U27182815 contra V9876543A") == ["H-31.415.92-0", "U27182815", "V9876543A"]
    # a path segment of a URL is no CIF
    for text in ("B87654324", "B8765432", "B876543230", "I87654323", "b87654323", "https://example.com/B87654323/",
                 "XB87654323", "B 87654323"):
        assert f(text) == [], text


def test_hard_vat_number():
    f = rre.es.vat_number
    assert f("ESB87654323") == ["ESB87654323"]
    assert f("NIF-IVA: ES 87654321X.") == ["ES 87654321X"]
    assert f("(ESY2345678Z)") == ["ESY2345678Z"]
    assert f("«ES-A28173615» y ESG1234567D") == ["ES-A28173615", "ESG1234567D"]
    assert f("El proveedor ES01234567L factura") == ["ES01234567L"]
    for text in ("ESB87654324", "ES8765432X", "ESB876543230", "esB87654323", "XESB87654323", "FRB87654323",
                 "ES00000000T", "ESI87654323"):
        assert f(text) == [], text


def test_hard_social_security_number():
    f = rre.es.social_security_number
    assert f("08 87654321 46") == ["08 87654321 46"]
    assert f("NSS: 461000000120.") == ["461000000120"]
    assert f("(41/23456789/78)") == ["41/23456789/78"]
    assert f("«66-11223344-67» y 01 00012345 05") == ["66-11223344-67", "01 00012345 05"]
    assert f("Afiliado 53 99887766 04 desde 2010, antes 03/0765432/39") == ["53 99887766 04", "03/0765432/39"]
    for text in ("08 87654321 47", "0887654321", "08876543214600", "67 87654321 46", "00 87654321 46",
                 "x088765432146", "08.87654321.46"):
        assert f(text) == [], text


def test_hard_iban():
    f = rre.es.iban
    assert f("ES6000491500051234567892") == ["ES6000491500051234567892"]
    assert f("IBAN: ES17 2085 2066 6234 5678 9011.") == ["ES17 2085 2066 6234 5678 9011"]
    assert f("(ES3501821234561234567890)") == ["ES3501821234561234567890"]
    assert f("«ES19 0081 0216 7300 0610 4569»") == ["ES19 0081 0216 7300 0610 4569"]
    assert f("Transferir a ES 45 3058 0000 1123 4567 8901 o ES7714650100911234567890") == [
        "ES 45 3058 0000 1123 4567 8901", "ES7714650100911234567890"]
    for text in ("ES6000491500051234567893", "ES600049150005123456789", "ES60004915000512345678921",
                 "es6000491500051234567892", "XES6000491500051234567892", "PT50000201231234567890154",
                 "ES60-0049-1500-0512-3456-7892"):
        assert f(text) == [], text


def test_hard_bic():
    f = rre.es.bic
    assert f("MUSTESMMXXX") == ["MUSTESMMXXX"]
    assert f("BIC: BEISESBB.") == ["BEISESBB"]
    assert f("(QRSTES2A)") == ["QRSTES2A"]
    assert f("«ABCDES12345» o ZYXWESMM100") == ["ABCDES12345", "ZYXWESMM100"]
    assert f("El banco TESTES3X paga") == ["TESTES3X"]
    for text in ("MUSTESM", "MUSTESMMXX", "MUSTESMMXXXX", "mustesmm", "XMUSTESMM", "MUSTFRPP", "MU5TESMM", "PRINCESA"):
        assert f(text) == [], text


def test_hard_passport_number():
    f = rre.es.passport_number
    assert f("XDB654321") == ["XDB654321"]
    assert f("Pasaporte: AAA000777.") == ["AAA000777"]
    assert f("(PAC246810)") == ["PAC246810"]
    assert f("«XDC135790» y PAB987654") == ["XDC135790", "PAB987654"]
    assert f("Número de pasaporte AAB012345 expedido en Madrid") == ["AAB012345"]
    for text in ("PA123456", "PAA12345", "PAA1234567", "paa123456", "XPAA123456", "1PAA123456", "PAA-123456",
                 "PA-A123456"):
        assert f(text) == [], text


def test_hard_mrz_id_card():
    f = rre.es.mrz_id_card
    lines = ["IDESPCAB123456012345678Z<<<<<<", "IDESPBHZ654321287654321X<<<<<<", "IDESPAAA000001111111111H<<<<<<",
             "IDESPBCD246810700000023T<<<<<<", "IRESPE123456782X1234567L<<<<<<", "IDESPDEF135791631415926L<<<<<<"]
    assert f(lines[0]) == [lines[0]]
    assert f(f"MRZ: {lines[1]}\n8001014M3001019ESP<<<<<<<<<<<6") == [lines[1]]
    assert f(f"({lines[2]})") == [lines[2]]
    assert f(f"«{lines[3]}»") == [lines[3]]
    assert f(f"Tarjeta de extranjero {lines[4]} y DNI {lines[5]}") == [lines[4], lines[5]]
    for text in (lines[0].replace("1234560", "1234561"), lines[0].replace("ESP", "FRA"), lines[0] + "<", "X" + lines[0],
                 lines[0].lower(), lines[0][:-1], "P<ESPESPANOLA<ESPANOLA<<CARMEN<<<<<<<<<<<<<<"):
        assert f(text) == [], text


def test_hard_mrz_passport():
    f = rre.es.mrz_passport
    lines = ["PAA1234560ESP8001014M300101912345678Z<<<<<38", "XDA6543219ESP9211306F290630287654321X<<<<<32",
             "AAB0007778ESP0102030M3102031<<<<<<<<<<<<<<<4", "PAC2468108ESP6507040F280916027182818S<<<<<58",
             "XDB6543210ESP7701018M3201015<<<<<<<<<<<<<<<8", "AAA0007777ESP8812315X271130201234567L<<<<<78"]
    assert f(lines[0]) == [lines[0]]
    assert f(f"P<ESPESPANOLA<ESPANOLA<<CARMEN<<<<<<<<<<<<<<\n{lines[1]}") == [lines[1]]
    assert f(f"({lines[2]})") == [lines[2]]
    assert f(f"«{lines[3]}»") == [lines[3]]
    assert f(f"Pasaporte {lines[4]} y {lines[5]}") == [lines[4], lines[5]]
    line = lines[0]
    for text in (line.replace("1234560", "1234561"), line.replace("8001014", "8001015"), line.replace("3001019", "3001018"),
                 line.replace("ESP", "D<<"), line + "<", line.lower(), "X" + line):
        assert f(text) == [], text


def test_hard_phone_number():
    f = rre.es.phone_number
    assert f("934 12 34 56") == ["934 12 34 56"]
    assert f("Tel.: 954.12.34.56.") == ["954.12.34.56"]
    assert f("(881 23 45 67)") == ["881 23 45 67"]
    assert f("«+34 963 123 456» o 0034-876-543-210") == ["+34 963 123 456", "0034-876-543-210"]
    assert f("llámame al 622 33 44 55 o al 911234567") == ["622 33 44 55", "911234567"]
    for text in ("934 12 34 5", "934 12 34 567", "34934123456", "+33 934 123 456", "500 123 456", "el 12/05/2024",
                 "1934 123 456", "934 123 456 7"):
        assert f(text) == [], text


def test_hard_mobile_number():
    f = rre.es.mobile_number
    assert f("698 765 432") == ["698 765 432"]
    assert f("Móvil: 744.123.456.") == ["744.123.456"]
    assert f("(601 23 45 67)") == ["601 23 45 67"]
    assert f("«+34 722 12 34 56» o 0034 622334455") == ["+34 722 12 34 56", "0034 622334455"]
    assert f("Escríbeme al 62 233 44 55 mañana") == ["62 233 44 55"]
    for text in ("934 123 456", "698 765 43", "698 765 4321", "34698765432", "+351 912 345 678", "800 123 456",
                 "1698 765 432"):
        assert f(text) == [], text


def test_hard_premium_number():
    f = rre.es.premium_number
    assert f("806 654 321") == ["806 654 321"]
    assert f("+34 807 11 22 33") == ["+34 807 11 22 33"]  # international form
    assert f("(803 123 456)") == ["803 123 456"]
    assert f("Tarifa compartida: 901 123 456.") == ["901 123 456"]  # shared cost
    assert f("«0034 902 202 122» o +34803654321") == ["0034 902 202 122", "+34803654321"]
    # 905 (televoting) is in no numbering plan libphonenumber knows
    for text in ("800 123 456", "905 123 456", "803 123 45", "803 123 4567", "803 123 456 7", "1803 123 456",
                 "934 123 456"):
        assert f(text) == [], text


def test_hard_msisdn():
    f = rre.es.msisdn
    assert f("34698765432") == ["34698765432"]
    assert f("MSISDN: 34722123456.") == ["34722123456"]
    assert f("(34601234567)") == ["34601234567"]
    assert f("msisdn=34622334455; b=34744123456") == ["34622334455", "34744123456"]
    assert f("El abonado 34711234567 llamó") == ["34711234567"]
    # with + it is an international number (es.mobile_number), not an MSISDN
    for text in ("+34612345678", "34934123456", "3469876543", "346987654321", "0034698765432", "x34698765432",
                 "33612345678"):
        assert f(text) == [], text


def test_hard_imsi():
    f = rre.es.imsi
    assert f("214071234567890") == ["214071234567890"]
    assert f("IMSI: 214011122334455.") == ["214011122334455"]
    assert f("(214039876543210)") == ["214039876543210"]
    assert f("«214040000000001» y 214051234567890") == ["214040000000001", "214051234567890"]
    assert f("La SIM 214060123456789 estaba activa") == ["214060123456789"]
    for text in ("21401123456789", "2140112345678901", "262011234567890", "x214011234567890", "214 01 1234567890",
                 "IMEI 352099001761481"):
        assert f(text) == [], text


def test_hard_iccid():
    f = rre.es.iccid
    assert f("893407123456789012") == ["893407123456789012"]
    assert f("ICCID: 89340400112233445561.") == ["89340400112233445561"]
    assert f("(8934039876543210983)") == ["8934039876543210983"]
    assert f("«89340700000000000015» y 8934010000000000000") == ["89340700000000000015", "8934010000000000000"]
    assert f("La tarjeta 8934011234567890128 apareció") == ["8934011234567890128"]
    for text in ("893407123456789013", "89340712345678901", "893404001122334455612", "8949020000123456788",
                 "x8934011234567890128", "8934 0112 3456 7890 128"):
        assert f(text) == [], text


def test_hard_license_plate():
    f = rre.es.license_plate
    assert f("1234BCD") == ["1234BCD"]
    assert f("(9876 ZYX)") == ["9876 ZYX"]
    assert f("«2345 KLM»") == ["2345 KLM"]
    assert f("Matrícula: 4321-DFG.") == ["4321-DFG"]
    assert f("El coche GC-1234-AB adelantó al IB 5678 C y al B-2345-XY") == ["GC-1234-AB", "IB 5678 C", "B-2345-XY"]
    # an old provincial plate always has its separators: L2304B is a lot number
    for text in ("Lot L2304B", "M1234AB", "1234 AEI", "12345 BCD", "1234 BCDF", "1234 BTC", "M-1234 AB", "1234-bcd"):
        assert f(text) == [], text


def test_hard_postal_code_city():
    f = rre.es.postal_code_city
    assert f("08001 Barcelona") == ["08001 Barcelona"]
    assert f("(41001 Sevilla)") == ["41001 Sevilla"]
    assert f("«48001 Bilbao»") == ["48001 Bilbao"]
    assert f("CP 29001 Málaga, España") == ["29001 Málaga"]
    assert f("08760 Martorell (Barcelona), 08901 L'Hospitalet de Llobregat y 01001 Vitoria-Gasteiz") == [
        "08760 Martorell (Barcelona)", "08901 L'Hospitalet de Llobregat", "01001 Vitoria-Gasteiz"]
    assert f("Vive en 35001 Las Palmas de Gran Canaria") == ["35001 Las Palmas de Gran Canaria"]
    for text in ("08001 barcelona", "53001 Madrid", "00001 Madrid", "2800 Madrid", "280130 Madrid", "unos 15000 Euros",
                 "10000 EUR"):
        assert f(text) == [], text


def test_hard_street_address():
    f = rre.es.street_address
    assert f("Avda. Diagonal 640, 5º") == ["Avda. Diagonal 640, 5º"]
    # in a sentence the street type is written in lower case
    assert f("Vive en la calle Mayor 12 desde 2019.") == ["calle Mayor 12"]
    assert f("(Calle Real 7)") == ["Calle Real 7"]
    assert f("«Plaza de España 1», Pº de la Castellana 100") == ["Plaza de España 1", "Pº de la Castellana 100"]
    assert f("Rúa do Franco 22 y Carrer de l'Hospital 5") == ["Rúa do Franco 22", "Carrer de l'Hospital 5"]
    assert f("Avenida 1º de Mayo 12, c/ Mayor 3 y Calle Mayor nº12") == [
        "Avenida 1º de Mayo 12", "c/ Mayor 3", "Calle Mayor nº12"]
    for text in ("Calle Mayor", "Calle Mayor 12345", "la calle de 3 carriles", "en la calle 2 personas y 3 niños",
                 "el camino 4 veces 2", "las calles 1 y 2", "Avenida 10"):
        assert f(text) == [], text


def test_hard_company_name():
    f = rre.es.company_name
    assert f("Talleres Pérez S.A.T.") == ["Talleres Pérez S.A.T."]
    assert f("Inversiones del Sur SL, Transportes Ruiz S.L.U. y Consorcio Puerto AIE") == [
        "Inversiones del Sur SL", "Transportes Ruiz S.L.U.", "Consorcio Puerto AIE"]
    assert f("(Gráficas Norte, S.L.)") == ["Gráficas Norte, S.L."]
    assert f("«Pinturas Sol S.L.»") == ["Pinturas Sol S.L."]
    assert f("Agrícola Los Olivos S.Coop.") == ["Agrícola Los Olivos S.Coop."]
    # a capitalised word that starts the sentence is not part of the name
    assert f("Según Construcciones Ruiz S.L.N.E., la deuda creció") == ["Construcciones Ruiz S.L.N.E."]
    for text in ("Hoy S.A. anunció", "Mi empresa S.L.", "Talleres Pérez SAS", "Muster GmbH", "S.A.",
                 "TALLERES PEREZ SLX", "talleres pérez s.l."):
        assert f(text) == [], text


def test_hard_ecli():
    f = rre.es.ecli
    assert f("ECLI:ES:APM:2019:5678") == ["ECLI:ES:APM:2019:5678"]
    assert f("(ECLI:ES:TC:2020:12)") == ["ECLI:ES:TC:2020:12"]
    assert f("ver ECLI:ES:TSJCAT:2018:1234.") == ["ECLI:ES:TSJCAT:2018:1234"]
    assert f("«ECLI:ES:AN:2017:345»") == ["ECLI:ES:AN:2017:345"]
    assert f("Véase ECLI:ES:TS:2021:9876A, firme, y ECLI:ES:JSO:2016:1.2") == [
        "ECLI:ES:TS:2021:9876A", "ECLI:ES:JSO:2016:1.2"]
    for text in ("ecli:es:ts:2015:1234", "ECLI:ES:ts:2015:1234", "ECLI:ES:TS:15:1234", "ECLI:ES::2015:1",
                 "XECLI:ES:TS:2015:1", "ECLI:ES:TS:2015:", "ECLI:ES:TS:2015:1234a", "ECLI:FR:CC:2015:1234"):
        assert f(text) == [], text


def test_hard_aircraft_registration():
    f = rre.es.aircraft_registration
    assert f("EC-MYT") == ["EC-MYT"]
    assert f("(EC-ABC)") == ["EC-ABC"]
    assert f("«EC-KLM»") == ["EC-KLM"]
    assert f("Matrícula: EC-JZX.") == ["EC-JZX"]
    assert f("El EC-NBV aterrizó tras el EC-LQP y el EC-HGZ") == ["EC-NBV", "EC-LQP", "EC-HGZ"]
    for text in ("EC-AB", "EC-ABCD", "EC-abc", "SEC-ABC", "EC ABC", "EC-1234", "EC-ÑAB", "D-EABC"):
        assert f(text) == [], text
