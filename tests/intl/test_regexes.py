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


# BOLT 11 test vectors: 2500u (a cup of coffee), 20m with a hashed description, testnet, all upper case
_LN_COFFEE = ("lnbc2500u1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq"
              "5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpu9qrsgquk0rl77nj30yxdy8j9vdx85fkpmdla2087ne0xh"
              "8nhedh8w27kyke0lp53ut353s06fv3qfegext0eh0ymjpf39tuven09sam30g4vgpfna3rh")
_LN_HASHED = ("lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqqsyqcyq5r"
              "qwzqfqqqsyqcyq5rqwzqfqypqhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahrqs9qrsgq7ea976txfraylv"
              "gzuxs8kgcw23ezlrszfnh8r6qtfpr6cxga50aj6txm9rxrydzd06dfeawfk6swupvz4erwnyutnjq7x39ymw6j38gp7ynn44")
_LN_TESTNET = ("lntb20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhdzgynm4zwqd5"
               "d7xmw5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqfpp3x9et2e20v6pu37c5"
               "d9vax37wxq72un989qrsgqdj545axuxtnfemtpwkc45hx9d2ft7x04mt8q7y6t0k2dge9e7h8kpy9p34ytyslj3yu569aalz2xdk"
               "8xkd7ltxqld94u8h2esmsmacgpghe9k8")
_LN_UPPER = ("LNBC25M1PVJLUEZPP5QQQSYQCYQ5RQWZQFQQQSYQCYQ5RQWZQFQQQSYQCYQ5RQWZQFQYPQDQ5VDHKVEN9V5SXYETPDEESSP5ZYG3"
             "ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYGS9Q5SQQQQQQQQQQQQQQQQSGQ2A25DXL5HRNTDTN6ZVYDT7D66HYZS"
             "YHQS4WDYNAVYS42XGL6SGX9C4G7ME86A27T07MDTFRY458RTJR0V92CNMSWPSJSCGT2VCSE3SGPZ3UAPA")


def test_crypto_lightning_invoice():
    # made up: bech32 over 140 bytes, for signet with 10n and regtest with 2500p
    signet = ("lntbs10n10awyma4autjr39yg53d8dd720x2as45z8phthgk4utdtqrnp9g5u9gs8shvxev8fgr8zyf3ll2fn093ts352kd0ftxk"
              "emdk3xu7s8q2ju27k5lquce3jcs07y4hgtrejvfvgazpmn5s8l9azvy08mj7j5tt72gtn45jkw8xasg22qf0e3m59wtpfsxtgc0e"
              "akdk0sappkes23fjs4eyxaf52ceqq83feck2pvy")
    regtest = ("lnbcrt2500p15ryj3yw74dxw7t7gnte6e57wgxcu0q35dqzc7l7a5mw7erhjtmwvrt3w9y48tktsfcgx5t44wfn227qhj9aue8y3p"
               "nt67rem4un0ltygypuzmp33fmryxh2984n6hx5hnag6majpmxmt4w5v7mxqphwukq70cwzptanncrgqrdt8qq9jw2ah6cwayxs9e"
               "v2z2zrr64xkz8hjtf9fsvuucaxywlc7s40zjh704a")
    assert rre.lightning_invoice(_LN_COFFEE) == [_LN_COFFEE]
    assert rre.lightning_invoice(f"pay lightning:{_LN_HASHED} please") == [_LN_HASHED]
    assert rre.lightning_invoice(f"QR: LIGHTNING:{_LN_UPPER}") == [_LN_UPPER]
    assert rre.lightning_invoice(f'test ({_LN_TESTNET}), "{signet}"; <{regtest}>.') == [_LN_TESTNET, signet, regtest]
    assert rre.lightning_invoice(f"bitcoin:bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4?lightning={_LN_COFFEE}\n") == [
        _LN_COFFEE]
    assert rre.lightning_invoice(f"{_LN_COFFEE}\n{_LN_COFFEE.upper()}") == [_LN_COFFEE, _LN_COFFEE.upper()]


def test_crypto_lightning_invoice_rejects():
    # BOLT 11's invalid invoices: checksum, too short (no signature), unknown multiplier x
    bad_checksum = ("lnbc2500u1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpquwpc4curk03c9wlrswe78q4ey"
                    "qc7d8d0xqzpuyk0sg5g70me25alkluzd2x62aysf2pyy8edtjeevuv4p2d5p76r4zkmneet7uvyakky2zr4cusd45tftc9c5fh0n"
                    "nqpnl2jfll544esqchsrnt")
    too_short = ("lnbc1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpl2pkx2ctnv5sxxmmwwd5kgetjypeh2u"
                 "rsdae8g6na6hlh")
    multiplier = ("lnbc2500x1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpu"
                  "sp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9qrsgqrrzc4cvfue4zp3hggxp47ag7xnrlr8vgcmkjxk3"
                  "j5jqethnumgkpqp23z9jclu3v0a7e0aruz366e9wqdykw6dxhdzcjjhldxq0w6wgqcnu43j")
    assert rre.lightning_invoice(f"{bad_checksum} {too_short} {multiplier}") == []
    # a character short or too many, the mainnet invoice relabelled testnet, glued to a word
    assert rre.lightning_invoice(f"{_LN_COFFEE[:-1]} {_LN_COFFEE}q {_LN_COFFEE.replace('lnbc', 'lntb')}") == []
    assert rre.lightning_invoice(f"x{_LN_COFFEE} {_LN_COFFEE}_x") == []
    # a SegWit address and an LNURL
    assert rre.lightning_invoice("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4 LNURL1DP68GURN8GHJ7ETCV9KHQMR99E3K7MF0D3H82U"
                                 "NVWQHK5CTWV5ZSTSSD") == []


def test_crypto_lnurl():
    # LUD-01's example, and one made up for https://example.com/lnurlp/jane
    lud = ("LNURL1DP68GURN8GHJ7UM9WFMXJCM99E3K7MF0V9CXJ0M385EKVCENXC6R2C35XVUKXEFCV5MKVV34X5EKZD3EV56NYD3HXQURZEPEXEJ"
           "XXEPNXSCRVWFNV9NXZCN9XQ6XYEFHVGCXXCMYXYMNSERXFQ5FNS")
    jane = "LNURL1DP68GURN8GHJ7ETCV9KHQMR99E3K7MF0D3H82UNVWQHK5CTWV5ZSTSSD"
    assert rre.lnurl(lud) == [lud]
    assert rre.lnurl(f"scan lightning:{lud}.") == [lud]
    assert rre.lnurl(f"https://service.com/giftcard?lightning={lud}&x=1") == [lud]
    assert rre.lnurl(f'"{jane.lower()}" ({jane})') == [jane.lower(), jane]
    assert rre.lnurl(f"withdraw:\n{jane}\n") == [jane]
    assert rre.lnurl(f"{lud}, {jane}") == [lud, jane]
    # checksum broken, a character short, glued to a word, LUD-17's lnurlp:// scheme, too short (made up: https://a.b)
    assert rre.lnurl(f"{jane[:-1]}A {jane[:-1]} x{jane} lnurlp://example.com/lnurlp/jane lnurl1dp68gurn8ghj7cfwvg8cuzpc") == []
    # a Lightning address, a Lightning invoice, mixed alphabets
    assert rre.lnurl(f"jane@example.com {_LN_COFFEE} LNURL1DP68GURN8GHJ7ETCV9KHQMR99E3K7MF0D3H82UNVWQHK5CTWV5ZSTSSB") == []


def test_crypto_nostr_key():
    # NIP-19 test vectors (npub, nsec); the note ID is made up
    npub = "npub10elfcs4fr0l0r8af98jlmgdh9c8tcxjvz9qkw038js35mp4dma8qzvjptg"
    nsec = "nsec1vl029mgpspedva04g90vltkh6fvh240zqtv9k0t9af8935ke9laqsnlfe5"
    note = "note16n4yeq4fast8ytnh4vazr9edk3u9egrftdmn3l8asvpl8qv4wtlstqrvpk"
    assert rre.nostr_key(npub) == [npub]
    assert rre.nostr_key(f"follow me: nostr:{npub}, my key {nsec}.") == [npub, nsec]
    assert rre.nostr_key(f'["e", "{note}"] (https://njump.me/{note})') == [note, note]
    assert rre.nostr_key(f"QR {npub.upper()}\n{nsec}") == [npub.upper(), nsec]
    # checksum broken, a character short and one too many, prefixes swapped (the checksum covers them)
    assert rre.nostr_key(f"{npub[:-1]}h {npub[:-1]} {npub}q {nsec.replace('nsec', 'npub')} {note.replace('note', 'nsec')}") == []
    # glued to a word, the key in hex, nprofile and other prefixes, a Lightning invoice
    assert rre.nostr_key(f"x{npub} 7e7e9c42a91bfef19fa929e5fda1b72e0ebc1a4c1141673e2794234d86addf4e "
                         f"nkey1{npub[5:]} {_LN_COFFEE}") == []


def test_crypto_ethereum_private_key():
    # made up: the SHA-256 of "ethkey0"
    key = "d0fca5a191812186c0c178b719ae2c9e302b76c960e35b809e4c97c13f04eaef"
    assert rre.ethereum_private_key(f"PRIVATE_KEY=0x{key}") == [f"PRIVATE_KEY=0x{key}"]
    assert rre.ethereum_private_key(f'{{"address": "0x{key[:40]}", "privateKey": "0x{key}"}}') == [
        f'privateKey": "0x{key}']
    assert rre.ethereum_private_key(f"Your private key:\n\n{key.upper()}\nNever share it") == [
        f"private key:\n\n{key.upper()}"]
    assert rre.ethereum_private_key(f"export WALLET_PRIVKEY='{key}'; Clé privée : 0x{key}.") == [
        f"PRIVKEY='{key}", f"Clé privée : 0x{key}"]
    assert rre.ethereum_private_key(f"Privésleutel: {key} (privater Schlüssel) - {key}") == [
        f"Privésleutel: {key}", f"privater Schlüssel) - {key}"]
    assert rre.ethereum_private_key(f"clave privada [{key}], chiave privata {key}, klucz prywatny: {key}") == [
        f"clave privada [{key}", f"chiave privata {key}", f"klucz prywatny: {key}"]
    # no keyword, one hex character short or too many, 0x and 66, a public key, the keyword too far off, no separator
    assert rre.ethereum_private_key(f"{key} private key: {key[:-1]} private key: {key}a private key: 0x{key}00") == []
    assert rre.ethereum_private_key(f"public key: {key}, private key of the old wallet: {key}, privatekey{key}") == []
    # a g in the key, a 128-character key, a PEM key
    assert rre.ethereum_private_key(f"private key: {key[:-1]}g, private key: {key}{key}") == []
    assert rre.ethereum_private_key("-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEIBkg4LVWM9nuwNSk3yByxZpYRTBnVJk5oA==") == []


def test_crypto_cardano_address():
    # CIP-19 test vectors: base, pointer and enterprise addresses, stake addresses (key and script)
    base = ("addr1qx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3n0d3vllmyqwsx5wktcd8cc3sq835lu7drv2xwl2wywfgse35a3x")
    pointer = "addr1gx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer5pnz75xxcrzqf96k"
    enterprise = "addr1vx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzers66hrl8"
    stake, stake_script = ("stake1uyehkck0lajq8gr28t9uxnuvgcqrc6070x3k9r8048z8y5gh6ffgw",
                           "stake178phkx6acpnf78fuvxn0mkew3l0fd058hzquvz7w36x4gtcccycj5")
    # made up: Byron addresses of the Icarus (Ae2...) and Daedalus (DdzFF...) wallets
    icarus = "Ae2tdPwUPEZBrFkSj7HEsHBm4Nb1hV3tDV8ajYz8SriLJqYLCVHcwrQLnN2"
    daedalus = ("DdzFFzCqrhsjcBGqhFrw4C1ZtBKr3PzNz9SdRTfTHWMx2P8ikTn3MfhSRM3MpS8Xfgjij9iP5prs7AiExS3S2ktWrRMSGCiKzoJe"
                "sB5M")
    assert rre.cardano_address(base) == [base]
    assert rre.cardano_address(f"https://cardanoscan.io/address/{pointer}, ({enterprise}).") == [pointer, enterprise]
    assert rre.cardano_address(f'stake "{stake}" or {stake_script}\n') == [stake, stake_script]
    assert rre.cardano_address(f"old wallet: {icarus}; {daedalus}") == [icarus, daedalus]
    assert rre.cardano_address(f"[{daedalus}]") == [daedalus]
    assert rre.cardano_address(f"web+cardano:{enterprise}?amount=10") == [enterprise]
    # checksum broken, a character short, testnet (addr_test1, and CIP-19's Byron example), capitals, glued to a word
    assert rre.cardano_address(f"{base[:-1]}y {enterprise[:-1]} addr_test1vz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydz"
                               f"erspjrlsz {enterprise.upper()} x{stake}") == []
    assert rre.cardano_address("37btjrVyb4KDXBNC4haBVPCrro8AQPHwvCMp3RFhhSVWwfFmZ6wwzSK6JK1hY6wHNmtrpTf1kdbva8TCneM2Ysi"
                               "XT7mrzT21EacHnPpz5YyUdj64na") == []
    # Byron with a character changed (CRC32), one short, one too many
    assert rre.cardano_address(f"{icarus[:-1]}3 {icarus[:-1]} {icarus}z {daedalus[:-1]}N") == []
    # a stake address one character too long, a SegWit address, a Monero-like base58 run
    assert rre.cardano_address(f"{stake}q bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4 4A{'x' * 93}") == []


def test_crypto_polkadot_address():
    # Substrate's well-known development account Alice, in generic Substrate (42), Polkadot (0) and Kusama (2) form
    alice, alice_dot, alice_ksm = ("5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
                                   "15oF4uVJwmo4TdGW7VfQxNLavjCXviqxT9S1MgbjMNHr6Sp5",
                                   "HNZata7iMYWmk5RvZRTiAsSDhV8366zq2YGb3tLH5Upf74F")
    # made up: a 47-character Polkadot address, Kusama addresses starting with C and J
    dot47, ksm_c, ksm_j = ("1CLihzstohVzsczjJbLvqKjPyYV1VquDcahyLQ4DGrATPYH",
                           "Cfj5bdmVzpCyzLjGn4tg6ndVEwxVVzNr3Tv3PUGrUj8DLd2", "J7yu2DALbLuKsV8bfZze81tdWaHfEZhV8aMoWoky75xtLNQ")
    assert rre.polkadot_address(alice) == [alice]
    assert rre.polkadot_address(f"send DOT to {alice_dot}, KSM to {alice_ksm}.") == [alice_dot, alice_ksm]
    assert rre.polkadot_address(f"https://polkadot.subscan.io/account/{dot47}?tab=transfer") == [dot47]
    assert rre.polkadot_address(f'("{ksm_c}", "{ksm_j}")') == [ksm_c, ksm_j]
    assert rre.polkadot_address(f"{alice}\n{alice_dot}") == [alice, alice_dot]
    assert rre.polkadot_address(f"[{alice_ksm}]") == [alice_ksm]
    # checksum broken, a character short, one too many, glued to a word
    assert rre.polkadot_address(f"{alice[:-1]}R {alice[:-1]} {alice}z x{alice_dot}") == []
    # a valid SS58 address with prefix 43, not one of Polkadot, Kusama or Substrate; a Bitcoin address; a base58 run
    assert rre.polkadot_address(f"5NecBZmeUHQKB9fT4PVSC7mribMBHbvLZbFep5FgG8rpCNS2 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa "
                                f"{'5' * 48} {'1' * 47}") == []
    # a Solana-style 44-character key and an IPFS hash (Qm..., 46)
    assert rre.polkadot_address("4XtRjD178mXbpmAk1LJGb5cJewxaaZtMw7QknyM79kT4 "
                                "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG") == []


def test_crypto_cosmos_address():
    # made up: bech32 of SHA-256 bytes
    atom, valoper = ("cosmos12wtuazg5tjtcutw29saqeeuu697xt48cgq3hmh",
                     "cosmosvaloper12wtuazg5tjtcutw29saqeeuu697xt48cd59zhy")
    contract = "osmo137eh8r48hsmgqjc7nvcsyekae5w9vh6y4davmewhjkxy7zw66ksqh9m689"
    inj, tia, rune = ("inj126p36z7vntlgam5x8sjyjj0v4cpm4en5r6mcpj", "celestia1yaej308t2vc3lncaueedxgpj9phzgnmzze7fa2",
                      "thor1gtpp776kaueaxczmg5pjqpydyuefpxwnshvzs4")
    assert rre.cosmos_address(atom) == [atom]
    assert rre.cosmos_address(f"https://www.mintscan.io/cosmos/validators/{valoper}") == [valoper]
    assert rre.cosmos_address(f'contract "{contract}", ({inj}).') == [contract, inj]
    assert rre.cosmos_address(f"{tia}\n{rune}") == [tia, rune]
    assert rre.cosmos_address(f"send to [{atom}], memo 12345") == [atom]
    assert rre.cosmos_address(f"from {inj} to {atom}") == [inj, atom]
    # checksum broken, a character short and one too many, another chain's prefix on the same data
    assert rre.cosmos_address(f"{atom[:-1]}j {atom[:-1]} {atom}q osmo1{atom[7:]}") == []
    # a chain not in the list (made up: band1...), capitals, glued to a word, a SegWit address
    assert rre.cosmos_address(f"band1spansh3cxe8tkzlczwq5mstm9p9akan0r2rwsx {atom.upper()} x{atom} "
                              "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4") == []


def test_crypto_stellar_address():
    # SEP-23 test vectors: an account and two muxed accounts; one made up
    account = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
    muxed, muxed2 = ("MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVAAAAAAAAAAAAAJLK",
                     "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUQ")
    made_up = "GAVZRUGOTOS4Q6B43XJVUTEXELB4VY3ZQKFS3QEVMA55JSZKGPSDDNCQ"
    assert rre.stellar_address(account) == [account]
    assert rre.stellar_address(f"web+stellar:pay?destination={made_up}&amount=10") == [made_up]
    assert rre.stellar_address(f"https://stellar.expert/explorer/public/account/{account}.") == [account]
    assert rre.stellar_address(f'("{muxed}", {muxed2})') == [muxed, muxed2]
    assert rre.stellar_address(f"XLM: {made_up}\nmemo 123") == [made_up]
    assert rre.stellar_address(f"[{account}] {muxed}") == [account, muxed]
    # SEP-23's invalid ones: algorithm 7, a trailing bit set, checksum, 57 and 70 characters
    assert rre.stellar_address("G47QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVP2I "
                               "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUR "
                               "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAAAAAAAACJUO "
                               "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZA "
                               "MA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVAAAAAAAAAAAAAJLKA") == []
    # a character short, lower case, glued to a word, a secret seed (S...), a contract (C...)
    assert rre.stellar_address(f"{account[:-1]} {account.lower()} X{account} "
                               "SAVZRUGOTOS4Q6B43XJVUTEXELB4VY3ZQKFS3QEVMA55JSZKGPSDCJRP "
                               "CA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUWDA") == []


def test_crypto_zcash_address():
    # made up: base58check with the t1 and t3 version bytes, bech32 (zs1) and bech32m (u1) of SHA-256 bytes
    t1, t3 = "t1gzrYQxjzxY84DdGQA47sHB3vHrKCxtkqa", "t3fkzjtuX4NZHYy34zbb3fqcgonNDHV79Ch"
    zs = "zs1nac2pzuuxsjvkvuqfnjy8pdhrf4068dcglhk8khzyzht8sa3up29mp0fdtjk0ft3faghk6z5xm4"
    ua = "u1nhqzyg76gf3cgf52pdyfk29spprypx2fr9nlduze0pf7jwv486sthqsrpk7zhj46x25shuhzq75y4pt0chcr8dmufqyrd2m0wugzsuff"
    assert rre.zcash_address(t1) == [t1]
    assert rre.zcash_address(f"zcash:{t3}?amount=1.5") == [t3]
    assert rre.zcash_address(f'shielded "{zs}", unified ({ua}).') == [zs, ua]
    assert rre.zcash_address(f"{ua}\n{t1}") == [ua, t1]
    assert rre.zcash_address(f"ZEC [{t1}] or {zs}") == [t1, zs]
    assert rre.zcash_address(f"https://mainnet.zcashexplorer.app/address/{t3}") == [t3]
    # checksum broken in each form, a character short
    assert rre.zcash_address(f"{t1[:-1]}b {zs[:-1]}5 {ua[:-1]}g {t1[:-1]} {zs[:-1]}") == []
    # one too many, glued to a word, a testnet address (made up, tm...), a Bitcoin address, capitals
    assert rre.zcash_address(f"{t3}z x{t1} tmYqbsFT9Pd3dCTpi4tMriwqoXGw8mGwC9u 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa "
                             f"{zs.upper()}") == []


def test_crypto_dash_address():
    # made up: base58check with Dash's version bytes 76 (X...) and 16 (7...)
    x, p2sh = "XgNSWgGvrWBeJpBKbJyDpRJL2q1DofCwz2", "7iwu5gwHpPmA2DudPwyediNdkyP9xhoTVd"
    assert rre.dash_address(x) == [x]
    assert rre.dash_address(f"dash:{x}?amount=0.5") == [x]
    assert rre.dash_address(f'P2SH "{p2sh}" ({x}).') == [p2sh, x]
    assert rre.dash_address(f"{p2sh}\n[{x}]") == [p2sh, x]
    assert rre.dash_address(f"https://insight.dash.org/insight/address/{x}") == [x]
    assert rre.dash_address(f"pay {p2sh}, thanks") == [p2sh]
    # checksum broken, a character short and one too many, glued to a word
    assert rre.dash_address(f"{x[:-1]}3 {x[:-1]} {x}z a{x} {p2sh[:-1]}e") == []
    # valid base58check with version 75 (also X...), Bitcoin, Dogecoin and Tron addresses
    assert rre.dash_address("XH2qXZye9KimVP3EZtduLJ2YQKkH8GxDah 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa "
                            "DD4KSSuBJqcjuTcvUg1CgUKeurPUFeEZkE TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t") == []


def test_crypto_ton_address():
    # made up: a bounceable (EQ) and a non-bounceable (UQ) address, in base64url and in base64
    eq, eq_std = "EQBE-sdHHG9Kz_4osTNj27fVJTLelI8ReGdXSff3npQU22f3", "EQBE+sdHHG9Kz/4osTNj27fVJTLelI8ReGdXSff3npQU22f3"
    uq, uq_std = "UQA1GzQQSS9TTcMzmQCxmmvcI-D8TB1VHRRSJbf1xiowooS-", "UQA1GzQQSS9TTcMzmQCxmmvcI+D8TB1VHRRSJbf1xiowooS+"
    assert rre.ton_address(eq) == [eq]
    assert rre.ton_address(f"ton://transfer/{uq}?amount=1000000000") == [uq]
    assert rre.ton_address(f"https://tonviewer.com/{eq_std}, ({uq_std}).") == [eq_std, uq_std]
    assert rre.ton_address(f'"{uq}"\n[{eq}]') == [uq, eq]
    assert rre.ton_address(f"USDT on TON: {uq}. Thanks") == [uq]
    assert rre.ton_address(f"{eq_std}/{uq}") == [eq_std, uq]
    # checksum broken, a character short and one too many, glued to a word or inside a longer token
    assert rre.ton_address(f"{eq[:-1]}4 {eq[:-1]} {eq}A x{eq} {uq}-x") == []
    # testnet (kQ...), masterchain (Ef8...), the raw form, lower case
    assert rre.ton_address("kQAvSRzMdgyurt69rbMA5KzEocn-LLnvqcEUMZwHKuyiUvpB "
                           "Ef8vSRzMdgyurt69rbMA5KzEocn-LLnvqcEUMZwHKuyiUr6D "
                           f"0:44fac7471c6f4acffe28b13363dbb7d52532de948f11786757c9f7f79e9414db {eq.lower()}") == []


def test_crypto_regexes_stay_fast():
    # runs of each regex's prefixes and alphabet, and words that pass the regex and run the validator (100 KB each)
    start = time.perf_counter()
    for text in ('lnbc1' * 20000, ('lnbc1' + 'q' * 170 + ' ') * 568, 'npub1q' * 16667, ('addr1' + 'q' * 53 + ' ') * 1695,
                 ('cosmos1' + 'q' * 38 + ' ') * 2173, ('5' + 'z' * 47 + ' ') * 2040, ('GA' + 'A' * 54 + ' ') * 1754,
                 ('zs1' + 'q' * 75 + ' ') * 1265, ('EQA' + 'A' * 44 + '/') * 2083, 'private key: ' * 7700,
                 ('X' + 'z' * 33 + ' ') * 2857, 'Ae2' * 33333, 'qpzry9x8gf2tvdw0s3jn54khce6mua7l' * 3125):
        for name in ('lightning_invoice', 'lnurl', 'nostr_key', 'ethereum_private_key', 'cardano_address',
                     'polkadot_address', 'cosmos_address', 'stellar_address', 'zcash_address', 'dash_address',
                     'ton_address'):
            getattr(rre, name)(text)
    assert time.perf_counter() - start < 1


def test_messaging_tox_id():
    # made up: the SHA-256 of a word as public key, nospam 0A1B2C3D and its checksum
    tox = "81F8F6DDE88365F3928796EC7AA53F72820B06DB8664F5FE76A7EB13E24546A20A1B2C3D53D6"
    other = "50D858E0985ECC7F60418AAF0CC5AB587F42C2570A884095A9E8CCACD0F6545C0A1B2C3D21AA"
    assert rre.tox_id(f"{tox} is my Tox ID; tox:{other}") == [tox, other]
    assert rre.tox_id(f'Contact us (Tox ID: {tox.lower()}), "{other}". Pay in 48h to {tox}') == [
        tox.lower(), other, tox]
    assert rre.tox_id(f"[{tox}]\n'{other}'") == [tox, other]
    # one character short or long, checksum wrong, mixed case, inside a longer token
    assert rre.tox_id(f"{tox[:-1]} {tox}A {tox[:-1]}7 {tox[:40].lower()}{tox[40:]} key_{tox} {tox}-2") == []
    # filler whose XOR is 0000, a SHA-256 and a Session ID
    assert rre.tox_id("0" * 76 + " " + "FF" * 36 + "0000 " + "AB" * 36 + "0000") == []
    assert rre.tox_id(f"{tox[:64]} 05{tox[:64].lower()}") == []


def test_messaging_simplex_link():
    # made up keys and queues
    key, link_id = "Ab1_" * 10 + "Cd2", "Ef3-" * 8
    smp = ("smp%3A%2F%2FAbCdEfGhIjKlMnOpQrStUvWxYz0123456789-_Ab%3D%40smp.example.com%2FQwErTyUiOpAsDfGh"
           "%23%2F%3Fv%3D1-3%26dh%3DMCowBQYDK2VuAyEAexampleexampleexample%253D")
    contact = f"https://simplex.chat/contact#/?v=2-7&smp={smp}"
    invitation = f"simplex:/invitation#/?v=2-7&smp={smp}&e2e=v%3D2-3"
    assert rre.simplex_link(f"my address: {contact}. Or scan {invitation}") == [contact, invitation]
    assert rre.simplex_link(f"(simplex.chat/contact#/?v=1&smp={smp})") == [f"simplex.chat/contact#/?v=1&smp={smp}"]
    short = [f"https://smp4.simplex.im/a#{key}", f"https://smp.example.com/i#{link_id}/{key}",
             f"simplex:/g#{key}?h=smp.example.com,smp2.example.net&p=5223", f"smp.example.com:5223/c#{key}="]
    assert rre.simplex_link(f"{short[0]} '{short[1]}', \"{short[2]}\", [{short[3]}]") == short
    assert rre.simplex_link(f"group: {short[2]}. HTTPS://SMP4.SIMPLEX.IM/r#{key}") == [
        short[2], f"HTTPS://SMP4.SIMPLEX.IM/r#{key}"]
    # key one character short or long, no link ID, wrong type, a page anchor, no queue
    assert rre.simplex_link(f"https://smp4.simplex.im/a#{key[:-1]} https://smp4.simplex.im/a#{key}x "
                            f"https://smp.example.com/i#{key} https://smp.example.com/x#{key} "
                            "https://example.com/a#section-one https://simplex.chat/contact#/?v=2-7") == []
    assert rre.simplex_link(f"https://simplex.chat/blog/ simplex:/a# xsimplex:/a#{key} x.com/a_{key}") == []


def test_messaging_discord_user_id():
    # made up snowflakes
    assert rre.discord_user_id("<@412345678901234567> hey, <@!1234567890123456789>, ask <@81234567890123456>") == [
        "<@412345678901234567>", "<@!1234567890123456789>", "<@81234567890123456>"]
    assert rre.discord_user_id("https://discord.com/users/412345678901234567 (Discordapp.com/USERS/81234567890123456)"
                               ) == ["https://discord.com/users/412345678901234567", "Discordapp.com/USERS/81234567890123456"]
    assert rre.discord_user_id("Discord ID: 412345678901234567, discord user id 1234567890123456789.") == [
        "Discord ID: 412345678901234567", "discord user id 1234567890123456789"]
    assert rre.discord_user_id('{"discord_id": "412345678901234567"} DISCORD-ID=81234567890123456') == [
        'discord_id": "412345678901234567', "DISCORD-ID=81234567890123456"]
    # a role, a channel, 16 digits, another app's mention
    assert rre.discord_user_id("<@&412345678901234567> <#412345678901234567> <@4123456789012345> <@U024BE7LH>") == []
    # 16 or 20 digits, no keyword, inside a longer word, a channel link
    assert rre.discord_user_id("Discord ID: 4123456789012345, Discord ID 41234567890123456789, user 412345678901234567, "
                               "mydiscord id 412345678901234567, discord.com/channels/412345678901234567/1") == []


def test_messaging_discord_webhook_url():
    token = "Ab1_-Cd2" * 8 + "Ef3G"  # made up, 68 characters like a real token
    hook = f"https://discord.com/api/webhooks/1234567890123456789/{token}"
    assert rre.discord_webhook_url(f'WEBHOOK = "{hook}"') == rre.discord_webhook_url(hook) == [hook]
    assert rre.discord_webhook_url(f"post to {hook}?wait=true and {hook}/slack.") == [hook, hook]
    others = [f"discordapp.com/api/webhooks/412345678901234567/{token}",
              f"https://ptb.discord.com/api/v10/webhooks/412345678901234567/{token}",
              f"HTTPS://Canary.Discord.com/api/v9/webhooks/81234567890123456/{token[:60]}"]
    assert rre.discord_webhook_url(f"({others[0]}) {others[1]}, {others[2]}") == others
    # token too short or too long
    assert rre.discord_webhook_url(f"discord.com/api/webhooks/412345678901234567/{token[:19]} "
                                   f"discord.com/api/webhooks/412345678901234567/{token * 2}") == []
    # ID too short, another API path, another host, inside a longer host
    assert rre.discord_webhook_url(f"discord.com/api/webhooks/4123456789012345/{token} "
                                   f"discord.com/api/channels/412345678901234567/{token} "
                                   f"example.com/api/webhooks/412345678901234567/{token} "
                                   f"notdiscord.com/api/webhooks/412345678901234567/{token}") == []


def test_messaging_url_shortener_link():
    # made up codes
    links = ["bit.ly/3AbCdEf", "https://t.co/AbC1dEf2Gh", "http://tinyurl.com/2p8abc3d", "is.gd/xYz123",
             "ow.ly/AbCd50PqRsT", "goo.gl/AbCdE", "https://cutt.ly/aBcD1eF", "rebrand.ly/my-link_2",
             "shorturl.at/abcD1", "rb.gy/abc12", "BIT.LY/ABC12", "https://www.tinyurl.com/my-alias"]
    assert rre.url_shortener_link(" ".join(links)) == links
    assert rre.url_shortener_link(f"click ({links[0]}), '{links[1]}', \"{links[3]}\". Or {links[4]}?utm_source=x") == [
        links[0], links[1], links[3], links[4]]
    assert rre.url_shortener_link("t.ly/Ab3, v.gd/Xy9z, x.gd/abc, lnkd.in/dAbC-12, buff.ly/3xYz") == [
        "t.ly/Ab3", "v.gd/Xy9z", "x.gd/abc", "lnkd.in/dAbC-12", "buff.ly/3xYz"]
    # a maps link, code too short or too long, no code
    assert rre.url_shortener_link("goo.gl/maps/AbCdEf maps.app.goo.gl/AbCdEf bit.ly/ab bit.ly/ bit.ly/" + "a" * 65) == []
    # look-alike or longer hosts, an email address
    assert rre.url_shortener_link("t.com/abc at.co/abc about.co/abc this.gd/abc bit.lyx/abc sub.bit.ly/abc "
                                  "jane@bit.ly/abc") == []


def test_messaging_mastodon_handle():
    assert rre.mastodon_handle("follow @jane@mastodon.example and @jane_doe@social.example.org.") == [
        "@jane@mastodon.example", "@jane_doe@social.example.org"]
    assert rre.mastodon_handle("(@j.doe@fosstodon.example), '@Jane@Example.Social', \"@jane-doe@pixel.example.net\"") == [
        "@j.doe@fosstodon.example", "@Jane@Example.Social", "@jane-doe@pixel.example.net"]
    assert rre.mastodon_handle("@jane@mastodon.example: see https://mastodon.example/@jane, cc:@a_b@m.example.de") == [
        "@jane@mastodon.example", "@a_b@m.example.de"]
    # an email address, a mail provider, inside a longer token, no domain, a Matrix ID, a package
    assert rre.mastodon_handle("jane@mastodon.example @jane@gmail.com @piet@outlook.com @x@yahoo.co.uk") == []
    assert rre.mastodon_handle("x@jane@mastodon.example @jane@localhost @jane:matrix.example @types/node@20.1.0") == []
    assert rre.mastodon_handle("@jane@@mastodon.example @jane@mastodon.example.c0m @@jane@mastodon.example") == []


def test_messaging_bluesky_handle():
    did = "did:plc:ab2cd3ef4gh5ij6kl7mn2op3"  # made up
    assert rre.bluesky_handle("@jane.bsky.social follows jane-doe.bsky.social") == [
        "@jane.bsky.social", "jane-doe.bsky.social"]
    assert rre.bluesky_handle(f"https://bsky.app/profile/jane.example.com (bsky.app/profile/{did}) "
                              "https://bsky.app/profile/Jane.bsky.social/post/3kabc2def3ghi") == [
        "https://bsky.app/profile/jane.example.com", f"bsky.app/profile/{did}",
        "https://bsky.app/profile/Jane.bsky.social"]
    assert rre.bluesky_handle("HTTPS://BSKY.APP/profile/JANE.EXAMPLE.COM") == ["HTTPS://BSKY.APP/profile/JANE.EXAMPLE.COM"]
    assert rre.bluesky_handle(f"Bluesky: @jane.example.com, bsky handle jane.example.org; Bluesky account: {did}.") == [
        "Bluesky: @jane.example.com", "bsky handle jane.example.org", f"Bluesky account: {did}"]
    assert rre.bluesky_handle("'@jane.bsky.social'\n\"BLUESKY ID=did:web:jane.example.com\"") == [
        "@jane.bsky.social", "BLUESKY ID=did:web:jane.example.com"]
    # a custom domain without keyword, the bare service, an email address, a longer domain, a short DID
    assert rre.bluesky_handle("jane.example.com @jane.example.com bsky.social jane@jane.bsky.social "
                              "jane.bsky.social.example.com bsky.app/profile/did:plc:ab2cd3") == []
    # no handle after the keyword, another page, inside a longer host or word
    assert rre.bluesky_handle("Bluesky is great, on Bluesky and Mastodon, bsky.app/search?q=jane.example.com "
                              "notbsky.app/profile/jane.example.com xbluesky: jane.example.com") == []


def test_messaging_reddit_user():
    assert rre.reddit_user("/u/Jane-Doe: thanks u/jane_doe") == ["/u/Jane-Doe", "u/jane_doe"]
    assert rre.reddit_user("HTTPS://WWW.REDDIT.COM/U/JANE_DOE!") == ["HTTPS://WWW.REDDIT.COM/U/JANE_DOE"]
    assert rre.reddit_user("https://www.reddit.com/user/jane_doe/ old.reddit.com/u/jane123 (REDDIT.COM/user/x_y_z)"
                           ) == ["https://www.reddit.com/user/jane_doe", "old.reddit.com/u/jane123", "REDDIT.COM/user/x_y_z"]
    assert rre.reddit_user("u/abc, 'u/abcdefghij0123456789'.") == ["u/abc", "u/abcdefghij0123456789"]
    # too short or too long, other sites' /u/ paths
    assert rre.reddit_user("u/ab u/abcdefghij01234567890 example.com/u/jane_doe lemmy.example/u/jane /home/u/files") == []
    # a subreddit, a word ending in u, units, a link without a user
    assert rre.reddit_user("r/jane_doe reddit.com/r/test you/jane 10 u/day, 1 u/min, reddit.com/user/ab") == []


def test_messaging_regexes_stay_fast():
    names = ("tox_id", "simplex_link", "discord_user_id", "discord_webhook_url", "url_shortener_link",
             "mastodon_handle", "bluesky_handle", "reddit_user")
    start = time.perf_counter()
    for unit in ("A", "a1", "0", "@a", "a@", "a.", "a-", "a/", "u/", "<@1", "1 ", "discord id ", "bsky ",
                 "a.bsky.social", "simplex:/a#", "https://a", "bit.ly/", "@a@a.", "reddit.com/user/"):
        text = unit * (100000 // len(unit))
        for name in names:
            getattr(rre, name)(text)
    assert time.perf_counter() - start < 1


def test_secrets_bitlocker_recovery_key():
    # made up: every block is a 16-bit number times 11
    key = "123453-440000-720885-013574-333333-000055-244442-659989"
    assert rre.bitlocker_recovery_key(f"BitLocker recovery key: {key}.") == [key]
    assert rre.bitlocker_recovery_key(f'({key}) "RecoveryPassword": "{key}"') == [key, key]
    assert rre.bitlocker_recovery_key(f"{key}\n{key.replace('-', ' ')}") == [key, key.replace('-', ' ')]
    assert rre.bitlocker_recovery_key(f"manage-bde: Password:\n    {key}\n") == [key]
    # a block not divisible by 11 (123456), one of 65536 * 11, last digit wrong, 7 or 9 blocks, separators mixed or
    # left out, glued to a digit or letter, a placeholder of eight equal blocks
    assert rre.bitlocker_recovery_key(key.replace('-', '')) == []
    assert rre.bitlocker_recovery_key("-".join(["000000"] * 8) + " " + "-".join(["111111"] * 8)) == []
    assert rre.bitlocker_recovery_key("123456" + key[6:]) == []
    assert rre.bitlocker_recovery_key(key.replace("720885", "720896")) == []
    assert rre.bitlocker_recovery_key(key[:-1] + "8") == []
    assert rre.bitlocker_recovery_key(f"{key[:-7]}, {key}-123453") == []
    assert rre.bitlocker_recovery_key(key.replace('-', ' ', 1)) == []
    assert rre.bitlocker_recovery_key(f"1{key} x{key} {key}x") == []
    # look-alikes: a UUID, an IBAN, a 48-digit number
    assert rre.bitlocker_recovery_key("123e4567-e89b-12d3-a456-426614174000 BE68 5390 0754 7034 " + "1" * 48) == []


def test_secrets_filevault_recovery_key():
    # made up
    key = "AB12-CD34-EF56-GH78-JK9L-MN0P"
    assert rre.filevault_recovery_key(f"FileVault recovery key: {key}.") == [f"FileVault recovery key: {key}"]
    assert rre.filevault_recovery_key(f"Recovery Key\n{key}") == [f"Recovery Key\n{key}"]
    assert rre.filevault_recovery_key(f"(filevault: {key}) personal recovery key={key}") == [
        f"filevault: {key}", f"personal recovery key={key}"]
    assert rre.filevault_recovery_key(f'{{"recoveryKey":"{key}"}}') == [f'recoveryKey":"{key}']
    assert rre.filevault_recovery_key(f"herstelsleutel: {key}, Wiederherstellungsschlüssel {key}") == [
        f"herstelsleutel: {key}", f"Wiederherstellungsschlüssel {key}"]
    assert rre.filevault_recovery_key(f"clé de secours : {key}; clave de recuperación: {key}") == [
        f"clé de secours : {key}", f"clave de recuperación: {key}"]
    # no keyword, 7 or 5 groups, lowercase, a group of 5, a keyword too far away
    assert rre.filevault_recovery_key(key) == []
    assert rre.filevault_recovery_key(f"recovery key: {key}-QR12, recovery key: {key[:-5]}") == []
    assert rre.filevault_recovery_key(f"recovery key: {key.lower()}") == []
    assert rre.filevault_recovery_key(f"FileVault {key}Q, FileVault A{key}") == []
    assert rre.filevault_recovery_key(f"the recovery key is written below: {key}") == []
    # look-alikes: a BitLocker key, a UUID, a Windows product key
    assert rre.filevault_recovery_key("recovery key: 123453-440000-720885-013574-333333-000055-244442-659989, "
                                      "recovery key: 123e4567-e89b-12d3-a456-426614174000, "
                                      "recovery key: W269N-WFGWX-YVC9B-4J6C9-T83GX") == []


def test_secrets_windows_product_key():
    # Microsoft's published generic KMS client keys (GVLK); the last one is made up, in the pre-Windows 8 alphabet
    assert rre.windows_product_key("Product key: W269N-WFGWX-YVC9B-4J6C9-T83GX.") == ["W269N-WFGWX-YVC9B-4J6C9-T83GX"]
    assert rre.windows_product_key("(NPPR9-FWDCX-D2C8J-H872K-2YT43)") == ["NPPR9-FWDCX-D2C8J-H872K-2YT43"]
    assert rre.windows_product_key("slmgr /ipk TX9XD-98N7V-6WMQ6-BX7FG-H8Q99") == ["TX9XD-98N7V-6WMQ6-BX7FG-H8Q99"]
    assert rre.windows_product_key('{"key":"M7XTQ-FN8P6-TTKYV-9D4CC-J462D"}') == ["M7XTQ-FN8P6-TTKYV-9D4CC-J462D"]
    assert rre.windows_product_key("BBBBB-CCCCC-DDDDD-FFFFF-2GGGG\n") == ["BBBBB-CCCCC-DDDDD-FFFFF-2GGGG"]
    assert rre.windows_product_key("key=W269N-WFGWX-YVC9B-4J6C9-T83GX;") == ["W269N-WFGWX-YVC9B-4J6C9-T83GX"]
    # one character short or too many, a sixth group, two Ns, lowercase, vowels, 5, all digits or all letters
    assert rre.windows_product_key("W269N-WFGWX-YVC9B-4J6C9-T83G W269N-WFGWX-YVC9B-4J6C9-T83GXX") == []
    assert rre.windows_product_key("W269N-WFGWX-YVC9B-4J6C9-T83GX-BBBBB") == []
    assert rre.windows_product_key("W269N-NFGWX-YVC9B-4J6C9-T83GX w269n-wfgwx-yvc9b-4j6c9-t83gx") == []
    assert rre.windows_product_key("ABCDE-FGHIJ-KLMNO-PQRST-UVWXY W2695-WFGWX-YVC9B-4J6C9-T83GX") == []
    assert rre.windows_product_key("22222-33333-44444-66666-77777 BBBBB-CCCCC-DDDDD-FFFFF-GGGGG") == []
    # look-alikes: a UUID, a phone number, a FileVault key
    assert rre.windows_product_key("123e4567-e89b-12d3-a456-426614174000 +32 470 12 34 56 AB12-CD34-EF56-GH78") == []


def test_secrets_ssh_fingerprint():
    # made up: the SHA-256 and MD5 of "example host key"
    sha, md5 = "SHA256:ht+qb8ckV14AvQbgJldN09NwZ23vdwTiRnXHtaFRcEY", "93:28:d9:7f:3f:de:a4:5d:b6:09:63:33:4f:2a:9a:99"
    assert rre.ssh_fingerprint(f"256 {sha} jane@laptop (ED25519)") == [sha]
    assert rre.ssh_fingerprint(f"ED25519 key fingerprint is {sha}.") == [sha]
    assert rre.ssh_fingerprint(f"({sha}) {sha}") == [sha, sha]
    assert rre.ssh_fingerprint(f"2048 MD5:{md5} jane@host (RSA)") == [f"MD5:{md5}"]
    assert rre.ssh_fingerprint(f"ssh-rsa 2048 {md5}\n") == [md5]
    assert rre.ssh_fingerprint(f"[{md5}]") == [md5]
    # one character short or long, a last character that cannot end 32 bytes, lowercase sha256:, a hex digest
    assert rre.ssh_fingerprint(f"{sha[:-1]} {sha}A {sha[:-1]}B") == []
    hexdigest = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
    assert rre.ssh_fingerprint(f"sha256:{sha[7:]} SHA256:{hexdigest} sha256:{hexdigest}") == []
    # 15 or 17 pairs, uppercase, part of a longer colon list
    assert rre.ssh_fingerprint(f"{md5[:-3]} {md5}:ab {md5.upper()} 00:{md5}") == []
    # 16 pairs of decimal digits (a fingerprint has a letter); look-alikes: a MAC address, an IPv6 address, an MD5
    # hash, a UUID
    assert rre.ssh_fingerprint("12:34:56:78:90:12:34:56:78:90:12:34:56:78:90:12") == []
    assert rre.ssh_fingerprint("00:1a:2b:3c:4d:5e fe80::1ff:fe23:4567:890a 9328d97f3fdea45db60963334f2a9a99 "
                               "123e4567-e89b-12d3-a456-426614174000") == []


def test_secrets_pgp_fingerprint():
    # made up: the SHA-1 of "example pgp key"
    fpr = "65A186BAD7DBB80E459DFC9445ECFFB159B34578"
    grouped = "65A1 86BA D7DB B80E 459D FC94 45EC FFB1 59B3 4578"
    gpg = "65A1 86BA D7DB B80E 459D  FC94 45EC FFB1 59B3 4578"
    assert rre.pgp_fingerprint(f"PGP fingerprint: {grouped}") == [f"PGP fingerprint: {grouped}"]
    assert rre.pgp_fingerprint(f"      Key fingerprint = {gpg}\n") == [f"Key fingerprint = {gpg}"]
    assert rre.pgp_fingerprint(f"Primary key fingerprint: {gpg}") == [f"Primary key fingerprint: {gpg}"]
    assert rre.pgp_fingerprint(f"OPENPGP4FPR:{fpr} openpgp4fpr:{fpr.lower()}") == [
        f"OPENPGP4FPR:{fpr}", f"openpgp4fpr:{fpr.lower()}"]
    assert rre.pgp_fingerprint(f"GPG key: 0x{fpr}, OpenPGP: {fpr}.") == [f"GPG key: 0x{fpr}", f"OpenPGP: {fpr}"]
    assert rre.pgp_fingerprint(f"(pgp {fpr}) GnuPG-Fingerprint={fpr}") == [f"pgp {fpr}", f"GnuPG-Fingerprint={fpr}"]
    # no keyword, or one that is not PGP's: a SHA-1 hash, a certificate fingerprint, a commit
    assert rre.pgp_fingerprint(f"{fpr} fingerprint: {fpr} SHA1 Fingerprint={fpr} commit {fpr.lower()}") == []
    # one hex digit short or long, a long key ID (16), nine groups, groups of another size
    assert rre.pgp_fingerprint(f"PGP: {fpr[:-1]}, PGP: {fpr}0, PGP key ID: 0x{fpr[-16:]}") == []
    assert rre.pgp_fingerprint(f"PGP fingerprint: {grouped[:-5]}, PGP {fpr[:20]}-{fpr[20:]}") == []
    assert rre.pgp_fingerprint(f"PGP {' '.join(fpr[i:i + 8] for i in range(0, 40, 8))}") == []
    # glued to letters, a keyword inside a longer word
    assert rre.pgp_fingerprint(f"PGP: {fpr}G mypgp {fpr}") == []
    # look-alikes: a SHA-256, a UUID, an Ethereum address
    assert rre.pgp_fingerprint("PGP 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08, "
                               "PGP 123e4567-e89b-12d3-a456-426614174000, PGP 0x" + "a" * 40 + "b") == []


def test_secrets_aws_secret_access_key():
    # AWS's documentation example keys
    secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    assert rre.aws_secret_access_key(f"[default]\naws_secret_access_key = {secret}\n") == [
        f"aws_secret_access_key = {secret}"]
    assert rre.aws_secret_access_key(f"export MY_AWS_SECRET_ACCESS_KEY={secret}") == [f"AWS_SECRET_ACCESS_KEY={secret}"]
    assert rre.aws_secret_access_key(f'{{"SecretAccessKey": "{secret}",') == [f'SecretAccessKey": "{secret}']
    assert rre.aws_secret_access_key(f"secretAccessKey: '{secret}'") == [f"secretAccessKey: '{secret}"]
    assert rre.aws_secret_access_key(f"<SecretAccessKey>{secret}</SecretAccessKey>") == [f"SecretAccessKey>{secret}"]
    assert rre.aws_secret_access_key(f"AWS Secret Key: {secret}. aws.secret.access.key={secret}") == [
        f"AWS Secret Key: {secret}", f"aws.secret.access.key={secret}"]
    # after its access key ID, as in the credentials CSV
    assert rre.aws_secret_access_key(f"jane,,AKIAIOSFODNN7EXAMPLE,{secret},https://") == [
        f"AKIAIOSFODNN7EXAMPLE,{secret}"]
    # no keyword, one character short or long, another keyword, a broken access key ID
    assert rre.aws_secret_access_key(secret) == []
    assert rre.aws_secret_access_key(f"aws_secret_access_key = {secret[:-1]}") == []
    assert rre.aws_secret_access_key(f"aws_secret_access_key = {secret}A") == []
    assert rre.aws_secret_access_key(f"secret_key = {secret}, aws_access_key_id = {secret}") == []
    assert rre.aws_secret_access_key(f"AKIAIOSFODNN7EXAMPL,{secret} xAKIAIOSFODNN7EXAMPLE,{secret}") == []
    # look-alikes: a SHA-256, a SHA-1 (40 hex, but followed by more), base64 with padding
    assert rre.aws_secret_access_key("aws_secret_access_key = 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 "
                                     f"aws_secret_access_key={secret[:38]}==") == []


def test_secrets_slack_webhook_url():
    # Slack's documentation placeholder, and made up; split so GitHub's push protection doesn't take them for real
    placeholder = "https://hooks.slack.com/services/" "T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
    assert rre.slack_webhook_url(placeholder) == [placeholder]
    hook = "hooks.slack.com/services/T0A1B2C3D/B0E1F2G3H/abcdEFGHijklMNOPqrstUVWX"
    assert rre.slack_webhook_url(f"url = 'https://{hook}'") == [f"https://{hook}"]
    assert rre.slack_webhook_url(f"({hook}).") == [hook]
    assert rre.slack_webhook_url(f"http://{hook.replace('slack', 'slack-gov')}") == [
        f"http://{hook.replace('slack', 'slack-gov')}"]
    workflow = "https://hooks.slack.com/workflows/" "T0A1B2C3D/A0E1F2G3H/123456789012345678/abcdEFGHijklMNOPqrstUVWX"
    assert rre.slack_webhook_url(workflow) == [workflow]
    assert rre.slack_webhook_url(
        "curl -X POST https://hooks.slack.com/triggers/T0A1B2C3D/1234567890123/0123456789abcdef0123456789abcdef.") == [
        "https://hooks.slack.com/triggers/T0A1B2C3D/1234567890123/0123456789abcdef0123456789abcdef"]
    # no path, a short team ID, another host, lowercase team ID, another path, one part only
    assert rre.slack_webhook_url("https://hooks.slack.com/services/ https://hooks.slack.com/services/T0A1/B0E1F2G3H/x") == []
    assert rre.slack_webhook_url(f"https://my{hook} https://{hook.replace('T0A1B2C3D', 't0a1b2c3d')}") == []
    assert rre.slack_webhook_url(f"https://{hook.replace('services', 'apps')} https://slack.com/services/T0A1B2C3D/B0/x") == []
    assert rre.slack_webhook_url("https://hooks.slack.com/services/T0A1B2C3D/B0E1F2G3H") == []
    # look-alikes: a Slack token, a message link
    assert rre.slack_webhook_url("xoxb-1234567890-abcdefghij https://example.slack.com/archives/C0A1B2C3D/p1234567890") == []
    assert rre.slack_webhook_url(f"https://{hook}-x") == []


def test_secrets_discord_webhook_url():
    # made up
    token = "QvYhW_R6Vc9UgTkr2gC2ByPd4JHhqfbfe5k6zyEeQtSgC4vz2lMWFFlC0pVr8d644C8r"
    hook = f"discord.com/api/webhooks/123456789012345678/{token}"
    assert rre.discord_webhook_url(f"https://{hook}") == [f"https://{hook}"]
    assert rre.discord_webhook_url(f"post to https://discordapp.com/api/webhooks/123456789012345678/{token}.") == [
        f"https://discordapp.com/api/webhooks/123456789012345678/{token}"]
    assert rre.discord_webhook_url(f"'https://canary.discord.com/api/v10/webhooks/1234567890123456789/{token}'") == [
        f"https://canary.discord.com/api/v10/webhooks/1234567890123456789/{token}"]
    assert rre.discord_webhook_url(f"({hook})") == [hook]
    assert rre.discord_webhook_url(f"WEBHOOK=https://ptb.{hook}?wait=true") == [f"https://ptb.{hook}"]
    assert rre.discord_webhook_url(f'{{"url": "HTTP://{hook}"}}') == [f'HTTP://{hook}']
    # an ID too short, a token too short, no token, another host, another path, an invite
    assert rre.discord_webhook_url(f"https://discord.com/api/webhooks/1234567890/{token}") == []
    assert rre.discord_webhook_url(f"https://{hook[:-30]} https://discord.com/api/webhooks/123456789012345678") == []
    assert rre.discord_webhook_url(f"https://evil-{hook} https://{hook.replace('webhooks', 'channels')}") == []
    assert rre.discord_webhook_url(f"https://{hook}0123456789abcdef") == []
    # look-alikes: an invite, a message link, a Telegram bot URL
    assert rre.discord_webhook_url("https://discord.gg/abcdef https://discord.com/channels/123456789012345678/"
                                   "123456789012345678/123456789012345678") == []
    assert rre.discord_webhook_url("https://api.telegram.org/bot123456789:AA" + "b" * 33 + "/getMe") == []


def test_secrets_azure_connection_string():
    # made up keys
    key = "wVI9xin6pF3K1h1D7tXEvKdAgSiQofgQdzu12ESthnKM2liZLzuhIT/nDH6ih6yLAN060WrLLOsAFii0NptILw=="
    storage = f"DefaultEndpointsProtocol=https;AccountName=examplestore;AccountKey={key};EndpointSuffix=core.windows.net"
    assert rre.azure_connection_string(storage) == [storage]
    assert rre.azure_connection_string(f'"AzureWebJobsStorage": "{storage}",') == [storage]
    assert rre.azure_connection_string(f"AZURE_STORAGE_CONNECTION_STRING=AccountName=examplestore;AccountKey={key};") == [
        f"AccountName=examplestore;AccountKey={key};"]
    bus = ("Endpoint=sb://example-ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;"
           "SharedAccessKey=LzN4eOLWv87ArH5SvAMc6Q2djpICie1wZiWpf9/lczM=")
    assert rre.azure_connection_string(f"<add value='{bus}' />") == [bus]
    iot = ("HostName=example-hub.azure-devices.net;DeviceId=dev1;"
           "SharedAccessKey=LzN4eOLWv87ArH5SvAMc6Q2djpICie1wZiWpf9/lczM=")
    assert rre.azure_connection_string(f"{iot}\n") == [iot]
    sas = ("BlobEndpoint=https://examplestore.blob.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=b&srt=co"
           "&sp=rl&se=2030-01-01T00:00:00Z&spr=https&sig=abcdEFGH1234%2Bxyz%3D")
    assert rre.azure_connection_string(sas) == [sas]
    token = "SharedAccessSignature sr=example-ns.servicebus.windows.net&sig=abcdEFGH1234%2Bxyz%3D&se=1893456000&skn=send"
    assert rre.azure_connection_string(f"Authorization: {token}") == [token]
    # a placeholder, no key, a key too short, lowercase names, a SAS without its signature
    assert rre.azure_connection_string(storage.replace(key, "<your-key>")) == []
    assert rre.azure_connection_string("UseDevelopmentStorage=true; AccountKey=YOUR_ACCOUNT_KEY") == []
    assert rre.azure_connection_string("DefaultEndpointsProtocol=https;AccountName=examplestore;"
                                       "EndpointSuffix=core.windows.net") == []
    assert rre.azure_connection_string(f"AccountKey={key[:19]} accountkey={key}") == []
    assert rre.azure_connection_string("SharedAccessSignature=sv=2022-11-02&ss=b&sig=short") == []
    # look-alikes: a SQL Server connection string with a password, base64 after another name, a JWT
    assert rre.azure_connection_string("Server=tcp:x.database.windows.net,1433;Initial Catalog=db;"
                                       f"Password=hunter2hunter2hunter2; ApiKey={key} AccountKeyX={key}") == []


def test_secrets_database_connection_uri():
    # made up
    assert rre.database_connection_uri("postgres://jane:s3cret@db.example.com:5432/app") == [
        "postgres://jane:s3cret@db.example.com:5432/app"]
    assert rre.database_connection_uri("DATABASE_URL=postgresql+psycopg2://jane:s3cret@localhost/app.") == [
        "postgresql+psycopg2://jane:s3cret@localhost/app"]
    assert rre.database_connection_uri("mongodb+srv://jane:p%40ss@cluster0.example.net/test?retryWrites=true&w=majority") == [
        "mongodb+srv://jane:p%40ss@cluster0.example.net/test?retryWrites=true&w=majority"]
    assert rre.database_connection_uri("MONGO=mongodb://jane:s3cret@h1.example.com:27017,h2.example.com:27017/db") == [
        "mongodb://jane:s3cret@h1.example.com:27017,h2.example.com:27017/db"]
    assert rre.database_connection_uri("(redis://:s3cret@cache.example.com:6379/0) rediss://default:s3cret@cache:6380") == [
        "redis://:s3cret@cache.example.com:6379/0", "rediss://default:s3cret@cache:6380"]
    # a password with an @, an IPv6 host after jdbc:
    assert rre.database_connection_uri("'mysql://root:p@ss@127.0.0.1:3306/shop' jdbc:mysql://jane:s3cret@[::1]:3306/db") == [
        "mysql://root:p@ss@127.0.0.1:3306/shop", "mysql://jane:s3cret@[::1]:3306/db"]
    # no password, no user and password, masked, empty, no host, a longer scheme, one slash, a web address
    assert rre.database_connection_uri("postgres://jane@db.example.com/app postgres://db.example.com:5432/app") == []
    assert rre.database_connection_uri("postgres://jane:***@db.example.com/app mysql://jane:@db.example.com") == []
    assert rre.database_connection_uri("postgresql://jane:s3cret xpostgres://jane:s3cret@host") == []
    assert rre.database_connection_uri("postgres:/jane:s3cret@host https://jane:s3cret@example.com") == []
    assert rre.database_connection_uri("mysql://jane:s3cret/@host mysql://jane/s3cret:x@host") == []
    # look-alikes: an e-mail address, a JDBC URL with the password as a parameter
    assert rre.database_connection_uri("jane:s3cret@example.com jdbc:postgresql://db:5432/app?user=jane&password=s3cret") == []


def test_secrets_basic_auth_url():
    # made up
    assert rre.basic_auth_url("https://jane:s3cret@example.com/path") == ["https://jane:s3cret@example.com/path"]
    assert rre.basic_auth_url("ftp://anonymous:guest@ftp.example.org.") == ["ftp://anonymous:guest@ftp.example.org"]
    assert rre.basic_auth_url("(http://admin:admin@192.168.1.1:8080/)") == ["http://admin:admin@192.168.1.1:8080/"]
    assert rre.basic_auth_url("git remote add origin https://jane:ghp_token123@git.example.com/repo.git") == [
        "https://jane:ghp_token123@git.example.com/repo.git"]
    assert rre.basic_auth_url('proxy = "socks5://user:pa:ss@proxy.example.com:1080"') == [
        "socks5://user:pa:ss@proxy.example.com:1080"]
    assert rre.basic_auth_url("rtsp://admin:12345@10.0.0.5:554/stream1 https://:token@example.com SMB://jane:s3cret@nas/x") == [
        "rtsp://admin:12345@10.0.0.5:554/stream1", "https://:token@example.com", "SMB://jane:s3cret@nas/x"]
    # no password, a port, a profile path, masked, a database URI, no scheme, a user only
    assert rre.basic_auth_url("https://jane@example.com https://example.com:8080/path ssh://git@example.com:22/r") == []
    assert rre.basic_auth_url("https://www.tiktok.com/@jane https://example.com:443/@jane http://localhost:3000/@u/x@y") == []
    assert rre.basic_auth_url("https://jane:****@example.com postgres://jane:s3cret@db.example.com/app") == []
    assert rre.basic_auth_url("user:pass@example.com mailto:jane@example.com") == []
    assert rre.basic_auth_url("https://jane:s3cret@ https://jane:s3cret@/path") == []
    # look-alikes: an e-mail address, an XMPP address, a magnet link
    assert rre.basic_auth_url("jane@example.com xmpp:jane@example.com magnet:?xt=urn:btih:" + "a" * 40) == []


def test_secrets_stay_fast():
    # runs of each regex's own keywords and separators, and of digits, hex, base64 and dashes (100 KB each)
    start = time.perf_counter()
    for text in ('123453-' * 15000, '123453 ' * 15000, '1' * 100000, 'recovery key: ' * 7500, 'AB12-' * 20000,
                 'BBBBB-' * 17000, 'N' * 100000, 'SHA256:' * 15000, 'ab:' * 34000, 'PGP fingerprint: ' * 6000,
                 '65A1 ' * 20000, 'aws_secret_access_key=' * 4600, 'AKIAIOSFODNN7EXAMPLE,' * 4800, 'a/' * 50000,
                 'hooks.slack.com/services/T0A1B2C3D/' * 2900, 'discord.com/api/webhooks/' * 4000, 'Ab=' * 33000,
                 'AccountKey=' * 9000, 'SharedAccessSignature=a&' * 4000, 'postgres://' * 9000, 'a:b@' * 25000,
                 'http://a:' * 11000, 'deadbeef' * 12500, 'aB3/' * 25000, '-' * 100000):
        for name in ('bitlocker_recovery_key', 'filevault_recovery_key', 'windows_product_key', 'ssh_fingerprint',
                     'pgp_fingerprint', 'aws_secret_access_key', 'slack_webhook_url', 'discord_webhook_url',
                     'azure_connection_string', 'database_connection_uri', 'basic_auth_url'):
            getattr(rre, name)(text)
    assert time.perf_counter() - start < 2


def test_timenet_mac_absolute_time():
    # made up: 2026-03-03 09:12:44 UTC is 794221964 seconds after 2001-01-01
    assert rre.mac_absolute_time(
        "Mac Absolute Time: 794221964, CFAbsoluteTime 794221964.123456 sent, cocoa core data timestamp=794221964, "
        "(Apple Cocoa Core Data timestamp: 794221964), macOS absolute time 794221964123456789.") == [
        "Mac Absolute Time: 794221964", "CFAbsoluteTime 794221964.123456", "cocoa core data timestamp=794221964",
        "Apple Cocoa Core Data timestamp: 794221964", "macOS absolute time 794221964123456789"]
    # Core Data columns (Z..., in capitals), in JSON, sqlite's line mode and a log line
    assert rre.mac_absolute_time('{"ZDATE": 794221964.5, "ZTEXT": "hi"}') == ['"ZDATE": 794221964.5']
    assert rre.mac_absolute_time("ZCREATIONDATE = 794221964") == ["ZCREATIONDATE = 794221964"]
    assert rre.mac_absolute_time("ZSTARTDATE: '794221964.25'") == ["ZSTARTDATE: '794221964.25'"]
    assert rre.mac_absolute_time("row 7|ZTIMESTAMP=794221964|ZCREATIONDATE1=794221964.0") == [
        "ZTIMESTAMP=794221964", "ZCREATIONDATE1=794221964.0"]
    # no label; 8 and 11 digits; Unix time under a Core Data column and 2041; lowercase, mach time and no date column
    assert rre.mac_absolute_time("794221964, ZDATE: 79422196, ZDATE: 79422196412") == []
    assert rre.mac_absolute_time("ZDATE: 1772529164, Mac absolute time 1262304000") == []
    assert rre.mac_absolute_time("zdate: 794221964, mach absolute time 794221964, ZONE: 794221964") == []
    # a version, too many decimals, plain numbers
    assert rre.mac_absolute_time("ZDATE: 794221964.1.2, ZDATE: 794221964.1234567890") == []
    assert rre.mac_absolute_time("order 794221964, version 794221964.1, unix time 1772529164") == []


def test_timenet_webkit_timestamp():
    # made up: 2026-03-03 09:12:44 UTC in microseconds since 1601
    assert rre.webkit_timestamp('{"last_visit_time": 13417002764123456}') == ['"last_visit_time": 13417002764123456']
    assert rre.webkit_timestamp("WebKit timestamp: 13417002764123456, Chrome time 13417002764123456") == [
        "WebKit timestamp: 13417002764123456", "Chrome time 13417002764123456"]
    assert rre.webkit_timestamp('"date_added": "13417002764123456",') == ['"date_added": "13417002764123456"']
    assert rre.webkit_timestamp("cookie expires_utc=13417002764123456; (visit_time=13417002764000000)") == [
        "expires_utc=13417002764123456", "visit_time=13417002764000000"]
    assert rre.webkit_timestamp("CREATION_UTC:13417002764123456") == ["CREATION_UTC:13417002764123456"]
    # no label; 16 and 18 digits; 1970 and 2041; a key that is no time, no time word
    assert rre.webkit_timestamp("13417002764123456") == []
    assert rre.webkit_timestamp('"last_visit_time": 1341700276412345, "last_visit_time": 134170027641234567') == []
    assert rre.webkit_timestamp("visit_time: 11644473600000000, visit_time: 13900000000000000") == []
    assert rre.webkit_timestamp('"order_id": 13417002764123456, chrome 13417002764123456') == []
    # Unix time in seconds and milliseconds, 20 digits
    assert rre.webkit_timestamp("time: 1772529164, date: 1772529164000, visit_time: 13417002764123456789") == []


def test_timenet_windows_filetime():
    # made up: 2026-03-03 09:12:44 UTC in 100 ns since 1601, decimal and hexadecimal
    assert rre.windows_filetime("FILETIME: 134170027640000000, Windows file time 0x01DCAAEDE4FC8E00") == [
        "FILETIME: 134170027640000000", "Windows file time 0x01DCAAEDE4FC8E00"]
    # Active Directory's LDAP timestamps
    assert rre.windows_filetime("lastLogonTimestamp: 134170027640000000, pwdLastSet=134170027640000000,") == [
        "lastLogonTimestamp: 134170027640000000", "pwdLastSet=134170027640000000"]
    assert rre.windows_filetime("accountExpires: 134170027640000000 (LDAP timestamp 134170027640000000)") == [
        "accountExpires: 134170027640000000", "LDAP timestamp 134170027640000000"]
    assert rre.windows_filetime('{"LastWriteTime": "134170027640000000"}') == ['"LastWriteTime": "134170027640000000"']
    assert rre.windows_filetime("ntfs time: 0x01dcaaede4fc8e00.") == ["ntfs time: 0x01dcaaede4fc8e00"]
    # no label; never expires and never set; 17 and 19 digits; 1970 and 2041; 15 hex digits, error codes, no time key
    assert rre.windows_filetime("134170027640000000") == []
    assert rre.windows_filetime("accountExpires: 9223372036854775807, pwdLastSet: 0") == []
    assert rre.windows_filetime("FILETIME: 13417002764000000, FILETIME: 1341700276400000000") == []
    assert rre.windows_filetime("FILETIME: 116444736000000000, FILETIME: 0x01ED4C1C4FCD4000") == []
    assert rre.windows_filetime("FILETIME: 0x01DCAAEDE4FC8E0, Error 0x80070005 at 0x7ffe4a2b") == []
    assert rre.windows_filetime("id: 134170027640000000, time: 1772529164") == []


def test_timenet_rfc2822_datetime():
    assert rre.rfc2822_datetime("Date: Tue, 3 Mar 2026 09:12:44 +0100") == ["Tue, 3 Mar 2026 09:12:44 +0100"]
    # two spaces before a one-digit day, a zone comment, no weekday, a Received header, no seconds, old zones
    assert rre.rfc2822_datetime("Tue,  3 Mar 2026 09:12:44 +0100 (CET)") == ["Tue,  3 Mar 2026 09:12:44 +0100"]
    assert rre.rfc2822_datetime("sent 03 Mar 2026 09:12:44 -0500.") == ["03 Mar 2026 09:12:44 -0500"]
    assert rre.rfc2822_datetime("by mx.example.com; Tue, 3 Mar 2026 08:12:44 GMT") == ["Tue, 3 Mar 2026 08:12:44 GMT"]
    assert rre.rfc2822_datetime('"Wed, 04 Mar 2026 23:59 +0530"') == ["Wed, 04 Mar 2026 23:59 +0530"]
    assert rre.rfc2822_datetime("Sun, 1 Feb 2026 00:00:00 PST, Date:Thu, 31 Dec 1998 23:59:59 UT") == [
        "Sun, 1 Feb 2026 00:00:00 PST", "Thu, 31 Dec 1998 23:59:59 UT"]
    # no time, no zone, a full month name, day 32, hour 24, ISO offset, offset +15, lowercase, ISO, a 5-digit year
    assert rre.rfc2822_datetime("Tue, 3 Mar 2026, 3 Mar 2026 09:12:44, Tue, 3 March 2026 09:12:44 +0100") == []
    assert rre.rfc2822_datetime("Tue, 32 Mar 2026 09:12:44 +0100, Tue, 3 Mar 2026 24:12:44 +0100") == []
    assert rre.rfc2822_datetime("Tue, 3 Mar 2026 09:12:44 +01:00, Tue, 3 Mar 2026 09:12:44 +1500") == []
    assert rre.rfc2822_datetime("tue, 3 mar 2026 09:12:44 +0100, Tue, 3 Mar 2026 09:12:44 +01001") == []
    assert rre.rfc2822_datetime("2026-03-03T09:12:44+01:00, 3 Mar 20261 09:12:44 +0100") == []


def test_timenet_cidr_range():
    assert rre.cidr_range("10.0.0.0/8") == ["10.0.0.0/8"]
    # an interface's address with its prefix, in config, in brackets, at the end of a sentence
    assert rre.cidr_range("inet 192.168.1.10/24 brd 192.168.1.255") == ["192.168.1.10/24"]
    assert rre.cidr_range("allow 198.51.100.0/24; deny all, default (0.0.0.0/0).") == ["198.51.100.0/24", "0.0.0.0/0"]
    # IPv6, also shortened to ::
    assert rre.cidr_range("prefix 2001:db8::/32 and ::/0") == ["2001:db8::/32", "::/0"]
    assert rre.cidr_range('"fe80::1ff:fe23:4567:890a/64"') == ["fe80::1ff:fe23:4567:890a/64"]
    assert rre.cidr_range("net=2001:DB8:0:0:8:800:200C:417A/128,") == ["2001:DB8:0:0:8:800:200C:417A/128"]
    # prefix too long, fractions and a date, a URL path, a longer path, an invalid IPv4, a dotted version
    assert rre.cidr_range("10.0.0.0/33, 2001:db8::/129, 1/2 cup, 3/4, 12.03.2024/25") == []
    assert rre.cidr_range("http://10.0.0.1/24 and 10.0.0.0/8/16") == []
    assert rre.cidr_range("256.0.0.0/8, 1.2.3.4.5/6, v1.2.3.4/5") == []
    # a time, an invalid IPv6, a leading zero, a decimal, addresses without a prefix
    assert rre.cidr_range("12:30:45/60, 2001:db8::1:/64, 10.0.0.0/08, 10.0.0.0/8.5") == []
    assert rre.cidr_range("192.168.1.10 and 2001:db8::1") == []


def test_timenet_asn():
    # documentation ASNs (RFC 5398), private ones and made up
    assert rre.asn("AS64496") == ["AS64496"]
    assert rre.asn("origin ASN 64497, peer ASN: 64512.") == ["ASN 64497", "ASN: 64512"]
    assert rre.asn('{"asn": 64500, "org": "x"}, "asn": "AS65536"') == ['"asn": 64500', '"asn": "AS65536"']
    assert rre.asn("autonomous_system_number=4200000000, (AS123)") == ["autonomous_system_number=4200000000", "AS123"]
    assert rre.asn("path AS4294967294,AS64496, ASN13335, ASN 1, asn=7") == [
        "AS4294967294", "AS64496", "ASN13335", "ASN 1", "asn=7"]
    # zero, reserved, 11 digits, lowercase and spaced AS, inside words, asdot, a leading zero
    assert rre.asn("AS0, AS4294967295, AS99999999999") == []
    assert rre.asn("as 2024, SUCH AS 2000 PEOPLE, as15169, AS 15169, ASN-13335") == []
    assert rre.asn("CLASS12, BASN 123, AS12345abc, AS1.2, ASN 012") == []
    # the AS/400 computer, EDI's AS2 and AS4, ASN.1
    assert rre.asn("an AS400, EDI over AS2 and AS4, AS12, ASN1 parse error, ASN.1 DER") == []
    assert rre.asn("asn: AS, 15169, A S15169") == []


def test_timenet_usb_vid_pid():
    # made up IDs: Windows device instance and interface paths, lsusb, dmesg, a serial port list, labels
    assert rre.usb_vid_pid(r"USB\VID_1234&PID_ABCD\5&1A2B3C4D&0&1") == ["VID_1234&PID_ABCD"]
    assert rre.usb_vid_pid(r"\\?\HID#vid_1234&pid_abcd&mi_00#7&1a2b") == ["vid_1234&pid_abcd"]
    assert rre.usb_vid_pid("Bus 001 Device 003: ID 1234:abcd Example Corp.") == ["ID 1234:abcd"]
    assert rre.usb_vid_pid("usb 1-1: New USB device found, idVendor=1234, idProduct=abcd, bcdDevice= 1.00") == [
        "idVendor=1234, idProduct=abcd"]
    assert rre.usb_vid_pid("USB VID:PID=1234:ABCD SER=0001 LOCATION=1-1") == ["VID:PID=1234:ABCD"]
    assert rre.usb_vid_pid("usb_id: 1234:abcd (VID/PID 1234:ABCD)") == ["usb_id: 1234:abcd", "VID/PID 1234:ABCD"]
    # no lsusb line before ID; 3, 5 hex digits; a process ID, a MAC-like run, a standard; no comma in dmesg's form
    assert rre.usb_vid_pid("ID 1234:5678, ticket 2024:0312") == []
    assert rre.usb_vid_pid("VID_123&PID_ABCD, VID_12345&PID_ABCD, VID_1234&PID_ABCDE") == []
    assert rre.usb_vid_pid("PID 4312, 12:34:56:78, ISO 9001:2015") == []
    assert rre.usb_vid_pid("Device 003: ID 1234:abcd5, Device 03: ID 1234:abcd") == []
    assert rre.usb_vid_pid("usb id 1234:abc, VID:PID 1234-abcd, idVendor=1234 idProduct=abcd") == []


def test_timenet_esim_eid():
    # GSMA SGP.29's example EID and two made up
    eid, eid2, eid3 = ("89049032123451234512345678901235", "89044000000000000000000012345617",
                       "89033023123456789012345678901212")
    assert rre.esim_eid(f"EID: {eid}, eid={eid2}") == [f"EID: {eid}", f"eid={eid2}"]
    assert rre.esim_eid(f'{{"eid": "{eid3}"}}') == [f'"eid": "{eid3}"']
    assert rre.esim_eid("eUICC ID 8904 9032 1234 5123 4512 3456 7890 1235") == [
        "eUICC ID 8904 9032 1234 5123 4512 3456 7890 1235"]
    assert rre.esim_eid(f"EUICC-ID: {eid}. (EID {eid}) EID#{eid2}") == [
        f"EUICC-ID: {eid}", f"EID {eid}", f"EID#{eid2}"]
    # no label, check digits wrong, 31 and 33 digits, not 89, an ICCID, other grouping, other words
    assert rre.esim_eid(f"{eid} EID: 89049032123451234512345678901236") == []
    assert rre.esim_eid(f"EID: {eid[:-1]}, EID: {eid}1") == []
    assert rre.esim_eid("EID: 98049032123451234512345678901235, EID: 8932011234567890100") == []
    assert rre.esim_eid("EID 89049 03212 34512 34512 34567 89012 35") == []
    assert rre.esim_eid(f"Eid holiday {eid}, PAID {eid}") == []


def test_timenet_user_agent():
    chrome = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
              "Safari/537.36")
    firefox = "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    iphone = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
              "Version/17.2 Mobile/15E148 Safari/604.1")
    android = ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile "
               "Safari/537.36")
    bot = "Mozilla/5.0 (compatible; ExampleBot/1.0; +https://bot.example.com/)"
    old = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"
    assert rre.user_agent(chrome) == [chrome]
    assert rre.user_agent(f"User-Agent: {firefox}\r\nAccept: */*") == [firefox]
    assert rre.user_agent(f"seen {iphone}. {android}") == [iphone, android]
    log = f'10.0.0.1 - - [03/Mar/2026:09:12:44 +0100] "GET / HTTP/1.1" 200 512 "-" "{old}" ({bot})'
    assert rre.user_agent(log) == [old, bot]
    # words after it are no product tokens
    assert rre.user_agent("Mozilla/5.0 (X11; Linux x86_64) was seen") == ["Mozilla/5.0 (X11; Linux x86_64)"]
    assert rre.user_agent("Mozilla/5.0 (X11; Linux x86_64) and/or Gecko/20100101") == [
        "Mozilla/5.0 (X11; Linux x86_64)"]
    # no platform, empty brackets, lowercase, version 6, other clients, no space, a longer word, broken brackets
    assert rre.user_agent("Mozilla/5.0, Mozilla Firefox 121, Mozilla/5.0 ()") == []
    assert rre.user_agent("mozilla/5.0 (x11), Mozilla/6.0 (X11; Linux x86_64)") == []
    assert rre.user_agent("curl/8.4.0, Dalvik/2.1.0 (Linux; U; Android 13), okhttp/4.9.0") == []
    assert rre.user_agent("Mozilla/5.0(X11), XMozilla/5.0 (X11)") == []
    assert rre.user_agent("Mozilla/5.0 (X11; Linux\nx86_64) Gecko/20100101, Mozilla/5.0 (a (b) c)") == []


def test_timenet_named_groups():
    # the raw patterns give the number of a labelled timestamp as a named group
    import json
    import re
    from pathlib import Path

    import regular_regexes
    patterns = json.loads((Path(regular_regexes.__file__).parent / 'intl' / 'regexes.json').read_text(encoding='utf-8'))
    for name, text, number in (('mac_absolute_time', '"ZDATE": 794221964.5', '794221964.5'),
                               ('webkit_timestamp', 'visit_time=13417002764123456', '13417002764123456'),
                               ('windows_filetime', 'FILETIME: 0x01DCAAEDE4FC8E00', '0x01DCAAEDE4FC8E00')):
        assert re.search(patterns[name]['regex'], text).group('timestamp') == number


def test_timenet_regexes_stay_fast():
    # 100 KB runs of digits, hex, dots, slashes, colons and of each regex's own labels
    start = time.perf_counter()
    labels = ('ZDATE: "last_visit_time": FILETIME 0x Tue, 3 Mar 2026 ASN AS1 VID_1234& Device 003: ID EID 8904 '
              'Mozilla/5.0 (')
    for text in ('1' * 100000, 'aB3f' * 25000, '1.' * 50000, '1/' * 50000, '1:' * 50000, '255.255.255.255/' * 6250,
                 '1:2:3:4:5:6:7:8/' * 6250, 'Z' + 'A' * 100000, labels * 1000,
                 'Mozilla/5.0 (a)' + ' a.b/1.1.1.1.1.1.1.1.1.1' * 4000):
        for fn in (rre.mac_absolute_time, rre.webkit_timestamp, rre.windows_filetime, rre.rfc2822_datetime,
                   rre.cidr_range, rre.asn, rre.usb_vid_pid, rre.esim_eid, rre.user_agent):
            fn(text)
    assert time.perf_counter() - start < 1


def test_travel_flight_number():
    # airline codes with made-up flight numbers
    assert rre.flight_number("Flight LH 1234 departs at 07:45, flight number: KL1702.") == [
        "Flight LH 1234", "flight number: KL1702"]
    assert rre.flight_number("(Flug LH400) Uw vlucht HV 5131 vertrekt; N° de vol : AF 1234") == [
        "Flug LH400", "vlucht HV 5131", "vol : AF 1234"]
    assert rre.flight_number("vuelo IB3456, volo AZ 610, zbor RO-301, Vlucht nr. KL 1702") == [
        "vuelo IB3456", "volo AZ 610", "zbor RO-301", "Vlucht nr. KL 1702"]
    # a digit in the airline code, an operational suffix, capitals, a label ending in nummer
    assert rre.flight_number('Flights: W6 4321 "Flight No. U2 8301A" FLIGHT: 3K 512, Flugnummer LH 2031') == [
        "Flights: W6 4321", "Flight No. U2 8301A", "FLIGHT: 3K 512", "Flugnummer LH 2031"]
    assert rre.flight_number("Subject: your flight FR 2468 is confirmed") == ["flight FR 2468"]
    assert rre.flight_number('{"flightNumber":"LH1234"} ?flight_no=KL1702&date=0') == [
        'flightNumber":"LH1234', "flight_no=KL1702"]
    # no label, as in a train or bus number
    assert rre.flight_number("LH 1234 departs, return KL 1702, train IC 2117, bus 71") == []
    # no airline code, a lowercase one, an airport code, five digits, two digits as the code, inside a word
    assert rre.flight_number("flight 1234, flight lh 1234, Flight LHR 1234, Flight LH 12345, Flight 12 3456") == []
    assert rre.flight_number("a flight of 12 stairs, flight time 2h 15m, inflight LH 1234, Vol. 12 No. 3") == []


def test_travel_airline_ticket_number():
    # made up
    assert rre.airline_ticket_number("Ticket number: 057-2123456789, E-ticket 0742123456789.") == [
        "Ticket number: 057-2123456789", "E-ticket 0742123456789"]
    assert rre.airline_ticket_number("(ETKT 125 2123456789) Ticketnummer: 074-2123456789") == [
        "ETKT 125 2123456789", "Ticketnummer: 074-2123456789"]
    assert rre.airline_ticket_number("numéro de billet : 0572123456789; Número de billete: 0752123456789") == [
        "billet : 0572123456789", "billete: 0752123456789"]
    assert rre.airline_ticket_number("eticket nr. 1252123456789 and TKT 057 2123456789") == [
        "eticket nr. 1252123456789", "TKT 057 2123456789"]
    assert rre.airline_ticket_number('{"ticketNumber": "0572123456789"}') == ['ticketNumber": "0572123456789']
    # no label, an air waybill, a support ticket
    assert rre.airline_ticket_number("0572123456789, AWB 020-12345675, Ticket 2024-117, ticket #12345") == []
    # twelve and fourteen digits, sixteen, grouped otherwise, no space after the label
    assert rre.airline_ticket_number("ticket number 057-212345678, ticket number 057-21234567890") == []
    assert rre.airline_ticket_number("Ticket: 1234567890123456, ticket: 057 2123 456 789, TKT0572123456789") == []


def test_travel_booking_reference():
    # made up
    assert rre.booking_reference("Booking reference: XK7P2Q, PNR ABC123.") == ["Booking reference: XK7P2Q", "PNR ABC123"]
    assert rre.booking_reference("Your booking code is K9Z2LM. Uw boekingscode: QWERTY") == [
        "booking code is K9Z2LM", "boekingscode: QWERTY"]
    assert rre.booking_reference("Ihr Buchungscode lautet ZX8Y7W (record locator: 7HJKLP)") == [
        "Buchungscode lautet ZX8Y7W", "record locator: 7HJKLP"]
    assert rre.booking_reference("localizador ABCDEF; code de réservation : PQR7ST; codice di prenotazione: LMN4OP") == [
        "localizador ABCDEF", "code de réservation : PQR7ST", "codice di prenotazione: LMN4OP"]
    # app data and links
    assert rre.booking_reference('{"bookingReference": "4TR9QX", "record_locator":"7HJKLP"} ?pnr=XK7P2Q&name=DOE') == [
        'bookingReference": "4TR9QX', 'record_locator":"7HJKLP', "pnr=XK7P2Q"]
    # no label, digits only, five and seven characters, lowercase, eight letters
    assert rre.booking_reference("XK7P2Q, Booking code: 123456, PNR: ABC12, PNR: ABC1234, PNR: abc123") == []
    assert rre.booking_reference("PNR status, confirmation code 482913, Reservation number: ABCDEFGH") == []
    assert rre.booking_reference("Bestelnummer ABC123, order ABC123") == []  # an order number


def test_travel_boarding_pass_barcode():
    # the IATA BCBP guide's example of one leg, and made-up ones
    bp = "M1DESMARAIS/LUC       EABC123 YULFRAAC 0834 226F001A0025 100"
    assert rre.boarding_pass_barcode(bp) == [bp]
    # the barcode ends where its sizes say: a quote and text after it on the line are left out
    assert rre.boarding_pass_barcode('{"barcode": "' + bp + '", "seat": "1A"}') == [bp]
    one = "M1DOE/JANE            EXK7P2Q BRUBCNSN 3171 172Y023C0098 100"
    assert rre.boarding_pass_barcode(f"scan 1: {one}\nscan 2: {bp} ok") == [one, bp]
    # 0x2D characters of conditional items after the first leg
    cond = "M1PEETERS/AN MS       EABC123 AMSLHRKL 1001 045M012A0003 12D>5180AKL 2A0742123456789 0KL                0"
    assert rre.boarding_pass_barcode(cond + " trailing text") == [cond]
    # two legs and security data
    two = ("M2DOE/JOHN MR         EK9Z2LM FRAJFKLH 0400 359J004D0012 120>60B0WW6359BLH 2A2202123456789 1"
           "K9Z2LM JFKBOSLH 7712 360J002A0001 100^108MEYCIQDx")
    assert rre.boarding_pass_barcode(two + " end") == [two]
    # a flight date of 000 and 367, five legs, lowercase, a name of 19 characters, a digit in an airport code
    assert rre.boarding_pass_barcode(one.replace("172Y", "000Y") + "\n" + one.replace("172Y", "367Y")) == []
    assert rre.boarding_pass_barcode("M5" + one[2:] + "\n" + one.replace("DOE/JANE", "doe/jane")) == []
    assert rre.boarding_pass_barcode(one.replace("DOE/JANE ", "DOE/JANE") + "\n" + one.replace("BCN", "BC1")) == []
    # inside a longer word; a second leg cut short
    assert rre.boarding_pass_barcode("X" + one + "\n" + "M2" + one[2:] + "XK7P2Q BCNBRUSN 3172 1") == []


def test_travel_aircraft_icao_address():
    # made up
    assert rre.aircraft_icao_address("ICAO 24-bit address: 44A1B2, Mode S hex 44a1b2.") == [
        "ICAO 24-bit address: 44A1B2", "Mode S hex 44a1b2"]
    assert rre.aircraft_icao_address('{"icao24":"44a1b2","callsign":"TEST123"} and ?icao24=44a1b2&time=0') == [
        'icao24":"44a1b2', "icao24=44a1b2"]
    assert rre.aircraft_icao_address("(ICAO hex: 4B1F2A) Mode-S code 40621D; icao address A1B2C3") == [
        "ICAO hex: 4B1F2A", "Mode-S code 40621D", "icao address A1B2C3"]
    # no label, hex alone (a colour as often), a colour
    assert rre.aircraft_icao_address('44A1B2, hex: 44A1B2, "hex":"44a1b2", #44a1b2') == []
    # ICAO documents and airport and airline codes
    assert rre.aircraft_icao_address("ICAO 9303, ICAO Doc 4444, ICAO code EBBR, ICAO: KLM") == []
    # seven and five hex digits, not hex, a transponder without its code
    assert rre.aircraft_icao_address("ICAO 44A1B2C, ICAO 44A1B, mode s 44A1BG, Mode S transponder") == []


def test_travel_fedex_tracking_number():
    # made up
    assert rre.fedex_tracking_number("FedEx 7489 1234 5679, FedEx tracking number: 748912345679") == [
        "FedEx 7489 1234 5679", "FedEx tracking number: 748912345679"]
    # Ground: 15 digits, and 22 starting with 96
    assert rre.fedex_tracking_number("fedex ground 1234 5678 9012 343 and FEDEX: 123456789012343.") == [
        "fedex ground 1234 5678 9012 343", "FEDEX: 123456789012343"]
    assert rre.fedex_tracking_number("FedEx 9611020123456776543218 (FedEx 9611 0201 2345 6776 5432 18)") == [
        "FedEx 9611020123456776543218", "FedEx 9611 0201 2345 6776 5432 18"]
    assert rre.fedex_tracking_number("FedEx Express (3987 6543 2103)") == ["FedEx Express (3987 6543 2103"]
    # no keyword, check digits wrong
    assert rre.fedex_tracking_number("7489 1234 5679, FedEx 7489 1234 5670, FedEx 1234 5678 9012 344") == []
    # 11 and 13 digits, a 22-digit one wrong, a year
    assert rre.fedex_tracking_number("FedEx 7489 1234 567, FedEx 7489 1234 5679 1, FedEx 9611020123456776543219") == []
    assert rre.fedex_tracking_number("FedEx 2024 annual report, FedEx Office 1234") == []
    # a 15-digit number whose check digit is wrong is not cut to its first 12 digits, which would pass
    assert rre.fedex_tracking_number("FedEx 1234 5678 9012 345") == []


def test_travel_usps_tracking_number():
    # made up
    assert rre.usps_tracking_number("USPS 9400 1123 4567 8901 2345 66 and 9205500000001234567896.") == [
        "USPS 9400 1123 4567 8901 2345 66", "9205500000001234567896"]
    assert rre.usps_tracking_number("(9300 1234 5678 9012 3456 75), 26 digits: 95055123456789012345678908") == [
        "9300 1234 5678 9012 3456 75", "95055123456789012345678908"]
    # 20 digits only after the keyword: Certified Mail
    assert rre.usps_tracking_number("usps 7019 2280 0000 1234 5677, USPS Certified Mail 70123460000123456789") == [
        "usps 7019 2280 0000 1234 5677", "USPS Certified Mail 70123460000123456789"]
    # check digit wrong, 20 digits without keyword, 21 and 23 digits
    assert rre.usps_tracking_number("9400 1123 4567 8901 2345 67, 70192280000012345677, USPS 7019 2280 0000 1234 5678") == []
    assert rre.usps_tracking_number("940011234567890123456, 94001123456789012345661") == []
    # FedEx's 96, UPU and UPS numbers
    assert rre.usps_tracking_number("9611020123456776543218, RR123456785US, 1Z999AA10123456784") == []
    # a failing 22-digit number is not cut to its first 20 digits, which would pass
    assert rre.usps_tracking_number("USPS 9400 1123 4567 8901 2303 00") == []


def test_travel_rf_creditor_reference():
    # ISO 11649's example, and made-up ones
    assert rre.rf_creditor_reference("RF18 5390 0754 7034 and RF18539007547034") == [
        "RF18 5390 0754 7034", "RF18539007547034"]
    assert rre.rf_creditor_reference("Reference: RF47ABC123. (RF7400000001)") == ["RF47ABC123", "RF7400000001"]
    # the shortest and the longest: 1 and 21 characters after the check digits
    assert rre.rf_creditor_reference("RF904, RF032026INV0042, RF34 1234 5678 9012 3456 7890 X") == [
        "RF904", "RF032026INV0042", "RF34 1234 5678 9012 3456 7890 X"]
    assert rre.rf_creditor_reference("RF18 5390 0754 7034 BIC") == ["RF18 5390 0754 7034"]
    # check digits wrong, lowercase, no reference, 22 characters, inside a word
    assert rre.rf_creditor_reference("RF18 5390 0754 7035, rf18539007547034, RF18, RF341234567890123456789012X") == []
    assert rre.rf_creditor_reference("XRF18539007547034, RF 18 5390 0754 7034") == []
    # radio parts
    assert rre.rf_creditor_reference("RF433 module, nRF24L01, RF 2.4 GHz, RF24 MODULE") == []


def test_travel_sepa_creditor_id():
    # the Bundesbank's example, and made-up ones
    assert rre.sepa_creditor_id("Gläubiger-ID: DE98ZZZ09999999999.") == ["DE98ZZZ09999999999"]
    assert rre.sepa_creditor_id("NL69ZZZ123456780000, BE81ZZZ0123456749 and FR78ZZZ123ABC") == [
        "NL69ZZZ123456780000", "BE81ZZZ0123456749", "FR78ZZZ123ABC"]
    assert rre.sepa_creditor_id("(ES11ZZZB12345674) DE98 ZZZ 09999999999 IT58ZZZ12345678901") == [
        "ES11ZZZB12345674", "DE98 ZZZ 09999999999", "IT58ZZZ12345678901"]
    # check digits wrong, an IBAN, no national identifier, lowercase, inside a word
    assert rre.sepa_creditor_id("DE98ZZZ09999999998, DE89370400440532013000, DE98ZZZ, de98zzz09999999999") == []
    assert rre.sepa_creditor_id("XDE98ZZZ09999999999, DE98ZZZ09999999999999999999999999999999") == []
    # a business code other than ZZZ is valid but not matched: without ZZZ the shape is an IBAN's
    assert rre.sepa_creditor_id("DE98AAA09999999999") == []


def test_travel_eori_number():
    # made up
    assert rre.eori_number("EORI: NL123456789, EORI number GB123456789000.") == [
        "EORI: NL123456789", "EORI number GB123456789000"]
    assert rre.eori_number("EORI-Nummer DE1234567; numéro EORI FR12345678901234") == [
        "EORI-Nummer DE1234567", "EORI FR12345678901234"]
    assert rre.eori_number("(EORI ESB12345674) EORI nr. BE0123456749, EORI XI123456789000") == [
        "EORI ESB12345674", "EORI nr. BE0123456749", "EORI XI123456789000"]
    # no label, a VAT number
    assert rre.eori_number("NL123456789, VAT NL123456789B01") == []
    # words, no digit, 16 characters after the country code, lowercase
    assert rre.eori_number("EORI registration, EORI number required, EORI: NLABCDEFGH") == []
    assert rre.eori_number("EORI: NL1234567890123456, EORI: nl123456789") == []


def test_travel_un_number():
    assert rre.un_number("UN 1203, UN1993 Flammable liquid, (UN 0004)") == ["UN 1203", "UN1993", "UN 0004"]
    assert rre.un_number("UN-Nummer 1203; UN No. 3480; numéro ONU 1202; UN-1263 PAINT") == [
        "UN-Nummer 1203", "UN No. 3480", "numéro ONU 1202", "UN-1263"]
    assert rre.un_number("UN number: 2014") == ["UN number: 2014"]
    # years after the
    assert rre.un_number("the UN 2030 Agenda, The UN 1948 declaration") == []
    # five and three digits, a test and a regulation, inside a word, lowercase, above 3999, no UN
    assert rre.un_number("UN 12345, UN 123, UN 38.3, UN R155, FUN 1234, UNO 1234, un 1234, UN 4000, 1203") == []


def test_travel_regexes_stay_fast():
    start = time.perf_counter()
    for text in ('Flight LH ' * 10000, 'M1' + ' ' * 99998, 'M1' * 50000, 'PNR ' * 25000, 'ICAO ' * 20000,
                 'FedEx 1234 ' * 9000, '9400 ' * 20000, 'RF18 ' * 20000, 'DE98 ZZZ ' * 11000, 'EORI NL' * 14000,
                 'UN 1203 ' * 12000, 'ticket 057 ' * 9000, '1' * 100000, 'A ' * 50000):
        rre.flight_number(text), rre.airline_ticket_number(text), rre.booking_reference(text)
        rre.boarding_pass_barcode(text), rre.aircraft_icao_address(text), rre.fedex_tracking_number(text)
        rre.usps_tracking_number(text), rre.rf_creditor_reference(text), rre.sepa_creditor_id(text)
        rre.eori_number(text), rre.un_number(text)
    assert time.perf_counter() - start < 2
