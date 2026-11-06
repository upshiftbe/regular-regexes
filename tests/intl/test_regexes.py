import time

from regular_regexes import rre

def test_email():
    assert len(rre.email("test@test.com")) > 0
    assert len(rre.email("test@test")) == 0

def test_url():
    assert len(rre.url("check it at test.com")) > 0
    assert len(rre.url("check it at testcom")) == 0
    assert len(rre.url("check it at https://test.com")) > 0
    assert len(rre.url("check it at https://testcom")) == 0

def test_multiple_punctuation():
    assert len(rre.multiple_punctuation("how are you??")) > 0
    assert len(rre.multiple_punctuation("how are you?!")) > 0
    assert len(rre.multiple_punctuation("&&&&& that's how it is")) > 0
    assert len(rre.multiple_punctuation("& that's how it is")) == 0
    assert len(rre.multiple_punctuation("how are you?")) == 0
    assert len(rre.multiple_punctuation("look over there!")) == 0

def test_returns_full_match_not_groups():
    assert rre.container_number("box CSQU3054383 here") == ["CSQU3054383"]
    assert rre.ip_address("host 192.168.1.10 up") == ["192.168.1.10"]


def test_iban():
    assert rre.iban("NL91ABNA0417164300 and GB29 NWBK 6016 1331 9268 19") == ["NL91ABNA0417164300", "GB29 NWBK 6016 1331 9268 19"]
    # greedy match swallows "BIC", validator trims it off again
    assert rre.iban("BE68 5390 0754 7034 BIC GEBABEBB") == ["BE68 5390 0754 7034"]


def test_imei():
    assert rre.imei("imei 490154203237518") == ["490154203237518"]
    assert rre.imei("imei 490154203237519") == []


def test_misc_intl():
    assert rre.phone_e164("+32470123456") == ["+32470123456"]
    assert rre.mac_address("mac 00:1A:2B:3C:4D:5E") == ["00:1A:2B:3C:4D:5E"]
    assert rre.ethereum_address("0x" + "a" * 40) == ["0x" + "a" * 40]
    assert rre.bitcoin_address("to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"]


def test_password():
    assert rre.password("Abcdefg1") == ["Abcdefg1"]
    assert rre.password("abcdefg1") == []  # no uppercase
    assert rre.password("Abcdefgh") == []  # no digit
    assert rre.password("Abcde1") == []  # too short


def test_ip_address():
    assert rre.ip_address("from 10.0.0.1 to 255.255.255.255") == ["10.0.0.1", "255.255.255.255"]
    assert rre.ip_address("not 256.1.1.1") == []
    assert rre.ip_address("version 1.2.3.4.5 and 6.1.2.3.4") == []


def test_email_does_not_swallow_text():
    assert rre.email("mail jan.peeters+x@test.be of piet@x.co.uk.") == ["jan.peeters+x@test.be", "piet@x.co.uk"]


def test_container_number():
    assert rre.container_number("container CSQU 305438 3 en CSQU3054384") == ["CSQU 305438 3"]


def test_bitcoin_address():
    # BIP173 test vector
    assert rre.bitcoin_address("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4") == ["bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"]
    assert rre.bitcoin_address("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5") == []
    assert rre.bitcoin_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNb") == []


def test_litecoin_address():
    assert rre.litecoin_address("ltc LKDyUEtTR1HXamkiEphisSiBJu6o3ZPE34") == ["LKDyUEtTR1HXamkiEphisSiBJu6o3ZPE34"]
    assert rre.litecoin_address("LKDyUEtTR1HXamkiEphisSiBJu6o3ZPE35") == []


def test_tron_address():
    assert rre.tron_address("usdt TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t") == ["TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"]
    assert rre.tron_address("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6u") == []


def test_monero_address():
    address = "4A" + "x" * 93
    assert rre.monero_address(f"xmr {address}") == [address]


def test_bitcoin_private_key():
    # WIF example from the bitcoin wiki
    key = "5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"
    assert rre.bitcoin_private_key(key) == [key]
    assert rre.bitcoin_private_key(key[:-1] + "K") == []


def test_ipv6():
    assert rre.ipv6("from 2001:db8::1 and fe80::1ff:fe23:4567:890a") == ["2001:db8::1", "fe80::1ff:fe23:4567:890a"]
    assert rre.ipv6("at 12:30:45 mac 00:1A:2B:3C:4D:5E") == []


def test_credit_card():
    assert rre.credit_card("visa 4111 1111 1111 1111") == ["4111 1111 1111 1111"]
    assert rre.credit_card("4111 1111 1111 1112") == []


def test_iccid():
    assert rre.iccid("sim 893201123456789010") == ["893201123456789010"]
    assert rre.iccid("893201123456789011") == []


def test_vin():
    assert rre.vin("chassis 1M8GDM9AXKP042788") == ["1M8GDM9AXKP042788"]
    assert rre.vin("ABCDEFGHJKLMNPRST") == []  # no digits


def test_imo_number():
    assert rre.imo_number("ship IMO 9074729") == ["IMO 9074729"]
    assert rre.imo_number("IMO 9074728") == []


def test_mrz():
    # ICAO 9303 specimens
    td1 = "I<UTOD231458907<<<<<<<<<<<<<<<"
    td3 = "L898902C36UTO7408122F1204159ZE184226B<<<<<10"
    assert rre.mrz_id_card(td1) == [td1]
    assert rre.mrz_passport(td3) == [td3]
    assert rre.mrz_id_card(td1.replace("907", "908")) == []


def test_gps():
    assert rre.gps_coordinates("at 51.0543, 3.7174 and -33.8688,151.2093") == ["51.0543, 3.7174", "-33.8688,151.2093"]
    assert rre.gps_coordinates("1.5, 2.5") == []
    # not the end of a longer number
    assert rre.gps_coordinates("91.0000, 3.7174 and 123.4567, 3.7174") == []
    assert rre.gps_dms("51°03'15.5\"N 3°43'02\"E") == ["51°03'15.5\"N", "3°43'02\"E"]


def test_iso_datetime():
    assert rre.iso_datetime("log 2024-03-01T14:30:05Z and 2024-03-02") == ["2024-03-01T14:30:05Z", "2024-03-02"]
    assert rre.iso_datetime("2024-13-01") == []


def test_hashes_and_uuid():
    assert rre.md5("md5 d41d8cd98f00b204e9800998ecf8427e") == ["d41d8cd98f00b204e9800998ecf8427e"]
    assert rre.sha1("da39a3ee5e6b4b0d3255bfef95601890afd80709") == ["da39a3ee5e6b4b0d3255bfef95601890afd80709"]
    sha = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert rre.sha256(sha) == [sha]
    assert rre.md5(sha) == []
    assert rre.uuid("id 550e8400-e29b-41d4-a716-446655440000") == ["550e8400-e29b-41d4-a716-446655440000"]


def test_onion_address():
    onion = "a" * 56 + ".onion"
    assert rre.onion_address(f"visit http://{onion}/x") == [onion]
    assert rre.onion_address("short.onion") == []


def test_messaging_links():
    assert rre.telegram_link("join t.me/joinchat/AbCdEf and https://telegram.me/somechannel") == [
        "t.me/joinchat/AbCdEf", "https://telegram.me/somechannel"]
    assert rre.telegram_link("preview https://t.me/s/somechannel") == ["https://t.me/s/somechannel"]
    assert rre.whatsapp_link("chat via wa.me/32470123456 or wa.me/+32470123456") == [
        "wa.me/32470123456", "wa.me/+32470123456"]
    assert rre.discord_invite("https://discord.gg/abc123") == ["https://discord.gg/abc123"]


def test_session_id():
    sid = "05" + "ab" * 32
    assert rre.session_id(f"session {sid}") == [sid]
    assert rre.session_id("06" + "ab" * 32) == []


def test_pgp_block():
    block = "-----BEGIN PGP MESSAGE-----\nhQEMA\n-----END PGP MESSAGE-----"
    assert rre.pgp_block(f"msg:\n{block}\nbye") == [block]


def test_mention_and_hashtag():
    assert rre.mention("ping @dealer123 not jan@test.be") == ["@dealer123"]
    assert rre.hashtag("#coke #420 x#y") == ["#coke"]


def test_ios_system_path():
    for path in (
        "/System/Library/PrivateFrameworks/Assistant.framework/sound.caf",
        "/Library/Ringtones/Opening.m4r",
        "/Applications/MobileSafari.app/icon.png",
        "/usr/share/x",
        "/private/preboot/Cryptexes/OS/System/Library/x.png",
    ):
        assert rre.ios_system_path(path) == [path]
    for path in (
        "/private/var/mobile/Media/DCIM/100APPLE/IMG_0001.HEIC",
        "/private/var/mobile/Library/Caches/x.png",
        "/private/var/containers/Bundle/Application/X/App.app/x.png",
        "/system/media/x.ogg",
        "/Systemx/x",
        "",
    ):
        assert rre.ios_system_path(path) == []


def test_android_system_path():
    for path in (
        "/system/media/audio/ui/Effect_Tick.ogg",
        "/system_ext/x.png",
        "/product/media/audio/ringtones/x.ogg",
        "/vendor/etc/x",
        "/apex/com.android.x/etc/x",
    ):
        assert rre.android_system_path(path) == [path]
    for path in (
        "/data/system/usagestats/0/daily/1",
        "/data/data/com.example/files/system/x.png",
        "/storage/emulated/0/System/x.png",
        "/System/Library/x",
        "text /system/x",
    ):
        assert rre.android_system_path(path) == []


def test_bip39_seed_phrase():
    # official BIP39 test vectors (trezor/python-mnemonic vectors.json)
    p12 = "legal winner thank year wave sausage worth useful legal winner thank yellow"
    assert rre.bip39_seed_phrase(f"seed phrase: {p12}\nkeep it safe") == [p12]
    p24 = ("hamster diagram private dutch cause delay private meat slide toddler razor book happy fancy gospel "
           "tennis maple dilemma loan word shrug inflict delay length").split()
    numbered = "\n".join(f"{i}. {w}" for i, w in enumerate(p24, 1))
    assert rre.bip39_seed_phrase(f"backup:\n{numbered}\n") == [numbered[3:]]
    p18 = ("Gravity machine north sort system female filter attitude volume fold club stay feature office ecology "
           "stable narrow fog")
    assert rre.bip39_seed_phrase(p18) == [p18]
    assert rre.bip39_seed_phrase(p12.rsplit(" ", 1)[0]) == []  # 11 words
    assert rre.bip39_seed_phrase(p12.replace("yellow", "wrong")) == []


def test_xrp_address():
    # the XRP Ledger genesis account and ACCOUNT_ZERO
    assert rre.xrp_address("to rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh and rrrrrrrrrrrrrrrrrrrrrhoLvTp") == [
        "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh", "rrrrrrrrrrrrrrrrrrrrrhoLvTp"]
    assert rre.xrp_address("rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTj") == []
    assert rre.xrp_address("btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == []


def test_bitcoin_extended_key():
    # BIP32 test vector 1, chain m
    xpub = ("xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsef"
            "D265TMg7usUDFdp6W1EGMcet8")
    xprv = ("xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRN"
            "NU3TGtRBeJgk33yuGBxrMPHi")
    assert rre.bitcoin_extended_key(f"watch-only {xpub}, master {xprv}") == [xpub, xprv]
    assert rre.bitcoin_extended_key(xpub[:-1] + "9") == []
    assert rre.bitcoin_extended_key(xpub[:-1]) == []  # 110 characters


def test_card_track_data():
    track1 = "%B4111111111111111^TEST/CARD^25121010000000000000?"
    track2 = ";4111111111111111=25121010000000000000?"
    assert rre.card_track_data(f"{track1}{track2}") == [track1, track2]
    assert rre.card_track_data("emv 4111111111111111D2512101123") == ["4111111111111111D2512101123"]
    assert rre.card_track_data(track1.replace("4111111111111111", "4111111111111112")) == []
    assert rre.card_track_data(";4111111111111111=25131010000000000000?") == []  # month 13


def test_card_dump():
    assert rre.card_dump("4111111111111111|12|2025|123|TEST CARD|1 TEST STREET\n5555555555554444:01:27:456") == [
        "4111111111111111|12|2025|123|TEST CARD|1 TEST STREET", "5555555555554444:01:27:456"]
    assert rre.card_dump("378282246310005;1225;1234 and 4111111111111111 | 12/25 | 123") == [
        "378282246310005;1225;1234", "4111111111111111 | 12/25 | 123"]
    assert rre.card_dump("4111111111111112|12|2025|123") == []
    assert rre.card_dump("4111111111111111|13|2025|123") == []


def test_gift_card_code():
    assert rre.gift_card_code("paysafecard pin: 1234 5678 9012 3456, coupon PCS de 100€ : AB12C3DE4F") == [
        "paysafecard pin: 1234 5678 9012 3456", "PCS de 100€ : AB12C3DE4F"]
    text = "Apple gift card X123456789ABCDEF, Steam ABCDE-FGH1J-KLMNO, amazon code AB12-CDEFGH-IJKL"
    assert rre.gift_card_code(text) == [
        "Apple gift card X123456789ABCDEF", "Steam ABCDE-FGH1J-KLMNO", "amazon code AB12-CDEFGH-IJKL"]
    assert rre.gift_card_code("Google Play ABCD EFGH 1JKL MNOP") == ["Google Play ABCD EFGH 1JKL MNOP"]
    assert rre.gift_card_code("amazon order 123-4567890-1234567, 100 PCS 1234567890, paysafecard 1234 5678") == []


def test_lei():
    assert rre.lei("GLEIF, LEI 506700GE1G29325QX363") == ["506700GE1G29325QX363"]
    assert rre.lei("506700GE1G29325QX364") == []
    assert rre.lei("iccid 89320112345678901232") == []  # digits only


def test_isin():
    assert rre.isin("ISIN US0378331005 and ISIN-code: BE0003470755") == ["ISIN US0378331005", "ISIN-code: BE0003470755"]
    assert rre.isin("ISIN US0378331006") == []
    assert rre.isin("btw BE0003470755") == []  # no ISIN keyword


def test_currency_amount():
    assert rre.currency_amount("paid € 1.234,56, $1,234.56, 250 EUR and 1 234,56 €") == [
        "€ 1.234,56", "$1,234.56", "250 EUR", "1 234,56 €"]
    assert rre.currency_amount("0.5 BTC, 100 usdt, 5k€, CHF 1'234.50, € 50,-") == [
        "0.5 BTC", "100 usdt", "5k€", "CHF 1'234.50", "€ 50,-"]
    assert rre.currency_amount("1 249,99 zł i 500 lei") == ["1 249,99 zł", "500 lei"]
    assert rre.currency_amount("in 2024 at 12:30, order 123, room 5, lei 25 anni") == []


def test_upu_tracking_number():
    assert rre.upu_tracking_number("bpost RR123456785BE and AA 473 124 829 GB") == [
        "RR123456785BE", "AA 473 124 829 GB"]
    assert rre.upu_tracking_number("RR123456786BE") == []
    assert rre.upu_tracking_number("RR12345678BE") == []


def test_ups_tracking_number():
    # UPS's own test number
    assert rre.ups_tracking_number("ups 1Z999AA10123456784 or 1Z 999 AA1 01 2345 678 4") == [
        "1Z999AA10123456784", "1Z 999 AA1 01 2345 678 4"]
    assert rre.ups_tracking_number("1Z999AA10123456785") == []
    assert rre.ups_tracking_number("1Z999AA1012345678") == []


def test_air_waybill():
    # serials from the Australian Border Force check digit examples
    assert rre.air_waybill("AWB 020-12345675, MAWB: 17681140743") == ["AWB 020-12345675", "MAWB: 17681140743"]
    assert rre.air_waybill("AWB 020-12345674") == []
    assert rre.air_waybill("tel 030-12345675") == []  # no keyword


def test_isbn():
    assert rre.isbn("ISBN 978-0-306-40615-7, ISBN-10: 0-306-40615-2 and ISBN 0-8044-2957-X") == [
        "ISBN 978-0-306-40615-7", "ISBN-10: 0-306-40615-2", "ISBN 0-8044-2957-X"]
    assert rre.isbn("ISBN 978-0-306-40615-8") == []
    assert rre.isbn("978-0-306-40615-7") == []  # no ISBN keyword


def test_gtin():
    assert rre.gtin("EAN 4006381333931, UPC-A: 036000291452, EAN-8 73513537") == [
        "EAN 4006381333931", "UPC-A: 036000291452", "EAN-8 73513537"]
    assert rre.gtin("EAN 4006381333932") == []
    assert rre.gtin("batch 4006381333931") == []  # no keyword


def test_signal_link():
    username = "Ab1-" * 16
    assert rre.signal_link(f"add me signal.me/#p/+447700900123 or https://signal.me/#eu/{username}.") == [
        "signal.me/#p/+447700900123", f"https://signal.me/#eu/{username}"]
    group = "CjQKI" + "Ab1_" * 15
    assert rre.signal_link(f"https://signal.group/#{group} https://signal.link/call/#key=bcdf-ghkm-npqr-stxz") == [
        f"https://signal.group/#{group}", "https://signal.link/call/#key=bcdf-ghkm-npqr-stxz"]
    assert rre.signal_link("signal.org/download and signal.me/#p/12") == []


def test_threema_link():
    assert rre.threema_link("add https://threema.id/ECHOECHO?text=hi") == ["https://threema.id/ECHOECHO"]
    assert rre.threema_link("threema.id/ECHO and threema.id/ECHOECHO1") == []


def test_matrix_id():
    assert rre.matrix_id("dm @alice:example.org or https://matrix.to/#/@bob.smith:example.com:8448.") == [
        "@alice:example.org", "@bob.smith:example.com:8448"]
    assert rre.matrix_id("mail alice@example.org, @alice: hi at 10:30") == []


def test_social_media_profile():
    assert rre.social_media_profile(
        "https://www.instagram.com/jane.example/ x.com/jane_example, tiktok.com/@jane.example "
        "m.facebook.com/profile.php?id=100000000000001&ref=x be.linkedin.com/in/jane-example-1a2b3c"
    ) == ["https://www.instagram.com/jane.example/", "x.com/jane_example", "tiktok.com/@jane.example",
          "m.facebook.com/profile.php?id=100000000000001", "be.linkedin.com/in/jane-example-1a2b3c"]
    # posts, shares and site pages are not profiles
    assert rre.social_media_profile(
        "instagram.com/p/C1a2b3c4d5/ x.com/jane_example/status/1790000000000000000 facebook.com/share/p/1AbCdEf/ "
        "tiktok.com/@jane.example/video/7300000000000000000 youtube.com/watch?v=abc facebook.com/photo.php?fbid=1 "
        "x.com/home help.instagram.com/1234") == []


def test_file_share_link():
    key = "Ab1_" * 10 + "Ab1"
    assert rre.file_share_link(f"get https://mega.nz/file/AbCdEfGh#{key}, we.tl/t-AbCdEf1234 (pastebin.com/AbCd1234).") == [
        f"https://mega.nz/file/AbCdEfGh#{key}", "we.tl/t-AbCdEf1234", "pastebin.com/AbCd1234"]
    assert rre.file_share_link("privnote.com/AbCd1234#EfGh5678 drive.google.com/file/d/1AbC/view?usp=sharing") == [
        "privnote.com/AbCd1234#EfGh5678", "drive.google.com/file/d/1AbC/view?usp=sharing"]
    assert rre.file_share_link("www.dropbox.com/login, mega.nz and https://wetransfer.com/") == []


def test_magnet_link():
    link = "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=file.iso&tr=udp%3A%2F%2Ftracker.example.org"
    assert rre.magnet_link(f"get {link}.") == [link]
    assert rre.magnet_link("magnet:?xt=urn:btih:ABCDEFGHIJKLMNOPQRSTUVWXYZ234567") == [
        "magnet:?xt=urn:btih:ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"]
    assert rre.magnet_link("magnet:?xt=urn:btih:0123456789abcdef") == []


def test_plus_code():
    # examples from the Open Location Code documentation
    assert rre.plus_code("at 8FVC9G8F+6X or 9G8F+6X Zurich") == ["8FVC9G8F+6X", "9G8F+6X"]
    assert rre.plus_code("2+2=4, 2345+6789, C++, ABCD+EF") == []


def test_what3words():
    assert rre.what3words("at ///filled.count.soap. or https://w3w.co/index.home.raft") == [
        "///filled.count.soap", "https://w3w.co/index.home.raft"]
    assert rre.what3words("file:///home.user.docs and ///two.words") == []


def test_maps_link():
    assert rre.maps_link("here https://maps.app.goo.gl/AbCdEf12345, maps.apple.com/?ll=50.8467,4.3525 or "
                         "waze.com/ul?ll=50.8467,4.3525&navigate=yes.") == [
        "https://maps.app.goo.gl/AbCdEf12345", "maps.apple.com/?ll=50.8467,4.3525",
        "waze.com/ul?ll=50.8467,4.3525&navigate=yes"]
    assert rre.maps_link("https://www.google.com/maps/place/Grand-Place/@50.8467,4.3525,17z") == [
        "https://www.google.com/maps/place/Grand-Place/@50.8467,4.3525,17z"]
    assert rre.maps_link("google.com/search?q=maps and maps.google.com") == []


def test_windows_sid():
    # domain SID from Microsoft's documentation
    assert rre.windows_sid(r"C:\$Recycle.Bin\S-1-5-21-1004336348-1177238915-682003330-512\x") == [
        "S-1-5-21-1004336348-1177238915-682003330-512"]
    assert rre.windows_sid("S-1-5-32-544 and S-1-5-21-1004336348-1177238915-682003330-1001_Classes") == [
        "S-1-5-32-544", "S-1-5-21-1004336348-1177238915-682003330-1001"]
    assert rre.windows_sid("system S-1-5-18, sheet S-1-2") == []


def test_windows_path():
    assert rre.windows_path(r"opened C:\Users\Jane Example\Documents\report.docx today") == [
        r"C:\Users\Jane Example\Documents\report.docx"]
    assert rre.windows_path(r"copy to \\fileserver\C$\Temp\a.txt, see C:\Windows\System32.") == [
        r"\\fileserver\C$\Temp\a.txt", r"C:\Windows\System32"]
    assert rre.windows_path(r"loaded \\?\C:\Windows\System32\x.dll") == [r"C:\Windows\System32\x.dll"]
    assert rre.windows_path("http://example.com and C:/Users/x") == []


def test_jwt():
    # RFC 7519 examples: a signed token and an unsecured one, whose signature is empty
    signed = ("eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9"
              ".eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ"
              ".dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk")
    unsecured = ("eyJhbGciOiJub25lIn0"
                 ".eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ.")
    assert rre.jwt(f"Authorization: Bearer {signed}") == [signed]
    assert rre.jwt(unsecured) == [unsecured]
    # one character changed: the header's "alg" becomes "alh"
    assert rre.jwt(signed.replace("ICJhbGci", "ICJhbGgi")) == []
    assert rre.jwt("eyJhbGciOiJIUzI1NiJ9 without payload") == []


def test_api_key():
    # AWS's documentation example; the others are made up
    assert rre.api_key("aws AKIAIOSFODNN7EXAMPLE gh ghp_" + "a1B2" * 9) == ["AKIAIOSFODNN7EXAMPLE", "ghp_" + "a1B2" * 9]
    assert rre.api_key("https://api.telegram.org/bot123456789:AA" + "b" * 33 + "/getMe") == ["123456789:AA" + "b" * 33]
    assert rre.api_key("xoxb-1234567890-abcdefghij sk-ant-api03-" + "x" * 93 + "AA") == [
        "xoxb-1234567890-abcdefghij", "sk-ant-api03-" + "x" * 93 + "AA"]
    assert rre.api_key("AKIAIOSFODNN7EXAMPL ghp_short sk_test_" + "a" * 24 + " xoxo-hugs-and-kisses") == []


def test_private_key_block():
    block = "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAA\n-----END OPENSSH PRIVATE KEY-----"
    encrypted = ("-----BEGIN RSA PRIVATE KEY-----\nProc-Type: 4,ENCRYPTED\nDEK-Info: AES-128-CBC,0123ABCD\n\n"
                 "MIIEpAIBAAKCAQEA\n-----END RSA PRIVATE KEY-----")
    assert rre.private_key_block(f"key:\n{block}\n{encrypted}\n") == [block, encrypted]
    assert rre.private_key_block("-----BEGIN PUBLIC KEY-----\nMIIB\n-----END PUBLIC KEY-----") == []


def test_ssh_public_key():
    key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB"
    assert rre.ssh_public_key(f"authorized_keys: {key} jane@laptop.local.") == [f"{key} jane@laptop.local"]
    assert rre.ssh_public_key(f"{key}\n") == [key]
    assert rre.ssh_public_key("ssh-rsa AAAAB3NzaC1yc2E is too short") == []


def test_password_hash():
    # published test vectors: bcrypt (Wikipedia), sha256/512-crypt (Drepper's spec), yescrypt and scrypt
    # (yescrypt's TESTS-OK), argon2 (reference README), phpass
    hashes = [
        "$2a$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW",
        "$5$saltstring$5B8vYYiY.CVt1RlTTf8KbXBH3hsxY/GNooZaBBGWEc5",
        "$6$rounds=10000$saltstringsaltst$OW1/O6BYHV6BcXZu8QVeXbDWra3Oeqh0sbHbbMCVNSnCM/UrjmM0Dp8vOuZeHBy/"
        "YTBmSK6H9qs/y3RnOaw5v.",
        "$y$jC4$qiyh2SQgE5vrF3ORvFho$HurI7MuukXHz..TpxrwKuakji/j9VKDh2WVUK4DIsq5",
        "$7$C6..../....SodiumChloride$kBGj9fHznVYFQMEn/qDCfrDevf9YDtcDdKvEqHJLV8D",
        "$argon2i$v=19$m=65536,t=2,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG",
        "$P$9IQRaTwmfeRo7ud9Fh4E2PdI0S3r.L0",
        "$1$saltsalt$qjXMvbEw8oaL.CzflDtaK/",
        "pbkdf2_sha256$870000$seasalt$5Ucm+TZNGTRiT4rClzbZ1W5HjdB4mJCKS6vx7hlWsFs=",
    ]
    shadow = "\n".join(f"user{i}:{h}:19000:0:99999:7:::" for i, h in enumerate(hashes))
    assert rre.password_hash(shadow) == hashes
    assert rre.password_hash("$6$saltstring$tooshort, $2a$12$short and $5$ off") == []


def test_sha512():
    sha = ("cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce"
           "47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e")
    assert rre.sha512(f"sha512 {sha}") == [sha]
    assert rre.sha512(sha[:-1]) == []


def test_hex_color():
    assert rre.hex_color("color: #ff0000; fill='#1A2B3C' #ffffff80 background:#fff") == [
        "#ff0000", "#1A2B3C", "#ffffff80", "#fff"]
    # a color has a letter a-f, and the short forms count only after ':', '=', a quote or '(' (CSS, HTML):
    # issue and order numbers, years, hashtags and unit numbers are not colors
    assert rre.hex_color("issue #123, order #123456, #2024, #bad #cafe, apt #12A") == []


def test_drug_emoji():
    # the emoji variation selector (U+FE0F) is part of the match
    assert rre.drug_emoji("\u2744\ufe0f\u2744 \U0001F3B1, \U0001F48A \U0001F344 \U0001F50C") == [
        "\u2744\ufe0f", "\u2744", "\U0001F3B1", "\U0001F48A", "\U0001F344", "\U0001F50C"]
    assert rre.drug_emoji("\U0001F525\U0001F680\U0001F4AF \U0001F600") == []


def test_url_not_numbers():
    assert rre.url("see politie.be, mail.google.com and seehttp://www.test.be") == [
        "politie.be", "mail.google.com", "http://www.test.be"]
    assert rre.url("paid 249.99 on 12.03.2024 from 192.168.1.1") == []


def test_url_hosts():
    assert rre.url("my-site.com, x.com and https://sub.domain.example.co.uk/x") == [
        "my-site.com", "x.com", "https://sub.domain.example.co.uk"]
    # the last label is lowercase or capitals: a name is no domain
    assert rre.url("Dhr. J.Peeters and Mr.Smith") == []


def test_url_not_email():
    assert rre.url("mail jan.peeters+x@test.be or jan.van.der.berg@x.co.uk") == []


def test_long_runs_stay_fast():
    # email and url used to retry from every position of a run without spaces: minutes on a 100 KB hex dump.
    # The last run checks that url looks at most 64 characters ahead for an email's @.
    start = time.perf_counter()
    for text in ('aB3_' * 12500, 'a.' * 25000, 'NL' * 25000, '1' * 50000, 'a-' * 25000, '1.' * 25000, 'ab.' * 33333 + '@'):
        rre.email(text), rre.url(text), rre.gps_coordinates(text), rre.ip_address(text)
    assert time.perf_counter() - start < 1


def test_imeisv():
    # the IMEI 49-015420-323751-8 without its check digit, software version 81
    assert rre.imeisv("IMEISV: 4901542032375181, IMEI SV 49-015420-323751-81, imei/sv=49015420 323751 81") == [
        "IMEISV: 4901542032375181", "IMEI SV 49-015420-323751-81", "imei/sv=49015420 323751 81"]
    # no keyword, or an IMEI (15 digits) after it
    assert rre.imeisv("4901542032375181 and IMEISV: 490154203237518") == []


def test_meid():
    # 3GPP2 X.S0008's example: AF 01 23 45 0A BC DE has check digit C, its decimal form 29360 87365 0070 3710 has 0
    assert rre.meid("MEID: AF0123450ABCDE, MEID HEX AF 01 23 45 0A BC DE C, MEID DEC: 29360 87365 0070 3710 0") == [
        "MEID: AF0123450ABCDE", "MEID HEX AF 01 23 45 0A BC DE C", "MEID DEC: 29360 87365 0070 3710 0"]
    # an IMEI's first 14 digits, with the IMEI's check digit
    assert rre.meid("MEID 35 209900 176148 1 and meid: A10000009296F2") == [
        "MEID 35 209900 176148 1", "meid: A10000009296F2"]
    # wrong check digit, hex digits without an A0-FF prefix, no keyword
    assert rre.meid("MEID: AF0123450ABCDED, MEID 12AB3450ABCDE0, AF0123450ABCDE") == []


def test_esn():
    # 0x80ABCDEF in decimal: manufacturer code 128, serial number 11259375
    assert rre.esn("ESN: 80ABCDEF, pESN 801A2B3C, ESN (DEC) 128 11259375") == [
        "ESN: 80ABCDEF", "pESN 801A2B3C", "ESN (DEC) 128 11259375"]
    # a manufacturer code over 255, nine hex digits, no keyword
    assert rre.esn("ESN 99912345678, ESN: 80ABCDEF0, 80ABCDEF") == []


def test_mcc_mnc():
    text = 'MCC 206, MNC 01; PLMN: 20601; <apn mcc="262" mnc="01"/>; ims.mnc001.mcc206.3gppnetwork.org'
    assert rre.mcc_mnc(text) == ["MCC 206, MNC 01", "PLMN: 20601", 'mcc="262" mnc="01', "mnc001.mcc206"]
    assert rre.mcc_mnc("[gsm.sim.operator.numeric]: [20810], HPLMN 310-260") == [
        "operator.numeric]: [20810", "HPLMN 310-260"]
    # Android's cell identity, an MNC without its leading zero, and JSON
    assert rre.mcc_mnc('CellIdentityGsm:{ mLac=1234 mMcc=206 mMnc=1 }, {"mcc": "208", "mnc": "10"}') == [
        "mMcc=206 mMnc=1", 'mcc": "208", "mnc": "10']
    # no such country code (1xx is reserved), and no keyword
    assert rre.mcc_mnc("MCC 199 MNC 01, PLMN 10001, mnc001.mcc100, room 206-01, postcode 26201") == []


def test_apple_serial_number():
    assert rre.apple_serial_number(
        "Serial Number: C02XL0GHJGH5, S/N F2LXK123HG7F, numéro de série : H4Q9KXF2LJ, Serial No.: YM9234ABCDE") == [
        "Serial Number: C02XL0GHJGH5", "S/N F2LXK123HG7F", "numéro de série : H4Q9KXF2LJ", "Serial No.: YM9234ABCDE"]
    # an iTunes backup's Info.plist
    assert rre.apple_serial_number("<key>Serial Number</key>\n\t<string>F2LXK123HG7F</string>") == [
        "Serial Number</key>\n\t<string>F2LXK123HG7F"]
    # no keyword, only digits or only letters, no year letter in 4th place, Spanish s/n (sin número)
    assert rre.apple_serial_number(
        "C02XL0GHJGH5, Serial: 12345678901, serial ABCDEFGHJK, Serial C02AL0GHJGH5, Calle Mayor s/n 28001") == []


def test_ios_udid():
    old = "0a1b2c3d4e" * 4
    assert rre.ios_udid(f"device 00008030-001A2B3C4D5E802E, UDID: {old}") == [
        "00008030-001A2B3C4D5E802E", f"UDID: {old}"]
    assert rre.ios_udid(f"<key>Unique Identifier</key>\n\t<string>{old}</string>") == [
        f"Unique Identifier</key>\n\t<string>{old}"]
    # 40 hex without the keyword is a SHA-1, and a UUID has other groups
    assert rre.ios_udid(f"{old} and 550e8400-e29b-41d4-a716-446655440000") == []


def test_apple_ecid():
    assert rre.apple_ecid("ECID: 0x1A2B3C4D5E6F7, UniqueChipID: 460367961908983") == [
        "ECID: 0x1A2B3C4D5E6F7", "UniqueChipID: 460367961908983"]
    assert rre.apple_ecid("0x1A2B3C4D5E6F7 and ECID 12") == []


def test_android_id():
    # settings_secure.xml before Android 8 (the leading zero dropped)
    text = 'Android ID: 3f2b9c71d04e8a65, <setting id="12" name="android_id" value="3f2b9c71d04e8a6" />'
    assert rre.android_id(text) == ["Android ID: 3f2b9c71d04e8a65", 'android_id" value="3f2b9c71d04e8a6']
    # no keyword, 17 hex digits
    assert rre.android_id("3f2b9c71d04e8a65 and Android ID: 3f2b9c71d04e8a65f") == []


def test_app_package_name():
    assert rre.app_package_name(
        "com.whatsapp, org.telegram.messenger, net.whatsapp.WhatsApp, ph.telegra.Telegraph, ch.threema.app, "
        "/data/data/com.tencent.mm/databases, Preferences/com.apple.mobilesafari.plist, com.whatsapp_preferences.xml, "
        "details?id=com.google.android.gm, group.net.whatsapp.WhatsApp.shared, network.loki.messenger") == [
        "com.whatsapp", "org.telegram.messenger", "net.whatsapp.WhatsApp", "ph.telegra.Telegraph", "ch.threema.app",
        "com.tencent.mm", "com.apple.mobilesafari", "com.whatsapp", "com.google.android.gm",
        "group.net.whatsapp.WhatsApp.shared", "network.loki.messenger"]
    # web addresses, file names, versions, e-mail addresses and words joined by dots or without a space after one
    assert rre.app_package_name(
        "www.example.com, de.wikipedia.org, ec.europa.eu, app.example.io, example.co.uk, com.au, report.final.docx, "
        "my.cv.pdf, v2.0.1, e.g. it.Then, me.thanks, is.it.ok, il.fait.beau, jan@com.example, de.smet@example.be") == []


def test_ussd_code():
    assert rre.ussd_code("dial *#06#, *100#, *139*1*1234567890#, **21*+32470123456#, ##002# or *#*#4636#*#*") == [
        "*#06#", "*100#", "*139*1*1234567890#", "**21*+32470123456#", "##002#", "*#*#4636#*#*"]
    # #31# hides the caller ID of the number dialled after it
    assert rre.ussd_code("#31#0470123456") == ["#31#"]
    assert rre.ussd_code("#2024#, issue #12, **bold**, 5*3# and a*100#") == []


def test_tel_uri():
    assert rre.tel_uri(
        '<a href="tel:+32470123456">, tel:+1-201-555-0123;ext=1234, sms:+32470123456?body=Hello%20there. '
        "smsto:0470123456 (tel:+32(0)470123456)") == [
        "tel:+32470123456", "tel:+1-201-555-0123;ext=1234", "sms:+32470123456?body=Hello%20there",
        "smsto:0470123456", "tel:+32(0)470123456"]
    # a label with a spaced-out number is no URI
    assert rre.tel_uri("Tel: +32 470 12 34 56, tel:0470 12 34 56, hotel:12345") == []


def test_mac_address_placeholders():
    assert rre.mac_address("wifi 00:1A:2B:3C:4D:5E, bt 00-1a-2b-3c-4d-5f") == ["00:1A:2B:3C:4D:5E", "00-1a-2b-3c-4d-5f"]
    # what Android and iOS report instead of the real address, all zeros and broadcast
    assert rre.mac_address("02:00:00:00:00:00, 00-00-00-00-00-00, FF:FF:FF:FF:FF:FF, ff-ff-ff-ff-ff-ff") == []


def test_device_ids_stay_fast():
    start = time.perf_counter()
    for text in ('com.a' * 20000, 'ab.' * 33333, 'tel:+1' + '-1' * 50000, 'sms:1?' + '.' * 100000, '*1' * 50000,
                 'MEID ' + 'A' * 100000, 'Serial ' + '1' * 100000, 'MCC 206 ' * 12500, 'fF0' * 33333):
        for fn in (rre.imeisv, rre.meid, rre.esn, rre.mcc_mnc, rre.apple_serial_number, rre.ios_udid, rre.apple_ecid,
                   rre.android_id, rre.app_package_name, rre.ussd_code, rre.tel_uri, rre.mac_address):
            fn(text)
    assert time.perf_counter() - start < 1


def test_whatsapp_jid():
    assert rre.whatsapp_jid("from 32470123456@s.whatsapp.net, web 32470123456@c.us, device 32470123456:12@s.whatsapp.net") == [
        "32470123456@s.whatsapp.net", "32470123456@c.us", "32470123456:12@s.whatsapp.net"]
    assert rre.whatsapp_jid("group 120363012345678901@g.us, old group 32470123456-1500000000@g.us, 123456789012345@lid, "
                            "status@broadcast") == [
        "120363012345678901@g.us", "32470123456-1500000000@g.us", "123456789012345@lid", "status@broadcast"]
    # avatar file names carry the JID
    assert rre.whatsapp_jid("/files/Avatars/32470123456@s.whatsapp.net.j") == ["32470123456@s.whatsapp.net"]
    assert rre.whatsapp_jid("mail 32470123456@example.com, 32470123456@s.whatsapp.network, 12345@g.us, 0@s.whatsapp.net") == []


def test_sip_uri():
    assert rre.sip_uri("call sip:alice@example.com or <sips:bob@voip.example.org:5061;transport=tls>.") == [
        "sip:alice@example.com", "sips:bob@voip.example.org:5061;transport=tls"]
    assert rre.sip_uri("SIP:+32470123456@sip.example.com;user=phone, sip:1001@192.0.2.10:5060, registrar sip:example.com.") == [
        "SIP:+32470123456@sip.example.com;user=phone", "sip:1001@192.0.2.10:5060", "sip:example.com"]
    assert rre.sip_uri("Sip: slowly, sip:water and gossip:alice@example.com") == []


def test_skype_id():
    assert rre.skype_id("skype live:.cid.1a2b3c4d5e6f7a8b, 8:live:.cid.1a2b3c4d5e6f and 8:live:jane.example_1.") == [
        "live:.cid.1a2b3c4d5e6f7a8b", "8:live:.cid.1a2b3c4d5e6f", "8:live:jane.example_1"]
    assert rre.skype_id("chat 8:jane.example, teams 8:orgid:2f1a2b3c-4d5e-4f60-8a7b-9c0d1e2f3a4b") == [
        "8:jane.example", "8:orgid:2f1a2b3c-4d5e-4f60-8a7b-9c0d1e2f3a4b"]
    assert rre.skype_id("going live: tonight at 8:30, score 8:jane, rtmp://live:1935/app") == []


def test_search_query_url():
    assert rre.search_query_url("https://www.google.com/search?q=test+query&oq=test and bing.com/search?q=test%20query.") == [
        "https://www.google.com/search?q=test+query", "bing.com/search?q=test%20query"]
    assert rre.search_query_url("https://duckduckgo.com/?t=h_&q=test+query&ia=web "
                                "https://www.youtube.com/results?search_query=test+video "
                                "https://search.yahoo.com/search;_ylt=AbC?p=test+query&fr=yfp-t") == [
        "https://duckduckgo.com/?t=h_&q=test+query", "https://www.youtube.com/results?search_query=test+video",
        "https://search.yahoo.com/search;_ylt=AbC?p=test+query"]
    assert rre.search_query_url("ecosia.org/search?method=index&q=test qwant.com/?q=test&t=web "
                                "startpage.com/sp/search?query=test search.brave.com/search?q=test "
                                "yandex.ru/search/?lr=1&p=2&text=test baidu.com/s?wd=test") == [
        "ecosia.org/search?method=index&q=test", "qwant.com/?q=test", "startpage.com/sp/search?query=test",
        "search.brave.com/search?q=test", "yandex.ru/search/?lr=1&p=2&text=test", "baidu.com/s?wd=test"]
    # a redirect, a video, a map and a query that was never sent are not searches
    assert rre.search_query_url("https://www.google.com/url?q=https://example.com youtube.com/watch?v=abc "
                                "google.com/maps?q=x google.com/search?oq=test notgoogle.com/search?q=x") == []


def test_otpauth_uri():
    # the example of Google Authenticator's key URI format, with a made-up account
    uri = "otpauth://totp/Example:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"
    assert rre.otpauth_uri(f"qr {uri}.") == [uri]
    assert rre.otpauth_uri("otpauth://hotp/Test?counter=0&secret=GEZDGNBVGY3TQOJQ "
                           "otpauth-migration://offline?data=CjEKCkhlbGxv%3D") == [
        "otpauth://hotp/Test?counter=0&secret=GEZDGNBVGY3TQOJQ", "otpauth-migration://offline?data=CjEKCkhlbGxv%3D"]
    assert rre.otpauth_uri("otpauth://totp/Example?issuer=Example, otpauth://sms/x?secret=AB") == []


def test_wifi_qr_string():
    assert rre.wifi_qr_string("scan WIFI:T:WPA;S:TestNet;P:test-pass;; to join") == ["WIFI:T:WPA;S:TestNet;P:test-pass;;"]
    # fields in any order, escaped ; : and \, an open network
    assert rre.wifi_qr_string(r"WIFI:S:Test\;Net;T:WPA;P:pa\:ss\;H:true;; WIFI:T:nopass;S:Guest Net;;") == [
        r"WIFI:S:Test\;Net;T:WPA;P:pa\:ss\;H:true;;", "WIFI:T:nopass;S:Guest Net;;"]
    assert rre.wifi_qr_string("WIFI:T:WPA;P:test-pass;; (no network name), WIFI: S:TestNet;") == []


def test_paypal_me_link():
    assert rre.paypal_me_link("pay paypal.me/testuser, https://www.paypal.me/TestUser/25EUR or "
                              "paypal.com/paypalme/testuser/10.50.") == [
        "paypal.me/testuser", "https://www.paypal.me/TestUser/25EUR", "paypal.com/paypalme/testuser/10.50"]
    # names are letters and digits, at most 20; money pools are no names
    assert rre.paypal_me_link("paypal.me/test-user paypal.me/abcdefghijklmnopqrstu paypal.me/pools/c/8abc "
                              "paypal.com/be/home") == []


def test_revolut_link():
    assert rre.revolut_link("revolut.me/testuser1 or "
                            "https://checkout.revolut.com/payment-link/0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d") == [
        "revolut.me/testuser1", "https://checkout.revolut.com/payment-link/0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"]
    # Revtags are 3 to 16 letters and digits
    assert rre.revolut_link("revolut.me/ab revolut.me/test_user revolut.com/en-BE") == []


def test_payconiq_link():
    # the payload formats of Bancontact Payconiq's documentation, with made-up ids
    assert rre.payconiq_link("https://payconiq.com/l/1/0a1b2c3d4e5f6a7b8c9d0e1f/POS00001, "
                             "https://pay.bancontact.net/pay/2/abc123def456ghi789jkl012.") == [
        "https://payconiq.com/l/1/0a1b2c3d4e5f6a7b8c9d0e1f/POS00001",
        "https://pay.bancontact.net/pay/2/abc123def456ghi789jkl012"]
    assert rre.payconiq_link("https://payconiq.com/t/1/0a1b2c3d4e5f6a7b8c9d0e1f?D=Invoice%20Payment&A=250&R=123456789101 "
                             "HTTPS://PAYCONIQ.COM/PAY/2/ABC123DEF456GHI789JKL012") == [
        "https://payconiq.com/t/1/0a1b2c3d4e5f6a7b8c9d0e1f?D=Invoice%20Payment&A=250&R=123456789101",
        "HTTPS://PAYCONIQ.COM/PAY/2/ABC123DEF456GHI789JKL012"]
    assert rre.payconiq_link("payconiq.be/en/private, payconiq.com/pay/ and pay.bancontact.net/?checkoutApi=x") == []


def test_verification_code_message():
    assert rre.verification_code_message("Your WhatsApp code: 123-456. Don't share this code") == [
        "Your WhatsApp code: 123-456"]
    assert rre.verification_code_message("G-123456 is your Google verification code. Telegram code: 12345") == [
        "123456 is your Google verification code", "Telegram code: 12345"]
    assert rre.verification_code_message("123 456 is your Instagram code; Your one-time passcode is 482913.") == [
        "123 456 is your Instagram code", "one-time passcode is 482913"]
    # Dutch, French, German
    assert rre.verification_code_message("Je verificatiecode is 482913. 123456 is je Facebook-code") == [
        "verificatiecode is 482913", "123456 is je Facebook-code"]
    assert rre.verification_code_message("Votre code de vérification est : 482913. 123456 est votre code Facebook") == [
        "Votre code de vérification est : 482913", "123456 est votre code"]
    assert rre.verification_code_message("Ihr Bestätigungscode lautet 482913. 123456 ist dein Instagram-Code") == [
        "Bestätigungscode lautet 482913", "123456 ist dein Instagram-Code"]
    assert rre.verification_code_message(
        "exit code 137, zip code 10001, your postal code is 2000, Code pénal article 222, 1234 lines of code, "
        "promo code SPRING24, verification code sent to +32470123456") == []


def test_machine_sender():
    assert rre.machine_sender("From: Example <noreply@example.com>, no-reply@accounts.example.com, ne-pas-repondre@example.fr") == [
        "noreply@example.com", "no-reply@accounts.example.com", "ne-pas-repondre@example.fr"]
    assert rre.machine_sender("niet-beantwoorden@example.be newsletter@example.com nieuwsbrief@example.nl "
                              "MAILER-DAEMON@example.com bounces+123-abc=example.com@em.example.com") == [
        "niet-beantwoorden@example.be", "newsletter@example.com", "nieuwsbrief@example.nl", "MAILER-DAEMON@example.com",
        "bounces+123-abc=example.com@em.example.com"]
    # the word as a whole part of the user name, between dots, hyphens or the like
    assert rre.machine_sender("drive-shares-noreply@example.com, do_not_reply@example.com") == [
        "drive-shares-noreply@example.com", "do_not_reply@example.com"]
    assert rre.machine_sender("jan.peeters@example.com info@newsletter.example.com noreplyx@example.com "
                              "mynewsletter@example.com noreply@") == []


def test_unsubscribe_text():
    assert rre.unsubscribe_text("Click here to unsubscribe. Opt-out") == ["unsubscribe", "Opt-out"]
    assert rre.unsubscribe_text("Uitschrijven | Afmelden | Meld je hier af | Se désabonner | désinscription | "
                                "Newsletter abbestellen | hier abmelden") == [
        "Uitschrijven", "Afmelden", "Meld je hier af", "désabonner", "désinscription", "abbestellen", "abmelden"]
    assert rre.unsubscribe_text("subscribe now, the outcome, an option out of town") == []


def test_automated_message_text():
    assert rre.automated_message_text("This is an automated message, please do not reply.") == [
        "automated message", "please do not reply"]
    assert rre.automated_message_text("Dit bericht is automatisch verzonden. Message automatique, merci de ne pas y répondre. "
                                      "Diese E-Mail wurde automatisch generiert.") == [
        "automatisch verzonden", "Message automatique", "ne pas y répondre", "automatisch generiert"]
    assert rre.automated_message_text("the automatic door, a message he generated, I will reply, je ne peux pas répondre") == []


def test_named_groups_messaging():
    # rre returns the whole match; the raw patterns also name the part an analyst is after
    import json
    import re
    from pathlib import Path

    import regular_regexes
    patterns = json.loads((Path(regular_regexes.__file__).parent / 'intl' / 'regexes.json').read_text(encoding='utf-8'))

    def groups(name, text):
        return re.search(patterns[name], text).groupdict()

    assert groups('whatsapp_jid', 'jid 32470123456:12@s.whatsapp.net') == {'phone': '32470123456'}
    assert groups('whatsapp_jid', '32470123456-1500000000@g.us') == {'phone': '32470123456'}
    assert groups('whatsapp_jid', '123456789012345@lid') == {'phone': None}
    assert groups('sip_uri', 'sip:alice@example.com;transport=tcp') == {'user': 'alice', 'host': 'example.com'}
    assert groups('search_query_url', 'https://duckduckgo.com/?t=h_&q=test+query&ia=web') == {'query': 'test+query'}
    assert groups('search_query_url', 'https://search.yahoo.com/search?fr=yfp-t&p=test+query') == {'query': 'test+query'}
    assert groups('otpauth_uri', 'otpauth://totp/Example:test@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Example') == {
        'label': 'Example:test@example.com', 'secret': 'JBSWY3DPEHPK3PXP'}
    assert groups('wifi_qr_string', 'WIFI:T:WPA;S:TestNet;P:test-pass;;') == {'ssid': 'TestNet', 'password': 'test-pass'}
    assert groups('paypal_me_link', 'paypal.me/testuser/25EUR') == {'user': 'testuser', 'amount': '25EUR'}
    assert groups('revolut_link', 'revolut.me/testuser1') == {'revtag': 'testuser1'}
    assert groups('payconiq_link', 'https://payconiq.com/l/1/0a1b2c3d4e5f6a7b8c9d0e1f/POS00001') == {
        'id': '0a1b2c3d4e5f6a7b8c9d0e1f'}
    assert groups('verification_code_message', 'G-123456 is your Google verification code') == {'code': '123456'}
    assert groups('machine_sender', 'noreply-alerts@example.com') == {'local': 'noreply-alerts'}


def test_ios_app_container_path():
    guid = "0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D"
    for path in (
        f"/private/var/mobile/Containers/Data/Application/{guid}/Documents/notes.sqlite",
        f"/private/var/mobile/Containers/Shared/AppGroup/{guid}/Library/Preferences/x.plist",
        f"/private/var/mobile/Containers/Data/PluginKitPlugin/{guid}/tmp/x.jpg",
        f"/private/var/containers/Bundle/Application/{guid}/Example.app/Info.plist",
        f"/var/mobile/Containers/Data/Application/{guid}",
    ):
        assert rre.ios_app_container_path(path) == [path]
    for path in (
        "/private/var/mobile/Library/SMS/sms.db",
        "/private/var/mobile/Containers/Data/Application/Example/x.jpg",
        f"/private/var/mobile/Containers/Data/Application/{guid}0/x.jpg",
        f"/private/var/containers/Shared/SystemGroup/{guid}/x.plist",
        f"path /private/var/mobile/Containers/Data/Application/{guid}/x.jpg",
    ):
        assert rre.ios_app_container_path(path) == []


def test_android_app_data_path():
    for path in (
        "/data/data/com.example.app/databases/messages.db",
        "/data/user/0/com.example.app/shared_prefs/settings.xml",
        "/data/user_de/10/com.example.app/files/x",
        "/storage/emulated/0/Android/media/com.example.app/Media/x.jpg",
        "/sdcard/Android/data/org.example.chat/cache/x.png",
        "/data/media/0/Android/obb/com.example.game/main.obb",
        "/data/data/com.example.app",
    ):
        assert rre.android_app_data_path(path) == [path]
    for path in (
        "/data/system/usagestats/0/daily/1",
        "/data/app/com.example.app-1/base.apk",
        "/data/data/example/x",
        "/data/data/com.example.app-1/x",
        "/storage/emulated/0/DCIM/Camera/x.jpg",
        "text /data/data/com.example.app/x",
    ):
        assert rre.android_app_data_path(path) == []


def test_app_cache_path():
    for path in (
        "/data/data/com.example.app/cache/image_manager_disk_cache/1.0",
        "/private/var/mobile/Containers/Data/Application/0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D/Library/Caches/x.jpg",
        "/storage/emulated/0/DCIM/.thumbnails/1234.jpg",
        "/private/var/mobile/Media/PhotoData/Thumbnails/V2/DCIM/100APPLE/IMG_0001.JPG/5005.JPG",
        "/data/data/com.example.app/files/emoji/1f600.png",
        "/data/data/com.example.app/files/stickers/pack_1/x.webp",
        "/data/app/com.example.app/base.apk/res/drawable-xxhdpi/icon.png",
    ):
        assert rre.app_cache_path(path) == [path]
    for path in (
        "/storage/emulated/0/DCIM/Camera/IMG_20260302_081512.jpg",
        "/storage/emulated/0/Pictures/cachet/x.jpg",
        "/data/data/com.example.app/cache",
        "relative/cache/x.jpg",
        "text /data/data/com.example.app/cache/x.jpg",
    ):
        assert rre.app_cache_path(path) == []


def test_camera_filename():
    assert rre.camera_filename(
        "IMG_20260302_081512.jpg PXL_20260302_081512123.MP.jpg VID_20260302_081512.mp4 IMG_0001.HEIC DSC01234.JPG") == [
        "IMG_20260302_081512.jpg", "PXL_20260302_081512123.MP.jpg", "VID_20260302_081512.mp4", "IMG_0001.HEIC",
        "DSC01234.JPG"]
    # Samsung has no prefix, Oppo no underscores; bursts and copies, other cameras, in a path
    assert rre.camera_filename(
        "/DCIM/Camera/20260302_081512.jpg 20260302_081512(1).jpg IMG20260302081512.jpg "
        "IMG_20260302_081512_BURST001.jpg IMG_E0001.HEIC DSC_0001.NEF GOPR0001.MP4 DJI_0001.JPG") == [
        "20260302_081512.jpg", "20260302_081512(1).jpg", "IMG20260302081512.jpg", "IMG_20260302_081512_BURST001.jpg",
        "IMG_E0001.HEIC", "DSC_0001.NEF", "GOPR0001.MP4", "DJI_0001.JPG"]
    # messenger and screenshot names, an impossible date, other files with a date, no extension
    assert rre.camera_filename(
        "IMG-20260303-WA0007.jpg Screenshot_20260302_081512.png signal-2026-03-03-091244.jpg IMG_20261302_081512.jpg "
        "backup_20260302_081512.jpg IMG_0001 build 20260302.1 IMG_0001.txt") == []


def test_screenshot_filename():
    assert rre.screenshot_filename(
        "Screenshot_20260302-081512.png Screenshot_20260302-081512_Example App.jpg "
        "Screenshot_2026-03-02-08-15-12-123_com.example.app.jpg Screenshot 2026-03-02 at 08.15.12.png") == [
        "Screenshot_20260302-081512.png", "Screenshot_20260302-081512_Example App.jpg",
        "Screenshot_2026-03-02-08-15-12-123_com.example.app.jpg", "Screenshot 2026-03-02 at 08.15.12.png"]
    # macOS in other languages and with AM/PM, Windows 11, GNOME
    assert rre.screenshot_filename(
        "Schermafbeelding 2026-03-02 om 08.15.12.png Capture d’écran 2026-03-02 à 08.15.12.png "
        "Bildschirmfoto 2026-03-02 um 08.15.12.png Screen Shot 2026-03-02 at 8.15.12 AM (2).png "
        "Screenshot 2026-03-02 081512.png Screenshot from 2026-03-02 08-15-12.png") == [
        "Schermafbeelding 2026-03-02 om 08.15.12.png", "Capture d’écran 2026-03-02 à 08.15.12.png",
        "Bildschirmfoto 2026-03-02 um 08.15.12.png", "Screen Shot 2026-03-02 at 8.15.12 AM (2).png",
        "Screenshot 2026-03-02 081512.png", "Screenshot from 2026-03-02 08-15-12.png"]
    assert rre.screenshot_filename(
        "Screenshot.png Screenshot (12).png Screenshots/x.png Screenshot_20260302-081512 IMG_20260302_081512.jpg") == []


def test_whatsapp_media_filename():
    assert rre.whatsapp_media_filename(
        "IMG-20260303-WA0007.jpg PTT-20260303-WA0007.opus VID-20260303-WA0001.mp4 STK-20260303-WA0012.webp "
        "WhatsApp Image 2026-03-03 at 09.12.44.jpeg WhatsApp Video 2026-03-03 at 9.12.44 PM (1).mp4") == [
        "IMG-20260303-WA0007.jpg", "PTT-20260303-WA0007.opus", "VID-20260303-WA0001.mp4", "STK-20260303-WA0012.webp",
        "WhatsApp Image 2026-03-03 at 09.12.44.jpeg", "WhatsApp Video 2026-03-03 at 9.12.44 PM (1).mp4"]
    # a camera name, an impossible date, no extension, no time, a chat export
    assert rre.whatsapp_media_filename(
        "IMG_20260303_091244.jpg IMG-20261303-WA0007.jpg IMG-20260303-WA0007 WhatsApp Image 2026-03-03.jpeg "
        "WhatsApp Chat with Example.txt") == []


def test_messenger_media_filename():
    # Signal (older and current Android, Desktop), Telegram Desktop and Telegram's chat export
    assert rre.messenger_media_filename(
        "signal-2026-03-03-091244.jpg signal-2026-03-03-09-12-44-123.jpg signal-2026-03-03-09-12-44-123_003.mov "
        "photo_2026-03-03_09-12-44.jpg video_2026-03-03_09-12-44 (2).mp4 "
        "chats/chat_01/photos/photo_1@03-03-2026_09-12-44.jpg voice_messages/audio_2@03-03-2026_09-12-44.ogg") == [
        "signal-2026-03-03-091244.jpg", "signal-2026-03-03-09-12-44-123.jpg", "signal-2026-03-03-09-12-44-123_003.mov",
        "photo_2026-03-03_09-12-44.jpg", "video_2026-03-03_09-12-44 (2).mp4", "photo_1@03-03-2026_09-12-44.jpg",
        "audio_2@03-03-2026_09-12-44.ogg"]
    assert rre.messenger_media_filename(
        "signal-2026-13-03-091244.jpg photo_2026-03-03.jpg photo_album.jpg file_1@example.com "
        "IMG-20260303-WA0007.jpg") == []


def test_exif_datetime():
    assert rre.exif_datetime("DateTimeOriginal: 2026:03:02 08:15:12, ExifTool 2026:03:02 08:15:12.123+01:00") == [
        "2026:03:02 08:15:12", "2026:03:02 08:15:12.123+01:00"]
    # unset (zeros), an impossible month, ISO, a longer run of colons
    assert rre.exif_datetime(
        "0000:00:00 00:00:00, 2026:13:02 08:15:12, 2026-03-02 08:15:12, 2026:03:02 08:15:12:34, ISO 9001:2015") == []


def test_cellebrite_datetime():
    assert rre.cellebrite_datetime(
        "sent 2/3/2026 8:15:12(UTC+1), read 14/09/2026 09:15:00(UTC+05:30), 3/2/2026 8:15:12 AM(UTC+0), "
        "02.03.2026 08:15:12 (UTC +1)") == [
        "2/3/2026 8:15:12(UTC+1)", "14/09/2026 09:15:00(UTC+05:30)", "3/2/2026 8:15:12 AM(UTC+0)",
        "02.03.2026 08:15:12 (UTC +1)"]
    # without the offset in brackets it is any date and time
    assert rre.cellebrite_datetime("2/3/2026 8:15:12, 14:30 (UTC+1) on 2/3/2026, 2026-03-02T08:15:12+01:00") == []


def test_windows_timezone_name():
    for name in (
        "(UTC+01:00) Brussels, Copenhagen, Madrid, Paris",
        "(UTC-05:00) Eastern Time (US & Canada)",
        "(UTC+03:00) Moscow, St. Petersburg",
        "(UTC-03:00) City of Buenos Aires",
        "(UTC+12:00) Petropavlovsk-Kamchatsky - Old",
        "(UTC) Coordinated Universal Time",
        "(UTC+01:00) Brussel, Kopenhagen, Madrid, Parijs",
        "(UTC+01:00) Bruxelles, Copenhague, Madrid, Paris",
    ):
        assert rre.windows_timezone_name(f"Time zone: {name}.") == [name]
    # a time with its zone in a sentence, an offset without minutes, other words after (UTC), lowercase words
    assert rre.windows_timezone_name("at 14:00 (UTC+01:00) Monday, 09:15:00(UTC+05:30) Sent, (UTC+1) Paris, "
                                     "(UTC) Weather, (UTC+01:00) local time") == []


def test_unix_timestamp():
    assert rre.unix_timestamp(
        'Unix time 1772409600, {"timestamp": 1772409600123, "date_sent": "1772409600"}, url?ts=1772409600&x=1, '
        'epoch: 1772409600, /data/system/usagestats/0/daily/1772409600000 '
        '/data/system_ce/0/usagestats/weekly/1772409600000') == [
        "Unix time 1772409600", '"timestamp": 1772409600123', '"date_sent": "1772409600"', "ts=1772409600",
        "epoch: 1772409600", "usagestats/0/daily/1772409600000", "usagestats/weekly/1772409600000"]
    # a bare number, a key that is no time, outside 2000-2040, a plain word without a separator
    assert rre.unix_timestamp('order 1772409600, "id": 1772409600, timestamp: 3000000000, date: 0470123456, '
                              'at that time 1772409600 people') == []


def test_exif_gps_rational():
    assert rre.exif_gps_rational("GPSLatitude 51/1, 15/1, 4536/100 GPSLongitude 4/1 22/1 451200/10000") == [
        "51/1, 15/1, 4536/100", "4/1 22/1 451200/10000"]
    # fractions and dates, minutes above 59, more than 180 degrees, a denominator that is no power of ten
    assert rre.exif_gps_rational(
        "1/2, 1/4, 3/4 cup; 12/03, 14/03, 15/03; 51/1, 75/1, 0/1; 200/1, 0/1, 0/1; 51/1, 15/1, 4536/99") == []


def test_gps_dms_deg():
    # ExifTool and Cellebrite write the word deg instead of °
    assert rre.gps_dms("51 deg 15' 45.36\" N, 4 deg 22' 45.12\" E") == ["51 deg 15' 45.36\" N", "4 deg 22' 45.12\" E"]
    assert rre.gps_dms("21 deg C, an angle of 45 deg 10'") == []


def test_named_groups_files():
    # the library returns the whole match; the raw patterns also give these parts as named groups
    import json
    import re
    from pathlib import Path

    import regular_regexes
    patterns = json.loads((Path(regular_regexes.__file__).parent / 'intl' / 'regexes.json').read_text(encoding='utf-8'))

    def groups(name, text):
        entry = patterns[name]
        return re.search(entry['regex'] if isinstance(entry, dict) else entry, text).groupdict()

    guid = "0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D"
    assert groups('ios_app_container_path', f"/private/var/containers/Bundle/Application/{guid}/x") == {'guid': guid}
    assert groups('android_app_data_path', "/data/user/0/com.example.app/files/x") == {'package': 'com.example.app'}
    assert groups('camera_filename', "PXL_20260302_081512123.jpg") == {'date': '20260302', 'time': '081512'}
    assert groups('screenshot_filename', "Screenshot 2026-03-02 at 08.15.12.png") == {'date': '2026-03-02',
                                                                                      'time': '08.15.12'}
    assert groups('whatsapp_media_filename', "IMG-20260303-WA0007.jpg") == {'date': '20260303', 'time': None}
    assert groups('messenger_media_filename', "photo_1@03-03-2026_09-12-44.jpg") == {'date': '03-03-2026',
                                                                                      'time': '09-12-44'}
    assert groups('unix_timestamp', '"date_sent": "1772409600"') == {'timestamp': '1772409600'}


def test_device_regexes_stay_fast():
    # runs of each regex's own prefix and of its separators (100 KB each)
    start = time.perf_counter()
    for text in ('/a' * 50000, 'IMG_' * 25000, '20260302_081512 ' * 6250, 'Screenshot_20260302-081512_a ' * 3500,
                 '"timestamp": ' * 7700, 'timetime' * 12500, '1/1,' * 25000, '(UTC+01:00) Aa, ' * 6250, '1' * 100000):
        for name in ('app_cache_path', 'camera_filename', 'screenshot_filename', 'whatsapp_media_filename',
                     'messenger_media_filename', 'exif_datetime', 'cellebrite_datetime', 'windows_timezone_name',
                     'unix_timestamp', 'exif_gps_rational', 'gps_dms'):
            getattr(rre, name)(text)
    assert time.perf_counter() - start < 1


def test_ethereum_tx_hash():
    # made up: the SHA-256 of "test"
    tx = "0x9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    assert rre.ethereum_tx_hash(f"paid, tx {tx} (https://etherscan.io/tx/{tx})") == [tx, tx]
    # an address, the hash without 0x, 66 and 63 hex characters
    assert rre.ethereum_tx_hash(f"0x{'a' * 40} {tx[2:]} 0x{'a' * 66} {tx[:-1]}") == []


def test_solana_address():
    # made up: the base58 of 32 bytes 0..31 and of a SHA-256
    a, b = "1thX6LZfHDZZKUs92febYZhYRcXddmzfzF2NvTkPNE", "4XtRjD178mXbpmAk1LJGb5cJewxaaZtMw7QknyM79kT4"
    assert rre.solana_address(f"my Solana address: {a}, pay solana:{b}?amount=1") == [
        f"Solana address: {a}", f"solana:{b}"]
    assert rre.solana_address(f"send 2 SOL to {b} or solscan.io/account/{a}") == [
        f"SOL to {b}", f"solscan.io/account/{a}"]
    # no keyword; a Bitcoin address (25 bytes); 44 characters that decode to 33 bytes
    assert rre.solana_address(f"{b} sol 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa, sol {'z' * 44}") == []


def test_dogecoin_address():
    # Dogecoin's base58 test vectors (src/test/data/base58_keys_valid.json): P2PKH and two P2SH
    assert rre.dogecoin_address("DD4KSSuBJqcjuTcvUg1CgUKeurPUFeEZkE, A7HRQk3GFCW2QasvdZxXuYj8kkQK5QrYLs or "
                                "9zYnVRaekPtdKBYuPw5QiBtv3NNrzD2LLW") == [
        "DD4KSSuBJqcjuTcvUg1CgUKeurPUFeEZkE", "A7HRQk3GFCW2QasvdZxXuYj8kkQK5QrYLs", "9zYnVRaekPtdKBYuPw5QiBtv3NNrzD2LLW"]
    # checksum broken; valid base58check with version byte 31 (made up); a testnet address
    assert rre.dogecoin_address("DD4KSSuBJqcjuTcvUg1CgUKeurPUFeEZkF DUUijPpZLwQdgQPEph3JdK5ocKikzEXNbz "
                                "nhRsrUaxZou6sewjqaS37cJrMRJRgwVXdk") == []


def test_bitcoin_cash_address():
    # CashAddr spec and CashTokens test vectors: P2PKH with and without its prefix, in capitals, P2SH, token-aware
    p2pkh = "bitcoincash:qr6m7j9njldwwzlg9v7v53unlr4jkmx6eylep8ekg2"
    assert rre.bitcoin_cash_address(f"bch {p2pkh} or {p2pkh[12:]}, QR: {p2pkh.upper()}") == [
        p2pkh, p2pkh[12:], p2pkh.upper()]
    p2sh, token = ("bitcoincash:ppm2qsznhks23z7629mms6s4cwef74vcwvn0h829pq",
                   "bitcoincash:zr7fzmep8g7h7ymfxy74lgc0v950j3r295z4y4gq0v")
    assert rre.bitcoin_cash_address(f"{p2sh}?amount=0.1 {token}") == [p2sh, token]
    # testnet, mixed case, checksum broken
    assert rre.bitcoin_cash_address("bchtest:pr6m7j9njldwwzlg9v7v53unlr4jkmx6eyvwc0uz5t "
                                    f"bitcoincash:{p2pkh[12:].upper()} {p2pkh[:-1]}3") == []


def test_ens_name():
    assert rre.ens_name("send to jane-example.eth, pay.jane-example.eth. or @jane-example.eth") == [
        "jane-example.eth", "pay.jane-example.eth", "jane-example.eth"]
    # too short, code, a longer domain, an amount, an interface
    assert rre.ens_name("ab.eth web3.eth.getBalance jane-example.eth.example.com 0.5 ETH eth0") == []


def test_mmsi():
    # MID 200 is not allocated: no real ship
    text = 'ship MMSI 200123456, group MMSI: 020012345, coast MMSI-nummer 002001234, {"mmsi": 992001234}'
    assert rre.mmsi(text) == ["MMSI 200123456", "MMSI: 020012345", "MMSI-nummer 002001234", 'mmsi": 992001234']
    assert rre.mmsi("SART MMSI no. 970012345") == ["MMSI no. 970012345"]
    # no keyword, no MID, ten digits
    assert rre.mmsi("200123456, MMSI 123456789, MMSI 2001234567") == []


def test_dhl_tracking_number():
    # made up, apart from DHL's own examples JJD0099999999 and JVGL9999999999
    assert rre.dhl_tracking_number("DHL waybill 1234567891, DHL Express: 12 3456 7891 and JJD0099999999") == [
        "DHL waybill 1234567891", "DHL Express: 12 3456 7891", "JJD0099999999"]
    assert rre.dhl_tracking_number("dhl Paket 123456789016, DHL 00340434123456789012, JVGL9999999999") == [
        "dhl Paket 123456789016", "DHL 00340434123456789012", "JVGL9999999999"]
    # check digits wrong, no keyword
    assert rre.dhl_tracking_number("DHL 1234567890, DHL 123456789017, DHL 00340434123456789013, 1234567891") == []


def test_dpd_tracking_number():
    # made up
    assert rre.dpd_tracking_number("DPD-pakket 01501234567890, DPD 0150 1234 5678 90 S, dpd: 01501234567890s") == [
        "DPD-pakket 01501234567890", "DPD 0150 1234 5678 90 S", "dpd: 01501234567890s"]
    # no keyword, check character wrong, 16 digits
    assert rre.dpd_tracking_number("01501234567890, DPD 01501234567890X, DPD 0150123456789012") == []


def test_gls_tracking_number():
    # 36631234567 is GLS's own example; the check digit added to it is made up
    assert rre.gls_tracking_number("GLS pakket 36631234567, GLS parcel number: 366312345673") == [
        "GLS pakket 36631234567", "GLS parcel number: 366312345673"]
    # check digit wrong, no keyword, a bank account
    assert rre.gls_tracking_number("GLS 366312345674, 36631234567, GLS Bank IBAN DE12 4306 0967 1234 5678 00") == []


def test_crypto_and_parcel_regexes_stay_fast():
    start = time.perf_counter()
    for text in ('sol ' * 25000, 'a.' * 50000 + 'eth', 'DHL ' * 25000, 'q' * 100000, 'DPD 0150 ' * 11000):
        rre.solana_address(text), rre.ens_name(text), rre.dhl_tracking_number(text), rre.bitcoin_cash_address(text)
        rre.dpd_tracking_number(text), rre.gls_tracking_number(text), rre.mmsi(text), rre.dogecoin_address(text)
    assert time.perf_counter() - start < 1
