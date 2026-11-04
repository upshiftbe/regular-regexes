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
        "/private/var/MobileAsset/AssetsV2/com_apple_MobileAsset_VoiceServicesVocalizerVoice/x.asset/AssetData/x.wav",
        "/var/MobileAsset/AssetsV2/x/x.ttf",
    ):
        assert rre.ios_system_path(path) == [path]
    for path in (
        "/private/var/mobile/Media/DCIM/100APPLE/IMG_0001.HEIC",
        "/private/var/mobile/Library/Caches/x.png",
        "/private/var/containers/Bundle/Application/X/App.app/x.png",
        "/system/media/x.ogg",
        "/private/var/mobile/Media/MobileAsset/x.png",
        "/private/var/MobileAssetx/x",
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
