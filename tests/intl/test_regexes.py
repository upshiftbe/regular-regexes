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
    # a v3 address ends in its version byte 3: 'd', after a, i, q or y
    onion = "a" * 55 + "d.onion"
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


def test_ios_app_bundle_path():
    for path in (
        "/private/var/containers/Bundle/Application/29DE755A-A2B2-46D8-8C2E-341BB444AFC5/FindMy.app/x.mov",
        "/var/containers/Bundle/Application/X/App.app/Assets.car",
        "/private/var/containers/Bundle/Application/X/iTunesMetadata.plist",
    ):
        assert rre.ios_app_bundle_path(path) == [path]
    for path in (
        "/private/var/mobile/Containers/Data/Application/X/Documents/x.jpg",
        "/private/var/mobile/Containers/Shared/AppGroup/X/x.sqlite",
        "/data/app/com.example-1/base.apk",
        "/private/var/mobile/Media/containers/Bundle/x",
        "text /private/var/containers/Bundle/x",
        "",
    ):
        assert rre.ios_app_bundle_path(path) == []


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


# hardened tests: at least six written forms and six near-misses per regex


def test_hard_iban():
    # SWIFT IBAN registry examples, ISO 13616's, and made-up ones
    assert rre.iban("IBAN: BE68 5390 0754 7034.") == ["BE68 5390 0754 7034"]
    assert rre.iban("NL91ABNA0417164300") == ["NL91ABNA0417164300"]
    assert rre.iban('{"iban": "DE89370400440532013000"}') == ["DE89370400440532013000"]
    assert rre.iban("https://bank.example/pay?iban=FR1420041010050500013M02606&amount=5") == [
        "FR1420041010050500013M02606"]
    # the shortest (Norway, 15) and longest (Russia, 33); Malta and Saint Lucia with letters inside
    assert rre.iban("(NO9386011117947) RU0204452560040702810412345678901") == [
        "NO9386011117947", "RU0204452560040702810412345678901"]
    assert rre.iban("MT84MALT011000012345MTLCAST001S\nLC55HEMM000100010012001200023015") == [
        "MT84MALT011000012345MTLCAST001S", "LC55HEMM000100010012001200023015"]
    # a country that uses IBANs outside the registry (Senegal, made up)
    assert rre.iban("SN08SN0100152000048500003035") == ["SN08SN0100152000048500003035"]
    # check digits wrong, a character short
    assert rre.iban("BE68 5390 0754 7035") == []
    assert rre.iban("BE68 5390 0754 703") == []
    # an RF creditor reference has the same check digits; a country without IBANs; Belgium at 15 and 17 characters
    assert rre.iban("RF18 5390 0754 7034") == []
    assert rre.iban("QQ91539007547034") == []
    assert rre.iban("BE0853900754703") == []
    assert rre.iban("BE705390075470341") == []
    # lower case, glued to a letter, a SEPA creditor identifier
    assert rre.iban("be68 5390 0754 7034") == []
    assert rre.iban("BE68539007547034X") == []
    assert rre.iban("DE98ZZZ09999999999") == []


def test_hard_credit_card():
    # payment card test numbers
    assert rre.credit_card("4111-1111-1111-1111") == ["4111-1111-1111-1111"]
    assert rre.credit_card("Amex 3782 822463 10005.") == ["3782 822463 10005"]
    assert rre.credit_card("(5555555555554444)") == ["5555555555554444"]
    assert rre.credit_card('{"pan": "6011000990139424"}') == ["6011000990139424"]
    assert rre.credit_card("Diners 3056 930902 5904, Visa 4222222222222 and 378282246310005") == [
        "3056 930902 5904", "4222222222222", "378282246310005"]
    # 19 digits (made up), 2-series Mastercard, a card followed by its expiry date
    assert rre.credit_card("6222 0200 0000 0000 000, 2223 0000 4840 0011") == [
        "6222 0200 0000 0000 000", "2223 0000 4840 0011"]
    assert rre.credit_card("card 4111 1111 1111 1111 12/25 cvv 123") == ["4111 1111 1111 1111"]
    # Luhn fails; 12 and 20 digits
    assert rre.credit_card("4111 1111 1111 1112") == []
    assert rre.credit_card("411111111111") == []
    assert rre.credit_card("41111111111111111111") == []
    # glued to a letter; separators mixed; groups not of four
    assert rre.credit_card("x4111111111111111") == []
    assert rre.credit_card("4111 1111-1111 1111") == []
    assert rre.credit_card("SIRET 552120222 00013") == []
    # four groups inside a longer run, at its start and end
    assert rre.credit_card("1234 4111 1111 1111 1111") == []
    assert rre.credit_card("4111 1111 1111 1111 2222") == []
    # 13 digits are Visa only, 14 Diners Club, 15 American Express: an EAN-13 barcode, a SIRET, an IMEI, an IMSI
    assert rre.credit_card("EAN 5901234123457") == []
    assert rre.credit_card("SIRET 55212022200013") == []
    assert rre.credit_card("IMEI 490154203237518") == []
    assert rre.credit_card("IMSI 260021234567890") == []
    # blocks of a BitLocker key, a USPS number, an IBAN
    assert rre.credit_card("BitLocker: 220088-440000-720885-013574-333333-000055-244442-659989") == []
    assert rre.credit_card("USPS 9300 1234 5678 9012 3456 75") == []
    assert rre.credit_card("DE89 3704 0044 0532 0130 00") == []


def test_hard_card_dump():
    assert rre.card_dump("4111111111111111/12/25/123") == ["4111111111111111/12/25/123"]
    assert rre.card_dump("dump: 5555555555554444;0127;456;US") == ["5555555555554444;0127;456;US"]
    assert rre.card_dump('"4111111111111111|12|2025|123"') == ["4111111111111111|12|2025|123"]
    assert rre.card_dump("4111111111111111 | 1 | 2025 | 123") == ["4111111111111111 | 1 | 2025 | 123"]
    assert rre.card_dump("6011000990139424:12:2026:999:JANE DOE:TESTSTRAAT 1\n") == [
        "6011000990139424:12:2026:999:JANE DOE:TESTSTRAAT 1"]
    assert rre.card_dump("4111111111111111|12/25|123 sold") == ["4111111111111111|12/25|123"]
    # month 00, a CVV of two or five digits, no CVV, a 12-digit number
    assert rre.card_dump("4111111111111111|00|2025|123") == []
    assert rre.card_dump("4111111111111111|12|2025|12") == []
    assert rre.card_dump("4111111111111111|12|2025|12345") == []
    assert rre.card_dump("4111111111111111|12|2025") == []
    assert rre.card_dump("411111111111|12|2025|123") == []
    # inside a longer digit run, glued to a letter, a date
    assert rre.card_dump("14111111111111111|12|2025|123") == []
    assert rre.card_dump("x4111111111111111|12|25|123") == []
    assert rre.card_dump("2024|12|2025|123") == []


def test_hard_card_track_data():
    track1 = "%B5555555555554444^DOE/JANE^2701101000000000000000000?"
    assert rre.card_track_data(track1) == [track1]
    assert rre.card_track_data("track2=4111111111111111=2512101123") == ["4111111111111111=2512101123"]
    # EMV track 2 equivalent data, padded with F
    assert rre.card_track_data("57: 4111111111111111D25121011234567F") == ["4111111111111111D25121011234567F"]
    assert rre.card_track_data("B4111111111111111^TEST/CARD^2512101") == ["B4111111111111111^TEST/CARD^2512101"]
    assert rre.card_track_data('{"track2": ";5555555555554444=27011010000000000000?"}') == [
        ";5555555555554444=27011010000000000000?"]
    assert rre.card_track_data("x;4111111111111111=2512101123?") == [";4111111111111111=2512101123?"]
    # month 00, a name of 27 characters, no expiry date, no first ^
    assert rre.card_track_data("%B4111111111111111^TEST/CARD^25001010000000000000?") == []
    assert rre.card_track_data("%B4111111111111111^ABCDEFGHIJKLMNOPQRSTUVWXYZA^25121010000000000000?") == []
    assert rre.card_track_data("%B4111111111111111^TEST/CARD^?") == []
    assert rre.card_track_data("%B4111111111111111TEST/CARD^2512101?") == []
    # a 12- and a 20-digit number, Luhn fails, inside a hexadecimal token
    assert rre.card_track_data(";411111111111=2512101?") == []
    assert rre.card_track_data(";12345678901234567890=2512101?") == []
    assert rre.card_track_data(";4111111111111112=2512101123?") == []
    assert rre.card_track_data("4111111111111111D2512101123ABCDEF") == []


def test_hard_currency_amount():
    # a capitalised code glued to the amount, Italian euro before the amount, a year after EUR, Ether
    assert rre.currency_amount("EUR100 and USD12,000.") == ["EUR100", "USD12,000"]
    assert rre.currency_amount("importo euro 1.249,99 (Euro 5,00 di spese)") == ["euro 1.249,99", "Euro 5,00"]
    assert rre.currency_amount("EUR 2024, 6 euros") == ["EUR 2024", "6 euros"]
    assert rre.currency_amount("eth 0.5 or 2 ETH") == ["eth 0.5", "2 ETH"]
    # the Euro 2024 tournament, Euro 6 emission standards
    assert rre.currency_amount("the Euro 2024 final") == []
    assert rre.currency_amount("a Euro 6d-TEMP diesel") == []
    assert rre.currency_amount("EURO 6 engine") == []
    # a network interface, the start of a Litecoin address, the end of an IBAN before its currency
    assert rre.currency_amount("eth0: flags=4163<UP>") == []
    assert rre.currency_amount("ltc1qm43ude0604ujspt5838rkg0whvgsuv40stzdek") == []
    assert rre.currency_amount("account BE68 5390 0754 7034 EUR") == []
    # a version number, a word that starts with a code
    assert rre.currency_amount("version 1.2.3 EUR") == []
    assert rre.currency_amount("Europe 2024, neuro 5") == []


def test_hard_gift_card_code():
    assert rre.gift_card_code("paysafecard 1234 5678 9012 3456 50€") == ["paysafecard 1234 5678 9012 3456"]
    # look-alikes: no digit in an Amazon, Google Play or Steam code
    assert rre.gift_card_code("amazon BLACK-FRIDAY-DEAL") == []
    assert rre.gift_card_code("Google Play GIFT CARD CODE HERE") == []
    assert rre.gift_card_code("steam STEAM-STEAM-STEAM") == []
    # a 17-digit paysafecard PIN, not cut to its first 12; a Neosurf code without digits
    assert rre.gift_card_code("paysafecard 1234 5678 9012 34567") == []
    assert rre.gift_card_code("neosurf ABCDEFGHIJ") == []
    # lower case, glued to the brand, a character too many
    assert rre.gift_card_code("apple x123456789abcdef") == []
    assert rre.gift_card_code("steamABCDE-FGH1J-KLMNO") == []
    assert rre.gift_card_code("steam ABCDE-FGH1J-KLMNOP") == []


def test_hard_rf_creditor_reference():
    # check digits right, but 22 characters after them
    assert rre.rf_creditor_reference("RF22ABCDEFGHIJKLMNOPQRSTUV") == []
    # dashes, check digits 00, lower case
    assert rre.rf_creditor_reference("RF18-5390-0754-7034") == []
    assert rre.rf_creditor_reference("RF00539007547034") == []
    assert rre.rf_creditor_reference("rf18 5390 0754 7034") == []


def test_hard_sepa_creditor_id():
    # dashes, a character short, lower case
    assert rre.sepa_creditor_id("DE98-ZZZ-09999999999") == []
    assert rre.sepa_creditor_id("DE98ZZZ0999999999") == []
    assert rre.sepa_creditor_id("de98ZZZ09999999999") == []


def test_hard_eori_number():
    # not an EU country (nor GB or XI)
    assert rre.eori_number("EORI: QQ123456789") == []
    assert rre.eori_number("EORI: US123456789") == []
    # lower case, 16 characters after the country code, no number
    assert rre.eori_number("eori: nl123456789") == []
    assert rre.eori_number("EORI: NL1234567890123456") == []
    assert rre.eori_number("EORI number required") == []


def test_hard_isin():
    # the common example and made-up ones
    assert rre.isin("ISIN:US0378331005") == ["ISIN:US0378331005"]
    assert rre.isin("(ISIN XS000TEST009)") == ["ISIN XS000TEST009"]
    assert rre.isin("ISIN-Code: DE000TEST009, ISIN code LU000TEST017") == [
        "ISIN-Code: DE000TEST009", "ISIN code LU000TEST017"]
    assert rre.isin("ISIN IE00B0TEST06.") == ["ISIN IE00B0TEST06"]
    # 11 and 13 characters, the keyword in lower case or glued, a digit in the country code, a letter as check digit
    assert rre.isin("ISIN US037833100") == []
    assert rre.isin("ISIN US03783310055") == []
    assert rre.isin("isin US0378331005") == []
    assert rre.isin("ISINUS0378331005") == []
    assert rre.isin("ISIN 1S0378331005") == []
    assert rre.isin("ISIN US037833100A") == []
    assert rre.isin('"ISIN": "IE00B0TEST06"') == []


def test_hard_lei():
    # GLEIF's own LEI, and made-up ones
    assert rre.lei("LEI: 506700GE1G29325QX363.") == ["506700GE1G29325QX363"]
    assert rre.lei("https://search.gleif.org/#/record/969500ABCDEFGHIJKL46") == ["969500ABCDEFGHIJKL46"]
    assert rre.lei('{"lei": "213800ABCDEFGHIJ1273"}') == ["213800ABCDEFGHIJ1273"]
    assert rre.lei("(549300TESTLEI0000064)") == ["549300TESTLEI0000064"]
    assert rre.lei("724500EXAMPLE0000125") == ["724500EXAMPLE0000125"]
    # 19 and 21 characters, glued to a letter, lower case
    assert rre.lei("506700GE1G29325QX36") == []
    assert rre.lei("506700GE1G29325QX3633") == []
    assert rre.lei("X506700GE1G29325QX363") == []
    assert rre.lei("506700ge1g29325qx363") == []
    # an IBAN without spaces and a hexadecimal token of the same shape
    assert rre.lei("LU280019400644750000") == []
    assert rre.lei("3F2504E04F8911D39A0C") == []


def test_hard_mrz_id_card():
    # ICAO 9303 specimen (in its three-line zone), the Belgian, German and Dutch specimens, made-up type A and C cards
    zone = "I<UTOD231458907<<<<<<<<<<<<<<<\n7408122F1204159UTO<<<<<<<<<<<6\nERIKSSON<<ANNA<MARIA<<<<<<<<<<"
    assert rre.mrz_id_card(zone) == ["I<UTOD231458907<<<<<<<<<<<<<<<"]
    assert rre.mrz_id_card('"IDBEL592123456<782<<<<<<<<<<<<"') == ["IDBEL592123456<782<<<<<<<<<<<<"]
    assert rre.mrz_id_card("MRZ: IDD<<T220001293<<<<<<<<<<<<<<<") == ["IDD<<T220001293<<<<<<<<<<<<<<<"]
    assert rre.mrz_id_card("I<NLDSPECI20142999999990<<<<<<\n") == ["I<NLDSPECI20142999999990<<<<<<"]
    assert rre.mrz_id_card("A<UTOAB12345671<<<<<<<<<<<<<<<") == ["A<UTOAB12345671<<<<<<<<<<<<<<<"]
    assert rre.mrz_id_card("(CIUTOCD98765435<<<<<<<<<<<<<<<)") == ["CIUTOCD98765435<<<<<<<<<<<<<<<"]
    # 29 and 31 characters, check digit wrong (also of a long number), lower case
    assert rre.mrz_id_card("I<UTOD231458907<<<<<<<<<<<<<<") == []
    assert rre.mrz_id_card("I<UTOD231458907<<<<<<<<<<<<<<<<") == []
    assert rre.mrz_id_card("IDBEL592123456<781<<<<<<<<<<<<") == []
    assert rre.mrz_id_card("i<utod231458907<<<<<<<<<<<<<<<") == []
    # a passport's first line, a TD2 first line (36), a name line starting with A, a digit in the country code
    assert rre.mrz_id_card("P<UTOD231458907<<<<<<<<<<<<<<<") == []
    assert rre.mrz_id_card("I<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<") == []
    assert rre.mrz_id_card("ADAMS<<JOHN<<<<<<<<<<<<<<<<<<<") == []
    assert rre.mrz_id_card("I<UT0D231458907<<<<<<<<<<<<<<<") == []


def test_hard_mrz_passport():
    td3 = "L898902C36UTO7408122F1204159ZE184226B<<<<<10"
    assert rre.mrz_passport(f"P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\n{td3}\n") == [td3]
    assert rre.mrz_passport(f'"{td3}"') == [td3]
    # the Dutch and German specimens; made up: another country, sex X
    assert rre.mrz_passport("SPECI20142NLD6503101F3103094999999990<<<<<82") == [
        "SPECI20142NLD6503101F3103094999999990<<<<<82"]
    assert rre.mrz_passport("MRZ C01X00T478D<<6408125F2702283<<<<<<<<<<<<<<<4") == [
        "C01X00T478D<<6408125F2702283<<<<<<<<<<<<<<<4"]
    assert rre.mrz_passport("(L898902C36BEL7408122F1204159ZE184226B<<<<<10)") == [
        "L898902C36BEL7408122F1204159ZE184226B<<<<<10"]
    assert rre.mrz_passport("L898902C36UTO7408122X1204159ZE184226B<<<<<10") == [
        "L898902C36UTO7408122X1204159ZE184226B<<<<<10"]
    # 43 and 45 characters, each check digit wrong in turn
    assert rre.mrz_passport(td3[:-1]) == []
    assert rre.mrz_passport(td3 + "<") == []
    assert rre.mrz_passport("L898902C35UTO7408122F1204159ZE184226B<<<<<10") == []
    assert rre.mrz_passport("L898902C36UTO7408121F1204159ZE184226B<<<<<10") == []
    assert rre.mrz_passport("L898902C36UTO7408122F1204158ZE184226B<<<<<10") == []
    # sex Y, lower case, the first line, two lines glued together
    assert rre.mrz_passport("L898902C36UTO7408122Y1204159ZE184226B<<<<<10") == []
    assert rre.mrz_passport(td3.lower()) == []
    assert rre.mrz_passport("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<") == []
    assert rre.mrz_passport(td3 + td3) == []


def test_hard_paypal_me_link():
    assert rre.paypal_me_link("PayPal.Me/TestUser") == ["PayPal.Me/TestUser"]
    assert rre.paypal_me_link("(paypal.me/testuser)") == ["paypal.me/testuser"]
    assert rre.paypal_me_link('"http://www.paypal.me/TestUser/10,50EUR"') == ["http://www.paypal.me/TestUser/10,50EUR"]
    assert rre.paypal_me_link("https://www.paypal.com/paypalme/testuser/5 thanks") == [
        "https://www.paypal.com/paypalme/testuser/5"]
    assert rre.paypal_me_link("paypal.me/testuser?locale.x=en_US") == ["paypal.me/testuser"]
    # PayPal.Me's own settings page, no name, glued to a word, another domain
    assert rre.paypal_me_link("paypal.com/paypalme/my/profile") == []
    assert rre.paypal_me_link("paypal.me/") == []
    assert rre.paypal_me_link("xpaypal.me/testuser") == []
    assert rre.paypal_me_link("notpaypal.me/testuser") == []
    assert rre.paypal_me_link("paypal.mex/testuser") == []
    assert rre.paypal_me_link("paypal.me/pools/c/8abc") == []


def test_hard_revolut_link():
    assert rre.revolut_link("https://revolut.me/testuser1") == ["https://revolut.me/testuser1"]
    assert rre.revolut_link("REVOLUT.ME/TESTUSER2") == ["REVOLUT.ME/TESTUSER2"]
    assert rre.revolut_link("pay me: revolut.me/testuser3?amount=10") == ["revolut.me/testuser3"]
    assert rre.revolut_link('<a href="https://revolut.me/abc">') == ["https://revolut.me/abc"]
    assert rre.revolut_link("www.revolut.me/abcdefghijklmnop.") == ["www.revolut.me/abcdefghijklmnop"]
    assert rre.revolut_link("(checkout.revolut.com/payment-link/0a1b2c3d)") == [
        "checkout.revolut.com/payment-link/0a1b2c3d"]
    # 17 characters, glued to a word, a hyphen or @, a checkout id too short, another path
    assert rre.revolut_link("revolut.me/abcdefghijklmnopq") == []
    assert rre.revolut_link("xrevolut.me/abc") == []
    assert rre.revolut_link("revolut.me/a-b") == []
    assert rre.revolut_link("revolut.me/@testuser") == []
    assert rre.revolut_link("https://checkout.revolut.com/payment-link/abc") == []
    assert rre.revolut_link("revolut.com/r/abc") == []


def test_hard_payconiq_link():
    assert rre.payconiq_link("payconiq.com/pay/1/abc123") == ["payconiq.com/pay/1/abc123"]
    assert rre.payconiq_link('{"qr": "https://payconiq.com/pay/2/abc123?amount=1000&description=x"}') == [
        "https://payconiq.com/pay/2/abc123?amount=1000&description=x"]
    assert rre.payconiq_link("(www.payconiq.com/pay/2/abc)") == ["www.payconiq.com/pay/2/abc"]
    # version 3, a static QR code of version 2, no id, glued to a word
    assert rre.payconiq_link("https://payconiq.com/pay/3/abc") == []
    assert rre.payconiq_link("https://payconiq.com/l/2/abc") == []
    assert rre.payconiq_link("payconiq.com/pay/2/") == []
    assert rre.payconiq_link("xpayconiq.com/pay/2/abc") == []
    # an id with an underscore or of 65 characters is not cut short; another host
    assert rre.payconiq_link("payconiq.com/pay/2/abc_def") == []
    assert rre.payconiq_link("payconiq.com/pay/2/" + "a" * 65) == []
    assert rre.payconiq_link("https://pay.bancontact.net.example.com/pay/2/abc") == []


def test_hard_bip39_seed_phrase():
    # official test vectors, written in capitals, title case, with commas, hyphens, one per line or numbered 1) 2) ...
    p12 = "legal winner thank year wave sausage worth useful legal winner thank yellow"
    zero = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    assert rre.bip39_seed_phrase(p12.upper()) == [p12.upper()]
    assert rre.bip39_seed_phrase(f"Seed: {p12.title()}.") == [p12.title()]
    assert rre.bip39_seed_phrase(p12.replace(" ", ", ")) == [p12.replace(" ", ", ")]
    assert rre.bip39_seed_phrase(f'"{p12.replace(" ", "-")}"') == [p12.replace(" ", "-")]
    assert rre.bip39_seed_phrase(f"wallet A: {p12}\nwallet B: {zero}") == [p12, zero]
    numbered = " ".join(f"{i}) {w}" for i, w in enumerate(zero.split(), 1))
    assert rre.bip39_seed_phrase(numbered) == [numbered[3:]]
    # checksum wrong, 11 words, glued to a letter at either end, written without spaces or with underscores
    assert rre.bip39_seed_phrase(zero.replace("about", "abandon")) == []
    assert rre.bip39_seed_phrase(" ".join(p12.split()[:11])) == []
    assert rre.bip39_seed_phrase("x" + p12) == []
    assert rre.bip39_seed_phrase(p12 + "x") == []
    assert rre.bip39_seed_phrase(p12.replace(" ", "")) == []
    assert rre.bip39_seed_phrase(p12.replace(" ", "_")) == []


def test_hard_bitcoin_address():
    # BIP173/BIP350 test vectors: in capitals as in QR codes, P2WSH and Taproot; the Bitcoin wiki's P2SH example
    assert rre.bitcoin_address("BITCOIN:BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4") == [
        "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4"]
    assert rre.bitcoin_address("(bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3)") == [
        "bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3"]
    assert rre.bitcoin_address('{"to": "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vqzk5jj0"}') == [
        "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vqzk5jj0"]
    assert rre.bitcoin_address("bitcoin:3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy?amount=0.1") == [
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"]
    # made up: P2PKH and P2SH
    assert rre.bitcoin_address("19uMPEqUGkxwf92ixFPkybcfHLdNorNWka\n3Jf4gsoQpw6vhnR213xzm5JcxuA86faKa2.") == [
        "19uMPEqUGkxwf92ixFPkybcfHLdNorNWka", "3Jf4gsoQpw6vhnR213xzm5JcxuA86faKa2"]
    # witness version 0 with a bech32m checksum (BIP350), version 1 with a bech32 one (made up), mixed case
    assert rre.bitcoin_address("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kemeawh") == []
    assert rre.bitcoin_address("bc1pprt4x8anym0sfc49dda8rwmp05mdm559hpex6qu4n3g35c4zt0csdjnlw6") == []
    assert rre.bitcoin_address("bc1qW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4") == []
    # made up: valid base58check with version byte 6 (also 3...); a character short, one too many, glued to a word
    assert rre.bitcoin_address("3SAupu6NCHraCfBXyuhFJo2vex6sgpe5sJ") == []
    assert rre.bitcoin_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfN") == []
    assert rre.bitcoin_address("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4x") == []
    assert rre.bitcoin_address("x1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == []
    # testnet addresses, a Litecoin address
    assert rre.bitcoin_address("tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx mipcBbFg9gMiCh81Kj8tqqdgoZub1ZJRfn") == []
    assert rre.bitcoin_address("LKDyUEtTR1HXamkiEphisSiBJu6o3ZPE34") == []


def test_hard_litecoin_address():
    # made up: L... (version 48), M... (50), SegWit P2WPKH and P2WSH, in capitals
    assert rre.litecoin_address("LUnH8y2ghiitRDHyMXiJrY43YB21CXbLJK") == ["LUnH8y2ghiitRDHyMXiJrY43YB21CXbLJK"]
    assert rre.litecoin_address("litecoin:MCTQCkH4bbSvoVtRjb4a6jJ7nwzQUWqRbV?amount=2") == [
        "MCTQCkH4bbSvoVtRjb4a6jJ7nwzQUWqRbV"]
    assert rre.litecoin_address('"ltc1qm43ude0604ujspt5838rkg0whvgsuv40stzdek"') == [
        "ltc1qm43ude0604ujspt5838rkg0whvgsuv40stzdek"]
    assert rre.litecoin_address("(ltc1qshkvhng7knk650j45x8qukhw04vrvf4uvzd6vc34zz9lx8zhgypsvujk9g)") == [
        "ltc1qshkvhng7knk650j45x8qukhw04vrvf4uvzd6vc34zz9lx8zhgypsvujk9g"]
    assert rre.litecoin_address("LTC1QM43UDE0604UJSPT5838RKG0WHVGSUV40STZDEK") == [
        "LTC1QM43UDE0604UJSPT5838RKG0WHVGSUV40STZDEK"]
    assert rre.litecoin_address("https://litecoinspace.org/address/LKDyUEtTR1HXamkiEphisSiBJu6o3ZPE34") == [
        "LKDyUEtTR1HXamkiEphisSiBJu6o3ZPE34"]
    # made up: valid base58check with version 49 (also L...); checksum broken, a character short, glued to a word
    assert rre.litecoin_address("Lq3c2XfgF3vUHjJDEukPJoi2zUGYmGjRWe") == []
    assert rre.litecoin_address("LUnH8y2ghiitRDHyMXiJrY43YB21CXbLJL") == []
    assert rre.litecoin_address("LUnH8y2ghiitRDHyMXiJrY43YB21CXbLJ") == []
    assert rre.litecoin_address("xLUnH8y2ghiitRDHyMXiJrY43YB21CXbLJK") == []
    # mixed case, testnet, a Bitcoin P2SH and a Bitcoin SegWit address
    assert rre.litecoin_address("ltc1qM43UDE0604UJSPT5838RKG0WHVGSUV40STZDEK") == []
    assert rre.litecoin_address("tltc1qm43ude0604ujspt5838rkg0whvgsuv40stzdek") == []
    assert rre.litecoin_address("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy") == []
    assert rre.litecoin_address("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4") == []


def test_hard_tron_address():
    # made up: base58check with Tron's version byte 0x41
    assert rre.tron_address("TXGzd77VsoUsfdFcN897QReH7PzCVDswwv") == ["TXGzd77VsoUsfdFcN897QReH7PzCVDswwv"]
    assert rre.tron_address("USDT (TRC-20): TExiFtF2M1JqHdknDuAXcUyvTZtHBZY6c9.") == [
        "TExiFtF2M1JqHdknDuAXcUyvTZtHBZY6c9"]
    assert rre.tron_address('{"address": "TFn3ZAniEP4ix5fMkWtRz8YzvDZ514pi1k"}') == [
        "TFn3ZAniEP4ix5fMkWtRz8YzvDZ514pi1k"]
    assert rre.tron_address("https://tronscan.org/#/address/TSZMkRZfG3Z1bC4K5ftRnk8CTBCAsVVDCD") == [
        "TSZMkRZfG3Z1bC4K5ftRnk8CTBCAsVVDCD"]
    assert rre.tron_address("(TMD2kPRt7Fq5vNRMpfVxayQnqjwobzTb8G)") == ["TMD2kPRt7Fq5vNRMpfVxayQnqjwobzTb8G"]
    # made up: valid base58check with version 0x42 (also T...); checksum broken, a character short and one too many
    assert rre.tron_address("TifgD74ZHBtYkoRZEuqf9Xq5u2KFK7xNRU") == []
    assert rre.tron_address("TXGzd77VsoUsfdFcN897QReH7PzCVDswwu") == []
    assert rre.tron_address("TXGzd77VsoUsfdFcN897QReH7PzCVDsww") == []
    assert rre.tron_address("TXGzd77VsoUsfdFcN897QReH7PzCVDswwvz") == []
    # glued to a word, lower case t, the address in hex
    assert rre.tron_address("xTXGzd77VsoUsfdFcN897QReH7PzCVDswwv") == []
    assert rre.tron_address("tXGzd77VsoUsfdFcN897QReH7PzCVDswwv") == []
    assert rre.tron_address("41a614f803b6fd780986a42c78ec9c7f77e6ded13c") == []


def test_hard_bitcoin_private_key():
    # made up: WIF of SHA-256 keys, uncompressed (5...) and compressed (K..., L...)
    assert rre.bitcoin_private_key("WIF: 5JB5Z3dJh7qCnmj1FWnw6RVBJrxNBcNCvSfNbvm5vhi26rGtGe9") == [
        "5JB5Z3dJh7qCnmj1FWnw6RVBJrxNBcNCvSfNbvm5vhi26rGtGe9"]
    assert rre.bitcoin_private_key('"KxoV6SbF659m32QQ74Vjkw5NVqVNVq6bctGNMAHak2g3rZanq6sj"') == [
        "KxoV6SbF659m32QQ74Vjkw5NVqVNVq6bctGNMAHak2g3rZanq6sj"]
    assert rre.bitcoin_private_key("5JYYfHogsFB5rUhyaJPY7U6WVM2WLyGGYSrn4vvsSyQLpwKfPdR\n"
                                   "KzSEk1B4xmZWRPHrhykUKYbKA7PeX9LPbo8hvM2mfdx2WLtg7Jsb") == [
        "5JYYfHogsFB5rUhyaJPY7U6WVM2WLyGGYSrn4vvsSyQLpwKfPdR", "KzSEk1B4xmZWRPHrhykUKYbKA7PeX9LPbo8hvM2mfdx2WLtg7Jsb"]
    assert rre.bitcoin_private_key("(5HwCtCrzEnY3gUuimuVpyZLgzoksBFj6sRVc3drTvwV3Avkaezq)") == [
        "5HwCtCrzEnY3gUuimuVpyZLgzoksBFj6sRVc3drTvwV3Avkaezq"]
    assert rre.bitcoin_private_key("key=KwkFT1Mddqz2qGBhPCiEkdjuY9NcUFzpuZ7FgdfKs5UkafWzEm2r.") == [
        "KwkFT1Mddqz2qGBhPCiEkdjuY9NcUFzpuZ7FgdfKs5UkafWzEm2r"]
    # testnet keys (9..., c...); made up: valid base58check with version 0x7e (also 5...) and 0x81 (also L...)
    assert rre.bitcoin_private_key("91wi8nSrHLuLkqEHsrgqy238xXK5LmuQGPXKgZ7bGST4svvaUay") == []
    assert rre.bitcoin_private_key("cPAUZMb6X8r2CTsfVUJs8FaS84nnAHCHgvQqTak6F9L47JgGv86s") == []
    assert rre.bitcoin_private_key("5F5egJfqeJHxic8Azka8NmmorCgK9DEQDXoPcLbkeV7mTRGGSyL") == []
    assert rre.bitcoin_private_key("LE32gTaqSzLrAstJka4ij97xE7MiqVQz93DTcaodN833yMuDpzia") == []
    # a character short or too many (52 is the compressed length), glued to a word
    assert rre.bitcoin_private_key("5JB5Z3dJh7qCnmj1FWnw6RVBJrxNBcNCvSfNbvm5vhi26rGtGe") == []
    assert rre.bitcoin_private_key("5JB5Z3dJh7qCnmj1FWnw6RVBJrxNBcNCvSfNbvm5vhi26rGtGe9z") == []
    assert rre.bitcoin_private_key("xKxoV6SbF659m32QQ74Vjkw5NVqVNVq6bctGNMAHak2g3rZanq6sj") == []


def test_hard_bitcoin_cash_address():
    p2pkh = "bitcoincash:qr6m7j9njldwwzlg9v7v53unlr4jkmx6eylep8ekg2"
    assert rre.bitcoin_cash_address(f'{{"cashaddr": "{p2pkh}"}}') == [p2pkh]
    # the spec's P2SH address without its prefix, in capitals
    assert rre.bitcoin_cash_address("(PPM2QSZNHKS23Z7629MMS6S4CWEF74VCWVN0H829PQ)") == [
        "PPM2QSZNHKS23Z7629MMS6S4CWEF74VCWVN0H829PQ"]
    # testnet, mixed case, checksum broken, a character short and one too many, glued to a word
    assert rre.bitcoin_cash_address("bchtest:pr6m7j9njldwwzlg9v7v53unlr4jkmx6eyvwc0uz5t") == []
    assert rre.bitcoin_cash_address("bitcoincash:qr6m7j9njldwwzlg9v7v53unlr4jkmx6eylEP8EKG2") == []
    assert rre.bitcoin_cash_address(p2pkh[:-1] + "3") == []
    assert rre.bitcoin_cash_address(p2pkh[:-1]) == []
    assert rre.bitcoin_cash_address(p2pkh + "q") == []
    assert rre.bitcoin_cash_address("x" + p2pkh[12:]) == []
    # the same key as a legacy Bitcoin address, a SegWit address
    assert rre.bitcoin_cash_address("1PQPheJQSauxRPTxzNMUco1XmoCyPoEJCp") == []
    assert rre.bitcoin_cash_address("bitcoincash:bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4") == []


def test_hard_bitcoin_extended_key():
    # BIP32 test vector 2's master key; made up: test vector 1's key with SLIP-132's zpub, ypub, Zpub and tpub versions
    v2 = ("xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCG"
          "u8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB")
    zpub = ("zpub6jftahH18ngZxUuv6oSniLNrBCSSE1B4EEU59bwTCEt8x6aS6b2mdfLx"
            "bS4QS53g85SWWP6wexqeer516433gYpZQoJie2tcMYdJ1SYYYAL")
    ypub = ("ypub6QqdH2c5z7967BioGSfAWFHM1EHzHPBZK7wrND3ZpEWFtzmCqvsD1bgp"
            "aE6pSAPkiSKhkuWPCJV6mZTSNMd2tK8xYTcJ48585pZecmSUzWp")
    zpub_m = ("Zpub6vZyhw1ShkEwP45J3TumYQietzUhSMreYW7k4sCza1iYaH9LrzR3inCt"
              "Q91szWGaMYWVNy74YBE9n1gmPHBzq2wEFGR83SMcFGuAbGkfiwg")
    tpub = ("tpubD6NzVbkrYhZ4XgiXtGrdW5XDAPFCL9h7we1vwNCpn8tGbBcgfVYjXyhW"
            "o4E1xkh56hjod1RhGjxbaTLV3X4FyWuejifB9jusQ46QzG87VKp")
    assert rre.bitcoin_extended_key(f"{v2}\n") == [v2]
    assert rre.bitcoin_extended_key(f"Electrum: {zpub}.") == [zpub]
    assert rre.bitcoin_extended_key(f'{{"xpub": "{ypub}"}}') == [ypub]
    assert rre.bitcoin_extended_key(f"multisig ({zpub_m}) testnet [{tpub}]") == [zpub_m, tpub]
    # a character too many, glued to a word, Litecoin's Ltub, version bytes of no wallet (made up), a 0 in the key
    assert rre.bitcoin_extended_key(v2 + "x") == []
    assert rre.bitcoin_extended_key("x" + v2) == []
    assert rre.bitcoin_extended_key("Ltub" + v2[4:]) == []
    assert rre.bitcoin_extended_key("DQks7kWSypcuLVthoWvRMruX6xNjNCaVuKY43yKFh5fKCaNa9ZPL9BT1dNu2Qqu79ed9sDPvLQL2dAU"
                                    "p4kKzmkWi8kVy7EU6qJdUG5VaGLkRZYz") == []
    assert rre.bitcoin_extended_key(v2[:-1] + "0") == []
    assert rre.bitcoin_extended_key(zpub[:-1] + "M") == []


def test_hard_cardano_address():
    enterprise = "addr1vx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzers66hrl8"
    icarus = "Ae2tdPwUPEZBrFkSj7HEsHBm4Nb1hV3tDV8ajYz8SriLJqYLCVHcwrQLnN2"
    assert rre.cardano_address(f"{enterprise[:-1]}9") == []
    assert rre.cardano_address(f"{enterprise}q") == []
    assert rre.cardano_address(f"x{enterprise}") == []
    assert rre.cardano_address(enterprise.upper()) == []
    assert rre.cardano_address(f"{icarus[:-1]}3") == []
    assert rre.cardano_address("stake_test1uqehkck0lajq8gr28t9uxnuvgcqrc6070x3k9r8048z8y5gssrtvn") == []


def test_hard_cosmos_address():
    atom = "cosmos12wtuazg5tjtcutw29saqeeuu697xt48cgq3hmh"
    assert rre.cosmos_address(f"{atom[:-1]}j") == []
    assert rre.cosmos_address(atom[:-1]) == []
    assert rre.cosmos_address(f"{atom}q") == []
    assert rre.cosmos_address(f"x{atom}") == []
    # a chain not in the list, capitals, 19 bytes (made up)
    assert rre.cosmos_address("band1vhc4e687ufdjfpz9amwx8nv6sgy5udvksdnp7c") == []
    assert rre.cosmos_address(atom.upper()) == []
    assert rre.cosmos_address("cosmos1vw5cxxxyzkl4kqxfmpn7gyy6nkw2lqsd88c2l") == []


def test_hard_dash_address():
    x = "XgNSWgGvrWBeJpBKbJyDpRJL2q1DofCwz2"
    assert rre.dash_address(f"{x[:-1]}3") == []
    assert rre.dash_address(x[:-1]) == []
    assert rre.dash_address(f"{x}z") == []
    assert rre.dash_address(f"a{x}") == []
    assert rre.dash_address("XH2qXZye9KimVP3EZtduLJ2YQKkH8GxDah") == []
    assert rre.dash_address("DD4KSSuBJqcjuTcvUg1CgUKeurPUFeEZkE") == []


def test_hard_dogecoin_address():
    # made up: base58check with Dogecoin's version bytes 30 (D...) and 22 (A...)
    assert rre.dogecoin_address("DHQ6wcyQf6Vx4bWFZMFyPLL9KaXzt3pUdi") == ["DHQ6wcyQf6Vx4bWFZMFyPLL9KaXzt3pUdi"]
    assert rre.dogecoin_address("dogecoin:DN5wR3x5nnXUyeN3NQvCyUrdNXJJotKHbo?amount=100") == [
        "DN5wR3x5nnXUyeN3NQvCyUrdNXJJotKHbo"]
    assert rre.dogecoin_address('("DFf83qnszeEwLRB2UuGjvzWwn9nDbZ15Yv")') == ["DFf83qnszeEwLRB2UuGjvzWwn9nDbZ15Yv"]
    assert rre.dogecoin_address("P2SH A8XG9519LtzsoPL3fZ5zByJEMDPW8u1GFi.") == ["A8XG9519LtzsoPL3fZ5zByJEMDPW8u1GFi"]
    # checksum broken, a character short and one too many, glued to a word
    assert rre.dogecoin_address("DHQ6wcyQf6Vx4bWFZMFyPLL9KaXzt3pUdj") == []
    assert rre.dogecoin_address("DHQ6wcyQf6Vx4bWFZMFyPLL9KaXzt3pUd") == []
    assert rre.dogecoin_address("DHQ6wcyQf6Vx4bWFZMFyPLL9KaXzt3pUdiz") == []
    assert rre.dogecoin_address("xDHQ6wcyQf6Vx4bWFZMFyPLL9KaXzt3pUdi") == []
    # Dash and Litecoin addresses
    assert rre.dogecoin_address("XgNSWgGvrWBeJpBKbJyDpRJL2q1DofCwz2") == []
    assert rre.dogecoin_address("LKDyUEtTR1HXamkiEphisSiBJu6o3ZPE34") == []


def test_hard_ens_name():
    assert rre.ens_name("JANE-EXAMPLE.ETH") == ["JANE-EXAMPLE.ETH"]
    assert rre.ens_name("https://app.ens.domains/jane-example.eth") == ["jane-example.eth"]
    assert rre.ens_name('{"ens": "wallet.jane-example.eth"}') == ["wallet.jane-example.eth"]
    assert rre.ens_name("(test-name.eth)") == ["test-name.eth"]
    assert rre.ens_name("send 1 ETH to my-test-wallet.eth.") == ["my-test-wallet.eth"]
    # too short, a longer name, a longer domain, glued or hyphenated, an amount, an interface
    assert rre.ens_name("ab.eth") == []
    assert rre.ens_name("jane-example.ethereum") == []
    assert rre.ens_name("jane-example.eth.io") == []
    assert rre.ens_name("jane-example.eth2") == []
    assert rre.ens_name("jane-example.eth-wallet") == []
    assert rre.ens_name("0.5 ETH") == []
    assert rre.ens_name("eth0") == []


def test_hard_ethereum_address():
    # EIP-55's test vectors: checksummed, all capitals, all lower case
    assert rre.ethereum_address("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed") == [
        "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed"]
    assert rre.ethereum_address("send to 0x52908400098527886E0F7030069857D2E4169EE7.") == [
        "0x52908400098527886E0F7030069857D2E4169EE7"]
    assert rre.ethereum_address('{"to": "0xde709f2102306220921060314715629080e2fb77"}') == [
        "0xde709f2102306220921060314715629080e2fb77"]
    assert rre.ethereum_address("https://etherscan.io/address/0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359") == [
        "0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359"]
    assert rre.ethereum_address("ethereum:0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB@1?value=1e18") == [
        "0xdbF03B407c01E7cD3CBea99509d93f8DDDC8C6FB"]
    assert rre.ethereum_address("(0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb)") == [
        "0xD1220A0cf47c7B9Be7A2E6BA89F429762e7b9aDb"]
    # 39 and 41 hexadecimal characters, a capital X, glued to a word, a g, no 0x, a transaction hash
    assert rre.ethereum_address("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAe") == []
    assert rre.ethereum_address("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed0") == []
    assert rre.ethereum_address("0X5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed") == []
    assert rre.ethereum_address("x0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed") == []
    assert rre.ethereum_address("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAeg") == []
    assert rre.ethereum_address("5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed") == []
    assert rre.ethereum_address("0xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f836") == []


def test_hard_ethereum_private_key():
    key = "d0fca5a191812186c0c178b719ae2c9e302b76c960e35b809e4c97c13f04eaef"
    assert rre.ethereum_private_key(f"private key: {key[:-1]}") == []
    assert rre.ethereum_private_key(f"privatekey{key}") == []


def test_hard_ethereum_tx_hash():
    # made up: SHA-256 hashes
    assert rre.ethereum_tx_hash("0xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f836") == [
        "0xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f836"]
    assert rre.ethereum_tx_hash("TxHash: 0x4FA3D8AA4D8582537E3FF385355C494928FC804FB29C02A3B99D5B266D9E62A9.") == [
        "0x4FA3D8AA4D8582537E3FF385355C494928FC804FB29C02A3B99D5B266D9E62A9"]
    assert rre.ethereum_tx_hash('{"hash": "0xf97420622c43047e0bc7a78508b428433abdbccf3472261a27833a544c84958f"}') == [
        "0xf97420622c43047e0bc7a78508b428433abdbccf3472261a27833a544c84958f"]
    tx = "0x501f1325e408e050a9b9de906ae5b73dce16c3c941661f1460d86cc42302db35"
    assert rre.ethereum_tx_hash(f"https://bscscan.com/tx/{tx}") == [
        "0x501f1325e408e050a9b9de906ae5b73dce16c3c941661f1460d86cc42302db35"]
    assert rre.ethereum_tx_hash("(0x9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08)") == [
        "0x9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"]
    # 63 and 65 hexadecimal characters, no 0x, a capital X, glued to a word, a g, an address
    assert rre.ethereum_tx_hash("0xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f83") == []
    assert rre.ethereum_tx_hash("0xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f8360") == []
    assert rre.ethereum_tx_hash("db81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f836") == []
    assert rre.ethereum_tx_hash("0Xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f836") == []
    assert rre.ethereum_tx_hash("x0xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f836") == []
    assert rre.ethereum_tx_hash("0xdb81d4496495cab5461493206bec8cd38aba7eb0823ff69c8c5842750ed6f83g") == []
    assert rre.ethereum_tx_hash("0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed") == []


def test_hard_lightning_invoice():
    assert rre.lightning_invoice(_LN_COFFEE[:-1]) == []
    assert rre.lightning_invoice(_LN_COFFEE.replace("lnbc", "lntb")) == []
    assert rre.lightning_invoice(f"x{_LN_COFFEE}") == []
    # mixed case (BIP173: one case only)
    assert rre.lightning_invoice(_LN_COFFEE[:100] + _LN_COFFEE[100:].upper()) == []


def test_hard_lnurl():
    jane = "LNURL1DP68GURN8GHJ7ETCV9KHQMR99E3K7MF0D3H82UNVWQHK5CTWV5ZSTSSD"
    assert rre.lnurl(f"{jane[:-1]}A") == []
    assert rre.lnurl(jane[:-1]) == []
    assert rre.lnurl(f"x{jane}") == []
    assert rre.lnurl(jane[:20].lower() + jane[20:]) == []
    assert rre.lnurl("lnurlp://example.com/lnurlp/jane") == []
    # too short (made up: https://a.b/x), a Lightning address
    assert rre.lnurl("lnurl1dp68gurn8ghj7cfwvghhsaf9qy6") == []
    assert rre.lnurl("jane@example.com") == []


def test_hard_monero_address():
    # made up: network byte 18, two SHA-256 keys and their Keccak checksum, in Monero's base58
    a = "44Mo2kWL4BC4TFKyAn8g3oZ6zPbzhNuL2fVAoT5XbUKG1pfjL7xbdnhNWJ1CLmxQqJ9YLqazSv9d1GwXAREAg3L9FjKNhbq"
    b = "464JSa4jdhkd7dCKginZhaJSVWUmkUARb6uwyPtwv1vE85xvRDm6yZBCxCQ5p4DSLWAcjJ9M9Sqvz2upp4e3mmiUPGxXyMC"
    c = "4A5w4dc1yGYDLKUJqAVXaLf7Eb1JmuouPU2a9zH25Xca9mKSvDzuN16CdGCLgVG228iEbYX4CTdZQVn93c9LZ7uHNBuXuBD"
    assert rre.monero_address(a) == [a]
    assert rre.monero_address(f"monero:{b}?tx_amount=0.5") == [b]
    assert rre.monero_address(f'{{"address": "{c}"}}') == [c]
    assert rre.monero_address(f"XMR ({a}).") == [a]
    assert rre.monero_address(f"{b}\n{c}") == [b, c]
    assert rre.monero_address(f"https://xmrchain.net/search?value={c}") == [c]
    # a character short and one too many, glued to a word, a 0 (not base58), a C after the 4
    assert rre.monero_address(a[:-1]) == []
    assert rre.monero_address(a + "z") == []
    assert rre.monero_address("x" + a) == []
    assert rre.monero_address(a[:-1] + "0") == []
    assert rre.monero_address("4C" + a[2:]) == []
    # a subaddress (8...), not a standard address
    assert rre.monero_address("8C23aeHFungHWPKQr2xTfEWBFpr8tF2Ln4iae8DPSJc7RpAiXjCC7iqJ9LjzWbfpc5NgaEyxMYhNS5MuBYi7cL"
                              "ePPwNi2pp") == []


def test_hard_nostr_key():
    # made up: bech32 of SHA-256 bytes
    npub = "npub1vd3jgslwfkd6k4lkddwxfdev8qtuepyvfe8jmsj08hem6mmzzhdqzjfpwz"
    nsec = "nsec1mzn8laszya97jjrmxldryklqn822n8l9sk9aazraem44snja929swcxgw4"
    note = "note1tvuvxkaaudgmlq9y0k8hlhjan468738q4jmnh6kpp8pupuhfmgrqw4mnz4"
    assert rre.nostr_key(f'{{"pubkey": "{npub}"}}') == [npub]
    assert rre.nostr_key(f"https://primal.net/e/{note}") == [note]
    assert rre.nostr_key(f"backup: {nsec.upper()}.") == [nsec.upper()]
    # checksum broken, a character short and one too many, glued to a word, prefixes swapped, mixed case
    assert rre.nostr_key(npub[:-1] + "x") == []
    assert rre.nostr_key(npub[:-1]) == []
    assert rre.nostr_key(npub + "q") == []
    assert rre.nostr_key("x" + npub) == []
    assert rre.nostr_key("nsec" + npub[4:]) == []
    assert rre.nostr_key(npub[:20] + npub[20:].upper()) == []


def test_hard_polkadot_address():
    alice = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
    assert rre.polkadot_address(f"{alice[:-1]}R") == []
    assert rre.polkadot_address(alice[:-1]) == []
    assert rre.polkadot_address(f"{alice}z") == []
    assert rre.polkadot_address(f"x{alice}") == []
    assert rre.polkadot_address("5NecBZmeUHQKB9fT4PVSC7mribMBHbvLZbFep5FgG8rpCNS2") == []
    assert rre.polkadot_address("QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG") == []


def test_hard_solana_address():
    a, b = "1thX6LZfHDZZKUs92febYZhYRcXddmzfzF2NvTkPNE", "4XtRjD178mXbpmAk1LJGb5cJewxaaZtMw7QknyM79kT4"
    assert rre.solana_address(f"Phantom wallet {a}") == [f"Phantom wallet {a}"]
    assert rre.solana_address(f"SOLANA:\n{b}") == [f"SOLANA:\n{b}"]
    # the keyword inside a longer word, no keyword
    assert rre.solana_address(f"solution {b}") == []
    assert rre.solana_address(f"parasol {b}") == []
    assert rre.solana_address(b) == []
    # a character short of 32, one too many after 44, the keyword more than 30 characters away
    assert rre.solana_address(f"sol {a[:31]}") == []
    assert rre.solana_address(f"sol {b}z") == []
    assert rre.solana_address(f"solana is the chain where my old wallet lives: {b}") == []
    # an Ethereum and a Bitcoin address
    assert rre.solana_address("sol 0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed") == []
    assert rre.solana_address("sol 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == []


def test_hard_stellar_address():
    account = "GA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJVSGZ"
    assert rre.stellar_address(account[:-1] + "A") == []
    assert rre.stellar_address(account[:-1]) == []
    assert rre.stellar_address(account + "A") == []
    assert rre.stellar_address("X" + account) == []
    assert rre.stellar_address(account.lower()) == []
    assert rre.stellar_address("SAVZRUGOTOS4Q6B43XJVUTEXELB4VY3ZQKFS3QEVMA55JSZKGPSDCJRP") == []


def test_hard_ton_address():
    eq = "EQBE-sdHHG9Kz_4osTNj27fVJTLelI8ReGdXSff3npQU22f3"
    assert rre.ton_address(eq[:-1] + "4") == []
    assert rre.ton_address(eq[:-1]) == []
    assert rre.ton_address(eq + "A") == []
    assert rre.ton_address("x" + eq) == []
    assert rre.ton_address("kQAvSRzMdgyurt69rbMA5KzEocn-LLnvqcEUMZwHKuyiUvpB") == []
    assert rre.ton_address(eq.lower()) == []


def test_hard_xrp_address():
    # made up: Ripple base58check of version 0 and SHA-256 bytes
    x0, x1, x2 = ("rHbo2MaEr3nx8UeUHj11g5WP2vDftKgLuL", "rfX6ek5yZFXqPme1Xy1RUWAmCbSgcA59bn",
                  "rL7LkTDPDHjQg6nZ6TpDmgo5xhaA4K7m9N")
    assert rre.xrp_address(f"XRP: {x0}, destination tag 12345") == [x0]
    assert rre.xrp_address(f'{{"Account": "{x1}"}}') == [x1]
    assert rre.xrp_address(f"https://xrpscan.com/account/{x2}") == [x2]
    assert rre.xrp_address(f"({x0})\n{x1}.") == [x0, x1]
    assert rre.xrp_address(f"ripple:{x2}?amount=25") == [x2]
    # checksum broken, a character short and one too many, glued to a word
    assert rre.xrp_address(x0[:-1] + "M") == []
    assert rre.xrp_address(x0[:-1]) == []
    assert rre.xrp_address(x0 + "r") == []
    assert rre.xrp_address("x" + x0) == []
    # made up: valid base58check of 24 bytes; an X-address; a Bitcoin address
    assert rre.xrp_address("rhFEPSS3ofHF3iy8zxGVj3pdRYbhfmyij") == []
    assert rre.xrp_address("XVLhHMPHU98es4dbozjVtdWzVrDjtV8xvjGQTYPiAx6gwDC") == []
    assert rre.xrp_address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == []


def test_hard_zcash_address():
    t1 = "t1gzrYQxjzxY84DdGQA47sHB3vHrKCxtkqa"
    zs = "zs1nac2pzuuxsjvkvuqfnjy8pdhrf4068dcglhk8khzyzht8sa3up29mp0fdtjk0ft3faghk6z5xm4"
    assert rre.zcash_address(t1[:-1] + "b") == []
    assert rre.zcash_address(t1[:-1]) == []
    assert rre.zcash_address(t1 + "z") == []
    assert rre.zcash_address("x" + t1) == []
    assert rre.zcash_address(zs[:-1] + "5") == []
    assert rre.zcash_address(zs.upper()) == []


def test_hard_ids_finance_crypto_regexes_stay_fast():
    # 100 KB runs of each changed regex's prefixes and shapes, many of which reach the validator
    start = time.perf_counter()
    for text in ('4111 ' * 20000, '4111 1111 1111 1111 ' * 5000, '3782 822463 ' * 8333, 'BE68 5390 0754 7034 ' * 5000,
                 'RF18 ' * 20000, ('RF18' + 'A' * 21 + ' ') * 3846, 'Euro 2024 ' * 10000, 'eth0 ' * 20000,
                 '1 000 ' * 16667,
                 ('bc1q' + 'q' * 38 + ' ') * 2325, ('BC1Q' + 'Q' * 38 + ' ') * 2325, ('1' + 'A' * 33 + ' ') * 2857,
                 ('L' + 'z' * 33 + ' ') * 2857, ('T' + 'R' * 33 + ' ') * 2857, ('5' + 'H' * 50 + ' ') * 1960,
                 ('r' + 'H' * 33 + ' ') * 2857, 'steam ABCDE-' * 8333, 'paysafecard 1234 ' * 5882, 'EORI NL' * 14286,
                 'payconiq.com/pay/2/' + 'a' * 99981, 'paypal.me/my/' * 7692, ';4111111111111111=2512' * 4545,
                 'lnbc1' * 20000, 'npub1q' * 16667):
        for name in ('credit_card', 'iban', 'rf_creditor_reference', 'currency_amount', 'bitcoin_address',
                     'litecoin_address', 'tron_address', 'bitcoin_private_key', 'xrp_address', 'gift_card_code',
                     'eori_number', 'payconiq_link', 'paypal_me_link', 'card_track_data', 'lightning_invoice', 'lnurl',
                     'nostr_key'):
            getattr(rre, name)(text)
    assert time.perf_counter() - start < 2


# hardened tests: one near-miss or look-alike per call, all values made up or documented examples

def test_hard_android_app_data_path():
    for path in (
        "/storage/1A2B-3C4D/Android/data/com.example.app/files/x.jpg",
        "/storage/self/primary/Android/data/com.example.app/cache",
        "/mnt/sdcard/Android/obb/com.example.game/main.1.com.example.game.obb",
    ):
        assert rre.android_app_data_path(path) == [path]
    # a path at the end of a line: the newline is left out
    assert rre.android_app_data_path("/data/user/0/com.example.app\n") == ["/data/user/0/com.example.app"]
    # four-digit user, a lowercase SD card ID, a folder next to data
    assert rre.android_app_data_path("/data/user/1234/com.example.app/x") == []
    assert rre.android_app_data_path("/storage/1a2b-3c4d/Android/data/com.example.app/x") == []
    assert rre.android_app_data_path("/storage/emulated/0/Android/datax/com.example.app/x") == []

def test_hard_android_id():
    assert rre.android_id('{"android_id": "3f2b9c71d04e8a65"}') == ['android_id": "3f2b9c71d04e8a65']
    assert rre.android_id("D/Example: androidId=3F2B9C71D04E8A65") == ["androidId=3F2B9C71D04E8A65"]
    assert rre.android_id("SSAID: 1a2b3c4d5e6f7a8b") == ["SSAID: 1a2b3c4d5e6f7a8b"]
    assert rre.android_id("device (ANDROID-ID 3f2b9c71d04e8a65).") == ["ANDROID-ID 3f2b9c71d04e8a65"]
    assert rre.android_id("$ settings get secure android_id\n1a2b3c4d5e6f7a8b\n") == ["android_id\n1a2b3c4d5e6f7a8b"]
    # leading zeros dropped: 13 digits
    assert rre.android_id("Android ID: 1a2b3c4d5e6f7") == ["Android ID: 1a2b3c4d5e6f7"]
    # 12 digits, keyword inside a word or longer, a UUID, not hex, glued, no keyword, keyword too far away
    assert rre.android_id("Android ID: 3f2b9c71d04e") == []
    assert rre.android_id("myandroid_id: 3f2b9c71d04e8a65") == []
    assert rre.android_id("android_identifier: 3f2b9c71d04e8a65") == []
    assert rre.android_id("android_id: 550e8400-e29b-41d4-a716-446655440000") == []
    assert rre.android_id("Android ID: 3f2b9c71d04e8a6g") == []
    assert rre.android_id("Android ID 3f2b9c71d04e8a65_x") == []
    assert rre.android_id("device 3f2b9c71d04e8a65") == []
    assert rre.android_id("Android ID: - - - 3f2b9c71d04e8a65") == []

def test_hard_android_system_path():
    for path in ("/odm/etc/x.xml", "/oem/media/audio/notification.ogg", "/system_root/system/build.prop",
                 "/system/app/Example/Example.apk"):
        assert rre.android_system_path(path) == [path]
    # the folder itself, a leading space, Windows separators, a vendor folder elsewhere, iOS's /System
    for path in ("/vendor", " /system/x", "C:\\system\\x", "/mnt/vendor/persist/x", "/systemx/x"):
        assert rre.android_system_path(path) == []

def test_hard_api_key():
    google = "AIza" + "Sy" + "A1b2C3d4E5" * 3 + "f6G"
    assert rre.api_key(f"GOOGLE_API_KEY={google}") == [google]
    pat = "github_pat_" + "11ABCDEFG0" * 2 + "ab_" + "A1b2C3d4E5f6" * 4 + "A1b2C3d4E5f"
    assert rre.api_key(f'{{"token": "{pat}"}}') == [pat]
    gitlab = "glpat-" + "a1B2c3D4e5F6g7H8i9J0"
    assert rre.api_key(f"git clone https://oauth2:{gitlab}@gitlab.example.com/x.git") == [gitlab]
    npm = "npm_" + "a1B2c3D4e5" * 3 + "f6G7h8"
    assert rre.api_key(f"//registry.npmjs.org/:_authToken={npm}\n") == [npm]
    hf = "hf_" + "abcdefghij" * 3 + "abcd"
    assert rre.api_key(f"(token {hf})") == [hf]
    do = "dop_v1_" + "0123456789abcdef" * 4
    assert rre.api_key(f"export DIGITALOCEAN_TOKEN='{do}'") == [do]
    stripe = "rk_" + "live_" + "a1B2c3D4e5F6g7H8i9J0"
    assert rre.api_key(stripe) == [stripe]
    openai = "sk-proj-" + "a1B2c3D4e5" * 2 + "T3BlbkFJ" + "a1B2c3D4e5" * 2
    assert rre.api_key(f"OPENAI_API_KEY: {openai}.") == [openai]
    sendgrid = "SG." + "a1B2c3D4e5F6g7H8i9J0k1" + "." + "a1B2c3D4e5F6g7H8i9J0k" * 2 + "L"
    assert rre.api_key(f"apikey {sendgrid}") == [sendgrid]
    # a publishable Stripe key, one character too many or too few, glued, lowercase, a short Telegram secret
    assert rre.api_key("pk_" + "live_" + "a1B2c3D4e5F6g7H8i9J0") == []
    assert rre.api_key("AKIAIOSFODNN7EXAMPLEX") == []
    assert rre.api_key("xAKIAIOSFODNN7EXAMPLE") == []
    assert rre.api_key("akiaiosfodnn7example") == []
    assert rre.api_key(hf[:-1]) == []
    assert rre.api_key(google[:-1]) == []
    assert rre.api_key(npm + "i") == []
    assert rre.api_key(do.upper().replace("DOP_V1_", "dop_v1_")) == []
    assert rre.api_key("12345678:AA" + "b" * 32) == []
    # look-alikes: an OpenAI-style key without its marker, a UUID
    assert rre.api_key("sk-" + "a" * 40 + " 550e8400-e29b-41d4-a716-446655440000") == []

def test_hard_app_cache_path():
    for path in ("/private/var/mobile/Library/Caches/com.example.app/x.db",
                 "/data/data/com.example.app/files/.cache/x"):
        assert rre.app_cache_path(path) == [path]
    # Android's code_cache, a folder starting with cache, Windows separators
    assert rre.app_cache_path("/data/data/com.example.app/code_cache/x") == []
    assert rre.app_cache_path("/data/data/com.example.app/cache_x/y") == []
    assert rre.app_cache_path("\\data\\cache\\x") == []

def test_hard_app_package_name():
    assert rre.app_package_name("io.github.example") == ["io.github.example"]
    assert rre.app_package_name("installed: jp.example.line.android,") == ["jp.example.line.android"]
    assert rre.app_package_name("https://play.google.com/store/apps/details?id=org.example.app&hl=en") == [
        "org.example.app"]
    assert rre.app_package_name("Preferences/group.com.example.app.plist") == ["group.com.example.app"]
    assert rre.app_package_name('{"bundleId": "net.example.ExampleApp"}') == ["net.example.ExampleApp"]
    assert rre.app_package_name("(com.example)") == ["com.example"]
    # web addresses, a country's second level, file names, a version, an e-mail domain, words joined by dots
    for text in ("www.example.com", "en.wikipedia.org", "ec.europa.eu", "app.example.io", "com.au", "my.cv.pdf",
                 "report.final.docx", "v2.0.1", "jane@com.example", "il.fait.beau", "it.Then"):
        assert rre.app_package_name(text) == []

def test_hard_apple_ecid():
    # ideviceinfo's XML output
    assert rre.apple_ecid("<key>UniqueChipID</key>\n\t<integer>460367961908983</integer>") == [
        "UniqueChipID</key>\n\t<integer>460367961908983"]
    assert rre.apple_ecid("ECID = 0x1A2B3C4D5E6F7;") == ["ECID = 0x1A2B3C4D5E6F7"]
    assert rre.apple_ecid("ecid:001A2B3C4D5E802E") == ["ecid:001A2B3C4D5E802E"]
    assert rre.apple_ecid("Unique Chip ID: 12345678901234567890") == ["Unique Chip ID: 12345678901234567890"]
    assert rre.apple_ecid("(ECID 0x1a2b3c4d5e6f7)") == ["ECID 0x1a2b3c4d5e6f7"]
    # too short after 0x, too short in decimal, glued, too long, keyword inside a word, 17 hex digits, too far away
    assert rre.apple_ecid("ECID: 0x12345") == []
    assert rre.apple_ecid("ECID: 123456789") == []
    assert rre.apple_ecid("ECID: 0x1A2B3C4D5E6F7G") == []
    assert rre.apple_ecid("ECID: 123456789012345678901") == []
    assert rre.apple_ecid("myecid: 0x1A2B3C4D5E6F7") == []
    assert rre.apple_ecid("ECID: 0x1A2B3C4D5E6F7A8B9") == []
    assert rre.apple_ecid("ECID - - - - 0x1A2B3C4D5E6F7") == []
    assert rre.apple_ecid("<key>UniqueChipID</key><string>Example</string>") == []

def test_hard_apple_serial_number():
    assert rre.apple_serial_number("SN: C02XL0GHJGH5") == ["SN: C02XL0GHJGH5"]
    assert rre.apple_serial_number("Seriennummer: C02XL0GHJGH5") == ["Seriennummer: C02XL0GHJGH5"]
    assert rre.apple_serial_number("numer seryjny: C02XL0GHJGH5") == ["numer seryjny: C02XL0GHJGH5"]
    assert rre.apple_serial_number('{"serialNumber":"C02XL0GHJGH5"}') == ['serialNumber":"C02XL0GHJGH5']
    # no keyword, digits or letters only, no year letter in 4th place, Spanish s/n, too long, lowercase, too short
    assert rre.apple_serial_number("C02XL0GHJGH5") == []
    assert rre.apple_serial_number("Serial: 12345678901") == []
    assert rre.apple_serial_number("serial ABCDEFGHJK") == []
    assert rre.apple_serial_number("Serial C02AL0GHJGH5") == []
    assert rre.apple_serial_number("Calle Mayor s/n 28001") == []
    assert rre.apple_serial_number("Serial Number: C02XL0GHJGH5X") == []
    assert rre.apple_serial_number("Serial Number: c02xl0ghjgh5") == []
    assert rre.apple_serial_number("Serial Number C02XL0GHJ") == []

def test_hard_bitlocker_recovery_key():
    # made up: every block is a 16-bit number times 11
    key = "011011-022022-033033-044044-055055-066066-077077-088088"
    assert rre.bitlocker_recovery_key(key) == [key]
    assert rre.bitlocker_recovery_key(f"laptop-01,{key},2026-03-02") == [key]
    manage_bde = ("    Numerical Password:\n      ID: {0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D}\n"
                  f"      Password:\n        {key}\n")
    assert rre.bitlocker_recovery_key(manage_bde) == [key]
    assert rre.bitlocker_recovery_key(f"[{key}]") == [key]

def test_hard_camera_filename():
    for name in ("MVIMG_20260302_081512.jpg", "PANO_20260302_081512.jpg", "GH010001.MP4", "MVI_1234.MOV",
                 "_DSC1234.ARW", "DSCF1234.RAF"):
        assert rre.camera_filename(name) == [name]
    assert rre.camera_filename('see "IMG_0001.JPG",') == ["IMG_0001.JPG"]
    # WhatsApp and screenshot names, an impossible date or hour, another file with a date, no or another extension,
    # three or six digits, glued to a letter
    for name in ("IMG-20260303-WA0007.jpg", "Screenshot_20260302_081512.png", "IMG_20261302_081512.jpg",
                 "IMG_20260302_251512.jpg", "backup_20260302_081512.jpg", "IMG_0001", "IMG_0001.txt", "IMG_001.JPG",
                 "DSC012345.JPG", "XIMG_0001.JPG"):
        assert rre.camera_filename(name) == []

def test_hard_ios_app_container_path():
    guid = "0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"
    path = f"/private/var/mobile/Containers/Data/Application/{guid}/Library/Preferences/x.plist"
    assert rre.ios_app_container_path(path) == [path]
    assert rre.ios_app_container_path(f"/private/var/mobile/Containers/Shared/AppGroup/{guid.upper()}") == [
        f"/private/var/mobile/Containers/Shared/AppGroup/{guid.upper()}"]
    # one digit short, lowercase folder, a GUID in braces, a Windows path, glued, on the next line
    assert rre.ios_app_container_path(f"/private/var/mobile/Containers/Data/Application/{guid[:-1]}/x") == []
    assert rre.ios_app_container_path(f"/private/var/mobile/Containers/Data/application/{guid}/x") == []
    assert rre.ios_app_container_path(f"/private/var/mobile/Containers/Data/Application/{{{guid}}}/x") == []
    assert rre.ios_app_container_path(f"C:\\Users\\x\\{guid}") == []
    assert rre.ios_app_container_path(f"/private/var/mobile/Containers/Data/Application/{guid}x/x") == []
    assert rre.ios_app_container_path(f"\n/private/var/mobile/Containers/Data/Application/{guid}/x") == []

def test_hard_ios_udid():
    old = "0A1B2C3D4E" * 4
    assert rre.ios_udid(f'"UDID": "{old}"') == [f'UDID": "{old}']
    assert rre.ios_udid(f"Target Identifier: {old.lower()}") == [f"Target Identifier: {old.lower()}"]
    assert rre.ios_udid("UniqueDeviceID: 00008101-000A1B2C3D4E5F6A") == ["00008101-000A1B2C3D4E5F6A"]
    # an iTunes backup's folder
    assert rre.ios_udid("/MobileSync/Backup/00008030-001A2B3C4D5E802E/Manifest.db") == ["00008030-001A2B3C4D5E802E"]
    assert rre.ios_udid("(00008101-000a1b2c3d4e5f6a)") == ["00008101-000a1b2c3d4e5f6a"]
    # 39 and 41 hex, an ECID one short or long, a chip ID not starting with 0000, glued, a UUID after the keyword
    assert rre.ios_udid(f"UDID: {old[:-1]}") == []
    assert rre.ios_udid(f"UDID: {old}5") == []
    assert rre.ios_udid("00008030-001A2B3C4D5E802") == []
    assert rre.ios_udid("00008030-001A2B3C4D5E802EF") == []
    assert rre.ios_udid("10008030-001A2B3C4D5E802E") == []
    assert rre.ios_udid("x00008030-001A2B3C4D5E802E") == []
    assert rre.ios_udid("UDID: 550e8400-e29b-41d4-a716-446655440000") == []

# the example token of jwt.io
JWT_IO = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
          ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")

def test_hard_jwt():
    assert rre.jwt(f'{{"access_token":"{JWT_IO}","token_type":"Bearer"}}') == [JWT_IO]
    assert rre.jwt(f"Set-Cookie: session={JWT_IO}; HttpOnly") == [JWT_IO]
    assert rre.jwt(f"https://example.com/cb#id_token={JWT_IO}&state=xyz") == [JWT_IO]
    assert rre.jwt(f"{JWT_IO}.") == [JWT_IO]
    # made up: {"alg":"RS256","kid":"k1"} and {"sub":"jane","exp":1893456000}
    rs = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImsxIn0.eyJzdWIiOiJqYW5lIiwiZXhwIjoxODkzNDU2MDAwfQ.c2lnbmF0dXJl"
    assert rre.jwt(f"token: {rs}") == [rs]
    # the signature is base64url: a letter outside ASCII after it is not part of it
    assert rre.jwt(f"{JWT_IO}é") == [JWT_IO]
    payload = JWT_IO.split(".")[1]
    # a header without alg ({"typ":"JWT"}), a header that is not JSON, a payload that is not an object ({}), glued,
    # no second dot, the header alone
    assert rre.jwt(f"eyJ0eXAiOiJKV1QifQ.{payload}.sig") == []
    assert rre.jwt(f"eyJub3QganNvbg.{payload}.sig") == []
    assert rre.jwt("eyJhbGciOiJIUzI1NiJ9.e30.sig") == []
    assert rre.jwt(f"x{JWT_IO}") == []
    assert rre.jwt(JWT_IO.rpartition(".")[0]) == []
    assert rre.jwt("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9") == []

def test_hard_md5():
    # made up: the MD5 of "example 1", "example 2" ...
    assert rre.md5("E93B3FA481BE3932AA08BD68C3DEEE70") == ["E93B3FA481BE3932AA08BD68C3DEEE70"]
    assert rre.md5("a6b23ee7f9c084154997ea3bf5b4c1e3  example.txt") == ["a6b23ee7f9c084154997ea3bf5b4c1e3"]
    assert rre.md5("MD5 (example.txt) = d376eaa7e7aecf81dcbdd6081fae63a9") == ["d376eaa7e7aecf81dcbdd6081fae63a9"]
    assert rre.md5('{"md5": "4aea863c087aa212286b14c7e0da99d1"}') == ["4aea863c087aa212286b14c7e0da99d1"]
    assert rre.md5("(e93b3fa481be3932aa08bd68c3deee70).") == ["e93b3fa481be3932aa08bd68c3deee70"]
    assert rre.md5("/thumbs/a6b23ee7f9c084154997ea3bf5b4c1e3/x.jpg") == ["a6b23ee7f9c084154997ea3bf5b4c1e3"]
    # one short or long, not hex, glued, after 0x, digits only (an eSIM EID), filler
    assert rre.md5("e93b3fa481be3932aa08bd68c3deee7") == []
    assert rre.md5("e93b3fa481be3932aa08bd68c3deee700") == []
    assert rre.md5("g93b3fa481be3932aa08bd68c3deee70") == []
    assert rre.md5("e93b3fa481be3932aa08bd68c3deee70_thumb.jpg") == []
    assert rre.md5("0xe93b3fa481be3932aa08bd68c3deee70") == []
    assert rre.md5('"eid": "89049032123451234512345678901224"') == []
    assert rre.md5("0" * 32 + " " + "f" * 32) == []
    # look-alikes: a SHA-1, a UUID
    assert rre.md5("f1f0188d7e74ce2e9b395726ee39848bcd92e869 550e8400-e29b-41d4-a716-446655440000") == []

def test_hard_sha1():
    # made up: the SHA-1 of "example 1", "example 2" ...
    assert rre.sha1("commit f1f0188d7e74ce2e9b395726ee39848bcd92e869\nAuthor: Jane") == [
        "f1f0188d7e74ce2e9b395726ee39848bcd92e869"]
    assert rre.sha1("D92D43A269B89A3E6A10CECD829C3B7D4F6170A5") == ["D92D43A269B89A3E6A10CECD829C3B7D4F6170A5"]
    assert rre.sha1("347483f6dc78ac4ca9a8f254b46a602c1f905de4  example.txt") == [
        "347483f6dc78ac4ca9a8f254b46a602c1f905de4"]
    assert rre.sha1('{"sha1":"a6c03da7b4c56d07cd0309c57963be0de6da2bf2"}') == ["a6c03da7b4c56d07cd0309c57963be0de6da2bf2"]
    assert rre.sha1("(f1f0188d7e74ce2e9b395726ee39848bcd92e869).") == ["f1f0188d7e74ce2e9b395726ee39848bcd92e869"]
    assert rre.sha1("SHA1 Fingerprint=d92d43a269b89a3e6a10cecd829c3b7d4f6170a5") == [
        "d92d43a269b89a3e6a10cecd829c3b7d4f6170a5"]
    # one short or long, not hex, glued, digits only, filler, an Ethereum address (0x), an MD5
    assert rre.sha1("f1f0188d7e74ce2e9b395726ee39848bcd92e86") == []
    assert rre.sha1("f1f0188d7e74ce2e9b395726ee39848bcd92e8690") == []
    assert rre.sha1("f1f0188d7e74ce2e9b395726ee39848bcd92e86z") == []
    assert rre.sha1("xf1f0188d7e74ce2e9b395726ee39848bcd92e869") == []
    assert rre.sha1("1234567890" * 4) == []
    assert rre.sha1("a" * 40) == []
    assert rre.sha1("0xf1f0188d7e74ce2e9b395726ee39848bcd92e869") == []
    assert rre.sha1("e93b3fa481be3932aa08bd68c3deee70") == []

def test_hard_sha256():
    # made up: the SHA-256 of "example 1" and "example 2"
    sha = "8ee89711330c1ccf39a2e65ad12bbd7df4a4a2ee857f53b4823f00fecb7bd252"
    other = "553295e4b848bee781c30a0c86a5b731330806eaaca214de195e48761b8a61ee"
    assert rre.sha256(f"{sha}  example.txt") == [sha]
    assert rre.sha256(f"SHA256          {other.upper()}       C:\\x.txt") == [other.upper()]
    assert rre.sha256(f"image@sha256:{sha}") == [sha]
    assert rre.sha256(f'{{"sha256": "{other}"}}') == [other]
    assert rre.sha256(f"txid ({sha}).") == [sha]
    assert rre.sha256(f"https://example.com/tx/{other}?x=1") == [other]
    # one short or long, not hex, glued, digits only, an Ethereum transaction hash (0x), a Session ID (66)
    assert rre.sha256(sha[:-1]) == []
    assert rre.sha256(sha + "0") == []
    assert rre.sha256(sha[:-1] + "g") == []
    assert rre.sha256(f"{sha}_x") == []
    assert rre.sha256("1234567890123456" * 4) == []
    assert rre.sha256(f"0x{sha}") == []
    assert rre.sha256(f"05{sha}") == []

def test_hard_sha512():
    # made up: the SHA-512 of "example 1" and "example 2"
    sha = ("82dbc4681e280b749ca508bb9dc2cb8aa16c4cfb4d653a60d06c7375448245ce"
           "4fb73172745cd6409a233e9d1f31e18b202cc8d81822637ccca6071616586afb")
    other = ("07a86d4770426106883d0f432e57191a4abaf253f73c964bfb2d8fd4f009175c"
             "f0b89bbd204fef7ad9b72508ee5bea2b74b03f207f7ccb686ac58f98bc11a321")
    assert rre.sha512(sha.upper()) == [sha.upper()]
    assert rre.sha512(f"{other}  example.txt") == [other]
    assert rre.sha512(f'{{"sha512": "{sha}"}}') == [sha]
    assert rre.sha512(f"SHA512 (example.txt) = {other}") == [other]
    assert rre.sha512(f"SHA512 hash of example.txt:\n{sha}\nCertUtil: done") == [sha]
    assert rre.sha512(f"({other}).") == [other]
    # one long, not hex, glued, digits only, a SHA-256, after 0x
    assert rre.sha512(sha + "a") == []
    assert rre.sha512(sha[:-1] + "x") == []
    assert rre.sha512(f"x{sha}") == []
    assert rre.sha512("1234567890123456" * 8) == []
    assert rre.sha512(sha[:64]) == []
    assert rre.sha512(f"0x{sha}") == []

def test_hard_uuid():
    assert rre.uuid("{550E8400-E29B-41D4-A716-446655440000}") == ["550E8400-E29B-41D4-A716-446655440000"]
    assert rre.uuid("urn:uuid:123e4567-e89b-12d3-a456-426614174000") == ["123e4567-e89b-12d3-a456-426614174000"]
    assert rre.uuid('{"id": "0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"}') == ["0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d"]
    assert rre.uuid("/Application/0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D/Documents") == [
        "0A1B2C3D-4E5F-4A6B-8C7D-9E0F1A2B3C4D"]
    assert rre.uuid("https://example.com/item?id=550e8400-e29b-41d4-a716-446655440000&x=1") == [
        "550e8400-e29b-41d4-a716-446655440000"]
    assert rre.uuid("request 123e4567-e89b-12d3-a456-426614174000.") == ["123e4567-e89b-12d3-a456-426614174000"]
    # a group one short or long, a dash missing or an underscore instead, not hex, glued, no dashes (an MD5's form)
    assert rre.uuid("550e840-e29b-41d4-a716-446655440000") == []
    assert rre.uuid("550e8400-e29b-41d4-a716-44665544000") == []
    assert rre.uuid("550e8400-e29b-41d4-a716-4466554400001") == []
    assert rre.uuid("550e8400e29b-41d4-a716-446655440000") == []
    assert rre.uuid("550e8400-e29b-41d4-a716_446655440000") == []
    assert rre.uuid("550g8400-e29b-41d4-a716-446655440000") == []
    assert rre.uuid("x550e8400-e29b-41d4-a716-446655440000") == []
    assert rre.uuid("550e8400e29b41d4a716446655440000") == []

def test_hard_messenger_media_filename():
    for name in ("doc_2026-03-03_09-12-44.pdf", "signal-attachment-2026-03-03-091244.jpg",
                 "photo_2026-03-03_09-12-44 (3).jpg"):
        assert rre.messenger_media_filename(name) == [name]
    assert rre.messenger_media_filename('"file": "photo_2026-03-03_09-12-44.jpg"') == ["photo_2026-03-03_09-12-44.jpg"]
    # an impossible month, day or hour, no time, no extension, glued, capitalised, other apps' names
    for name in ("signal-2026-13-03-091244.jpg", "photo_2026-03-32_09-12-44.jpg", "photo_2026-03-03_25-12-44.jpg",
                 "photo_2026-03-03.jpg", "signal-2026-03-03-091244", "xsignal-2026-03-03-091244.jpg",
                 "Photo_2026-03-03_09-12-44.jpg", "photo_album.jpg", "file_1@example.com", "IMG-20260303-WA0007.jpg"):
        assert rre.messenger_media_filename(name) == []

def test_hard_otpauth_uri():
    assert rre.otpauth_uri("OTPAUTH://TOTP/EXAMPLE?SECRET=JBSWY3DPEHPK3PXP") == [
        "OTPAUTH://TOTP/EXAMPLE?SECRET=JBSWY3DPEHPK3PXP"]
    full = ("otpauth://totp/Example:jane?secret=JBSWY3DPEHPK3PXP&issuer=Example&algorithm=SHA1&digits=6"
            "&period=30")
    assert rre.otpauth_uri(f'<a href="{full}">') == [full]
    assert rre.otpauth_uri('{"uri":"otpauth://totp/Example?issuer=Example&secret=JBSWY3DPEHPK3PXP"}') == [
        "otpauth://totp/Example?issuer=Example&secret=JBSWY3DPEHPK3PXP"]
    assert rre.otpauth_uri("(otpauth://totp/?secret=JBSWY3DPEHPK3PXP)") == ["otpauth://totp/?secret=JBSWY3DPEHPK3PXP"]
    encoded = "otpauth://totp/Example%20Co:jane%40example.com?secret=JBSWY3DPEHPK3PXP&issuer=Example%20Co"
    assert rre.otpauth_uri(f"{encoded}\n") == [encoded]
    assert rre.otpauth_uri("export: otpauth-migration://offline?data=CjEKCkhlbGxvIQ%3D%3D;") == [
        "otpauth-migration://offline?data=CjEKCkhlbGxvIQ%3D%3D"]
    # an empty secret, a parameter ending in secret, one slash, no query, no export data, another scheme, glued
    assert rre.otpauth_uri("otpauth://totp/Example?secret=&issuer=x") == []
    assert rre.otpauth_uri("otpauth://totp/Example?mysecret=ABC&issuer=X") == []
    assert rre.otpauth_uri("otpauth:/totp/Example?secret=ABC") == []
    assert rre.otpauth_uri("otpauth://totp/Example") == []
    assert rre.otpauth_uri("otpauth-migration://offline?data=") == []
    assert rre.otpauth_uri("https://example.com/?secret=ABC") == []
    assert rre.otpauth_uri("xotpauth://totp/E?secret=ABC") == []

def test_hard_password():
    # password checks the whole input as one value, it does not search text
    assert rre.password("Correct-Horse-9-Battery") == ["Correct-Horse-9-Battery"]
    assert rre.password("P@ssw0rd!") == ["P@ssw0rd!"]
    assert rre.password("Wachtwoord1é") == ["Wachtwoord1é"]
    assert rre.password("Abcdefg1\n") == ["Abcdefg1"]
    assert rre.password("my password is Abcdefg1") == ["my password is Abcdefg1"]
    assert rre.password(" Abcdefg1 ") == [" Abcdefg1 "]
    # no lowercase, one character short, digits only, empty, two lines (a text, not a value)
    assert rre.password("ABCDEFG1") == []
    assert rre.password("Abcdef1") == []
    assert rre.password("12345678") == []
    assert rre.password("") == []
    assert rre.password("Abcd\nefg1XY") == []
    assert rre.password("password:\nAbcdefg1") == []

def test_hard_password_hash():
    # made up
    bcrypt = "$2y$10$" + "abcdefghijklmnopqrstuv" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234"
    assert rre.password_hash(f"INSERT INTO users VALUES (1,'jane','{bcrypt}');") == [bcrypt]
    argon = "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG"
    assert rre.password_hash(f'{{"hash": "{argon}"}}') == [argon]
    assert rre.password_hash("jane:$apr1$saltsalt$qjXMvbEw8oaL.CzflDtaK/") == ["$apr1$saltsalt$qjXMvbEw8oaL.CzflDtaK/"]
    assert rre.password_hash("pbkdf2_sha1$10000$salt$aGFzaGhhc2hoYXNo") == ["pbkdf2_sha1$10000$salt$aGFzaGhhc2hoYXNo"]
    assert rre.password_hash("phpbb: $H$9IQRaTwmfeRo7ud9Fh4E2PdI0S3r.L0.") == ["$H$9IQRaTwmfeRo7ud9Fh4E2PdI0S3r.L0"]
    bcrypt2 = "$2a$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW"
    # an unknown bcrypt version, one character short or long, a salt too long, an MD5, Django's unsupported sha512,
    # Argon2 without its hash, phpass one short, sha512-crypt one short
    assert rre.password_hash(bcrypt2.replace("$2a$", "$2c$")) == []
    assert rre.password_hash(bcrypt2[:-1]) == []
    assert rre.password_hash(bcrypt2 + "x") == []
    assert rre.password_hash("$1$saltsaltX$qjXMvbEw8oaL.CzflDtaK/") == []
    assert rre.password_hash("d41d8cd98f00b204e9800998ecf8427e") == []
    assert rre.password_hash("pbkdf2_sha512$10000$salt$aGFzaA==") == []
    assert rre.password_hash("$argon2id$v=19$m=65536,t=3,p=4$") == []
    assert rre.password_hash("$P$9IQRaTwmfeRo7ud9Fh4E2PdI0S3r.L") == []
    assert rre.password_hash("$6$saltstring$" + "a" * 85) == []

def test_hard_pgp_block():
    # made up
    public = ("-----BEGIN PGP PUBLIC KEY BLOCK-----\nVersion: GnuPG v2\nComment: https://example.com/a-b\n\n"
              "mQINBFexample\n=AbCd\n-----END PGP PUBLIC KEY BLOCK-----")
    assert rre.pgp_block(f"my key:\n{public}\n") == [public]
    private = "-----BEGIN PGP PRIVATE KEY BLOCK-----\n\nlQOYBFexample\n-----END PGP PRIVATE KEY BLOCK-----"
    signature = "-----BEGIN PGP SIGNATURE-----\n\niQEzBAEBCAAdFiEE\n-----END PGP SIGNATURE-----"
    assert rre.pgp_block(f"{private}\n{signature}") == [private, signature]
    # a clear-signed message, whose text may have dashes, with its signature
    signed = f"-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\nhello -- world\n{signature}"
    assert rre.pgp_block(f"> {signed}\n") == [signed]
    crlf = "-----BEGIN PGP MESSAGE-----\r\n\r\nhQEMAexample\r\n-----END PGP MESSAGE-----"
    assert rre.pgp_block(crlf) == [crlf]
    escaped = "-----BEGIN PGP MESSAGE-----\\n\\nhQEMAexample\\n-----END PGP MESSAGE-----"
    assert rre.pgp_block(f'{{"body": "{escaped}"}}') == [escaped]
    # a truncated block does not swallow the next one
    assert rre.pgp_block(f"-----BEGIN PGP MESSAGE-----\ntruncated\n\n{public}") == [public]
    # no END, an END of another type, a body missing, four dashes, lowercase, a PEM key, a signed message without
    # its signature
    assert rre.pgp_block("-----BEGIN PGP MESSAGE-----\nhQEMAexample\n") == []
    assert rre.pgp_block("-----BEGIN PGP MESSAGE-----\nhQEMA\n-----END PGP PUBLIC KEY BLOCK-----") == []
    assert rre.pgp_block("-----BEGIN PGP MESSAGE----------END PGP MESSAGE-----") == []
    assert rre.pgp_block("----BEGIN PGP MESSAGE----\nhQEMA\n----END PGP MESSAGE----") == []
    assert rre.pgp_block("-----begin pgp message-----\nhQEMA\n-----end pgp message-----") == []
    assert rre.pgp_block("-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC\n-----END PRIVATE KEY-----") == []
    assert rre.pgp_block("-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\nhello\n") == []

def test_hard_private_key_block():
    # made up bodies
    pkcs8 = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCexample\n-----END PRIVATE KEY-----"
    assert rre.private_key_block(pkcs8) == [pkcs8]
    # a service account's JSON, the newlines escaped
    escaped = pkcs8.replace("\n", "\\n")
    assert rre.private_key_block(f'{{"private_key": "{escaped}\\n", "client_email": "x"}}') == [escaped]
    encrypted = "-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFHDBOBgkqhkiG9w0BBQ0wQTAp\n-----END ENCRYPTED PRIVATE KEY-----"
    assert rre.private_key_block(f"key.pem: {encrypted}.") == [encrypted]
    ec = "-----BEGIN EC PRIVATE KEY-----\r\nMHcCAQEEIBkgexampleexample\r\n-----END EC PRIVATE KEY-----"
    assert rre.private_key_block(ec) == [ec]
    dsa = "-----BEGIN DSA PRIVATE KEY-----\nMIIBuwIBAAKBgQDexample+/\n-----END DSA PRIVATE KEY-----"
    assert rre.private_key_block(f"({dsa})") == [dsa]
    # a placeholder, an empty body, a short one, no END, a PGP key, a certificate, four dashes
    assert rre.private_key_block("-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----") == []
    assert rre.private_key_block("-----BEGIN PRIVATE KEY-----\n-----END PRIVATE KEY-----") == []
    assert rre.private_key_block('key = "-----BEGIN PRIVATE KEY-----\\n<your key here>\\n-----END PRIVATE KEY-----"') == []
    assert rre.private_key_block("-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC\n") == []
    assert rre.private_key_block("-----BEGIN PGP PRIVATE KEY BLOCK-----\nlQOYBFexample\n-----END PGP PRIVATE KEY BLOCK-----") == []
    assert rre.private_key_block("-----BEGIN CERTIFICATE-----\nMIIDdzCCAl+gAwIBAgIE\n-----END CERTIFICATE-----") == []
    assert rre.private_key_block("----BEGIN PRIVATE KEY----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC\n----END PRIVATE KEY----") == []

def test_hard_screenshot_filename():
    for name in ("Zrzut ekranu 2026-03-02 o 08.15.12.png", "Captura de pantalla 2026-03-02 a las 08.15.12.png",
                 "Schermata 2026-03-02 alle 08.15.12.png", "Screenshot_20260302-081512_Chrome.jpg",
                 # macOS puts a narrow no-break space before AM
                 "Screenshot 2026-03-02 at 8.15.12\u202fAM.png"):
        assert rre.screenshot_filename(name) == [name]
    assert rre.screenshot_filename("/storage/emulated/0/Pictures/Screenshots/Screenshot_20260302-081512.png") == [
        "Screenshot_20260302-081512.png"]
    # an impossible month, day, hour or minute, no date, no extension or another one, lowercase, glued, a camera name
    for name in ("Screenshot_20261302-081512.png", "Screenshot_20260300-081512.png", "Screenshot_20260332-081512.png",
                 "Screenshot_20260302-251512.png", "Screenshot_20260302-086512.png", "Screenshot (12).png",
                 "Screenshot_20260302-081512", "Screenshot_20260302-081512.pdf", "screenshot_20260302-081512.png",
                 "MyScreenshot_20260302-081512.png", "IMG_20260302_081512.jpg"):
        assert rre.screenshot_filename(name) == []

def test_hard_session_id():
    sid = "05" + "0123456789abcdef" * 4
    assert rre.session_id(f"Session ID: {sid}.") == [sid]
    assert rre.session_id(f'{{"sessionId":"{sid}"}}') == [sid]
    assert rre.session_id(f"({sid})") == [sid]
    assert rre.session_id(f"jane,{sid},2026") == [sid]
    assert rre.session_id(f"add me\n{sid}\n") == [sid]
    assert rre.session_id("05" + "fedcba9876543210" * 4) == ["05" + "fedcba9876543210" * 4]
    # uppercase, one long or short, glued, after 0x, not hex, a SHA-256 starting with 05
    assert rre.session_id(sid.upper()) == []
    assert rre.session_id(sid + "a") == []
    assert rre.session_id(sid[:-1]) == []
    assert rre.session_id(f"x{sid}") == []
    assert rre.session_id(f"0x{sid}") == []
    assert rre.session_id(sid[:-1] + "g") == []
    assert rre.session_id(sid[:64]) == []

def test_hard_ssh_fingerprint():
    sha = "SHA256:ht+qb8ckV14AvQbgJldN09NwZ23vdwTiRnXHtaFRcEY"
    assert rre.ssh_fingerprint(f'{{"fingerprint": "{sha}"}}') == [sha]
    # base64 padding after it, glued, dashes instead of colons
    assert rre.ssh_fingerprint(f"{sha}=") == []
    assert rre.ssh_fingerprint(f"x{sha}") == []
    assert rre.ssh_fingerprint("93-28-d9-7f-3f-de-a4-5d-b6-09-63-33-4f-2a-9a-99") == []

def test_hard_ssh_public_key():
    ed = "AAAAC3NzaC1lZDI1NTE5AAAAIAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB"  # made up
    ecdsa = "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB"
    rsa = "AAAAB3NzaC1yc2EAAAADAQABAAABAQDBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB=="
    assert rre.ssh_public_key(f"example.com,192.0.2.1 ecdsa-sha2-nistp256 {ecdsa}") == [f"ecdsa-sha2-nistp256 {ecdsa}"]
    assert rre.ssh_public_key(f"sk-ssh-ed25519@openssh.com {ed} jane@yubikey") == [
        f"sk-ssh-ed25519@openssh.com {ed} jane@yubikey"]
    assert rre.ssh_public_key(f'command="/bin/true",no-pty ssh-rsa {rsa} jane@host') == [f"ssh-rsa {rsa} jane@host"]
    assert rre.ssh_public_key(f'{{"key": "ssh-ed25519 {ed}"}}') == [f"ssh-ed25519 {ed}"]
    assert rre.ssh_public_key(f"ssh-dss {rsa}") == [f"ssh-dss {rsa}"]
    # uppercase type, two spaces or a tab, glued, an unknown type, base64 not starting with AAAA, too short
    assert rre.ssh_public_key(f"SSH-ED25519 {ed}") == []
    assert rre.ssh_public_key(f"ssh-ed25519  {ed}") == []
    assert rre.ssh_public_key(f"ssh-ed25519\t{ed}") == []
    assert rre.ssh_public_key(f"xssh-ed25519 {ed}") == []
    assert rre.ssh_public_key(f"ssh-foo {ed}") == []
    assert rre.ssh_public_key(f"ssh-ed25519 BBBB{ed[4:]}") == []
    assert rre.ssh_public_key("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5") == []

def test_hard_usb_vid_pid():
    assert rre.usb_vid_pid("usb_id=1234:abcd") == ["usb_id=1234:abcd"]
    assert rre.usb_vid_pid("Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub") == ["ID 1d6b:0003"]
    # a dash instead of &, not hex, a device ID without lsusb's line
    assert rre.usb_vid_pid("VID_1234-PID_ABCD") == []
    assert rre.usb_vid_pid("VID_G234&PID_ABCD") == []
    assert rre.usb_vid_pid("device ID 1234:abcd") == []

def test_hard_whatsapp_media_filename():
    for name in ("AUD-20260303-WA0003.opus", "DOC-20260303-WA0007.pdf", "WhatsApp Ptt 2026-03-03 at 09.12.44.ogg",
                 "WhatsApp Image 2026-03-03 at 09.12.44_1a2b3c4d.jpg"):
        assert rre.whatsapp_media_filename(name) == [name]
    assert rre.whatsapp_media_filename("/Media/WhatsApp Images/Sent/IMG-20260303-WA0007.jpg") == [
        "IMG-20260303-WA0007.jpg"]
    assert rre.whatsapp_media_filename('"VID-20260303-WA0012.mp4",') == ["VID-20260303-WA0012.mp4"]
    # a camera name, an impossible date or hour, no extension, no time, a chat export, three or six digits, glued,
    # lowercase
    for name in ("IMG_20260303_091244.jpg", "IMG-20261303-WA0007.jpg", "IMG-20260332-WA0007.jpg",
                 "WhatsApp Image 2026-03-03 at 25.12.44.jpeg", "IMG-20260303-WA0007", "WhatsApp Image 2026-03-03.jpeg",
                 "WhatsApp Chat with Example.txt", "IMG-20260303-WA007.jpg", "IMG-20260303-WA123456.jpg",
                 "XIMG-20260303-WA0007.jpg", "img-20260303-wa0007.jpg"):
        assert rre.whatsapp_media_filename(name) == []

def test_hard_wifi_qr_string():
    # Android's share code, WPA2-Enterprise fields
    assert rre.wifi_qr_string("WIFI:S:MyNet;T:WPA;P:pass1234;H:false;;") == ["WIFI:S:MyNet;T:WPA;P:pass1234;H:false;;"]
    eap = "WIFI:T:WPA2-EAP;S:Corp;E:PEAP;PH2:MSCHAPV2;A:anon;I:jane;P:pass1234;;"
    assert rre.wifi_qr_string(eap) == [eap]
    assert rre.wifi_qr_string('{"qr":"WIFI:T:WPA;S:TestNet;P:test-pass;;"}') == ["WIFI:T:WPA;S:TestNet;P:test-pass;;"]
    assert rre.wifi_qr_string("code WIFI:S:TestNet;P:x;") == ["WIFI:S:TestNet;P:x;"]
    assert rre.wifi_qr_string("WIFI:T:WPA;S:TestNet;P:test-pass;;\nnext") == ["WIFI:T:WPA;S:TestNet;P:test-pass;;"]
    assert rre.wifi_qr_string("(WIFI:T:SAE;S:Home 5G;P:x y z;;)") == ["WIFI:T:SAE;S:Home 5G;P:x y z;;"]
    # unterminated, lowercase scheme or field, an empty name, glued, a name too long
    assert rre.wifi_qr_string("WIFI:S:TestNet") == []
    assert rre.wifi_qr_string("wifi:S:TestNet;;") == []
    assert rre.wifi_qr_string("WIFI:s:TestNet;;") == []
    assert rre.wifi_qr_string("WIFI:S:;P:x;;") == []
    assert rre.wifi_qr_string("xWIFI:S:TestNet;;") == []
    assert rre.wifi_qr_string("WIFI:S:" + "a" * 129 + ";;") == []

def test_hard_windows_path():
    # JSON doubles the backslashes
    assert rre.windows_path(r'{"path": "C:\\Users\\Jane\\report.docx"}') == [r"C:\\Users\\Jane\\report.docx"]
    assert rre.windows_path(r'{"share": "\\\\fileserver\\share\\a.txt"}') == [r"\\\\fileserver\\share\\a.txt"]
    assert rre.windows_path(r"C:\Program Files\Example\app.exe") == [r"C:\Program Files\Example\app.exe"]
    assert rre.windows_path(r"see (D:\backup\x.zip).") == [r"D:\backup\x.zip"]
    assert rre.windows_path(r'"C:\Users\Jane\a.txt"') == [r"C:\Users\Jane\a.txt"]
    assert rre.windows_path("2026-03-02 08:15:12 opened e:\\Backup\\notes.txt\n") == [r"e:\Backup\notes.txt"]
    # a registry key, a relative path, a drive alone, an environment variable, a file URL, glued, a Unix path
    assert rre.windows_path(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft") == []
    assert rre.windows_path(r"Users\Jane\x.txt") == []
    assert rre.windows_path("C:\\") == []
    assert rre.windows_path(r"%SystemRoot%\System32\x.dll") == []
    assert rre.windows_path("file:///C:/Users/x.txt") == []
    assert rre.windows_path(r"xC:\Users\a.txt") == []
    assert rre.windows_path("/home/jane/x.txt") == []

def test_hard_windows_sid():
    assert rre.windows_sid(r"HKU\S-1-5-21-1004336348-1177238915-682003330-1001\Software") == [
        "S-1-5-21-1004336348-1177238915-682003330-1001"]
    assert rre.windows_sid("SID: S-1-5-21-1004336348-1177238915-682003330-500.") == [
        "S-1-5-21-1004336348-1177238915-682003330-500"]
    # an Entra ID (Azure AD) user, a service SID, both made up
    assert rre.windows_sid('{"sid":"S-1-12-1-1234567890-1234567890-1234567890-1234567890"}') == [
        "S-1-12-1-1234567890-1234567890-1234567890-1234567890"]
    assert rre.windows_sid("S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464") == [
        "S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464"]
    assert rre.windows_sid("(S-1-5-32-545)") == ["S-1-5-32-545"]
    assert rre.windows_sid("S-1-5-32-544-") == ["S-1-5-32-544"]
    # a subauthority of 11 digits, lowercase, revision 2, glued, a 3-digit authority, 16 subauthorities, only one
    assert rre.windows_sid("S-1-5-21-12345678901-1-1") == []
    assert rre.windows_sid("s-1-5-32-544") == []
    assert rre.windows_sid("S-2-5-32-544") == []
    assert rre.windows_sid("XS-1-5-32-544") == []
    assert rre.windows_sid("S-1-123-5-6") == []
    assert rre.windows_sid("S-1-5-" + "-".join(["1"] * 16)) == []
    assert rre.windows_sid("S-1-5-32") == []

def test_hard_keys_and_paths_stay_fast():
    # an armored block without its END was scanned to the end of the text from every BEGIN
    start = time.perf_counter()
    for text in ('-----BEGIN PGP MESSAGE-----\n' * 3700, '-----BEGIN PGP SIGNED MESSAGE-----\na' * 2800,
                 '-----BEGIN PRIVATE KEY-----' + 'a-' * 50000, 'C:\\\\a ' * 16000, 'a0 ' * 33000,
                 'Screenshot_20260302-' * 5000, 'ecid: ' * 16000, 'eyJa.eyJa.' * 10000):
        rre.pgp_block(text), rre.private_key_block(text), rre.windows_path(text), rre.md5(text), rre.sha1(text)
        rre.sha256(text), rre.sha512(text), rre.screenshot_filename(text), rre.apple_ecid(text), rre.jwt(text)
    assert time.perf_counter() - start < 1


# hardened tests: dates and times, places, vehicles, ships and parcels, products and publications, text, justice

def test_hard_air_waybill():
    # made up: the 7-digit serial mod 7 is the last digit
    assert rre.air_waybill("AWB020-12345675") == ["AWB020-12345675"]
    assert rre.air_waybill("awb no. 125-1234 5675") == ["awb no. 125-1234 5675"]
    assert rre.air_waybill("Air Waybill Number: 057-11111111.") == ["Air Waybill Number: 057-11111111"]
    assert rre.air_waybill("airwaybill 176-00000000") == ["airwaybill 176-00000000"]
    assert rre.air_waybill("(MAWB 220-98765435)") == ["MAWB 220-98765435"]
    assert rre.air_waybill('{"awb": "020-12345675"}') == ['awb": "020-12345675']
    assert rre.air_waybill("AWB: 020 1234 5675") == ["AWB: 020 1234 5675"]
    # a forwarder's house waybill, one digit short and too long, check digit wrong, inside a word, no AWB keyword
    assert rre.air_waybill("HAWB 020-12345675") == []
    assert rre.air_waybill("AWB 020-1234567") == []
    assert rre.air_waybill("AWB 020-123456751") == []
    assert rre.air_waybill("AWB 125-12345676") == []
    assert rre.air_waybill("AWB 02012345675X") == []
    assert rre.air_waybill("waybill 020-12345675") == []
    assert rre.air_waybill("AWB 020/12345675") == []


def test_hard_aircraft_icao_address():
    # made up
    assert rre.aircraft_icao_address("ModeS 44A1B2") == ["ModeS 44A1B2"]
    assert rre.aircraft_icao_address("MODE S: 3C6444,") == ["MODE S: 3C6444"]
    assert rre.aircraft_icao_address("icao_24bit=44a1b2&") == ["icao_24bit=44a1b2"]
    # the word modes, five, seven and eight hex digits, not hex, no ICAO or Mode S label, an airport code
    assert rre.aircraft_icao_address("two modes 44A1B2") == []
    assert rre.aircraft_icao_address("Modes 44a1b2") == []
    assert rre.aircraft_icao_address("ICAO: 44A1B") == []
    assert rre.aircraft_icao_address("icao24=44a1b2c") == []
    assert rre.aircraft_icao_address("ICAO 44A1B2C3") == []
    assert rre.aircraft_icao_address("Mode S code 44A1BG") == []
    assert rre.aircraft_icao_address("callsign 44A1B2") == []
    assert rre.aircraft_icao_address("ICAO code: EBBR") == []


def test_hard_airline_ticket_number():
    # made up
    assert rre.airline_ticket_number("Ticket #057-2123456789") == ["Ticket #057-2123456789"]
    assert rre.airline_ticket_number("biglietto 0552123456789") == ["biglietto 0552123456789"]
    assert rre.airline_ticket_number("bilet nr 0802123456789") == ["bilet nr 0802123456789"]
    assert rre.airline_ticket_number("ticket no: 0572123456789") == ["ticket no: 0572123456789"]
    # a longer word, a letter after, 12 and 14 digits, no label, a support ticket
    assert rre.airline_ticket_number("ticketing 0572123456789") == []
    assert rre.airline_ticket_number("ticket 0572123456789X") == []
    assert rre.airline_ticket_number("TKT 057-212345678") == []
    assert rre.airline_ticket_number("ticket 05721234567890") == []
    assert rre.airline_ticket_number("receipt 0572123456789") == []
    assert rre.airline_ticket_number("support ticket #48213") == []


_BP_ONE = "M1DOE/JANE            EXK7P2Q BRUBCNSN 3171 172Y023C0098 100"


def test_hard_boarding_pass_barcode():
    # made up; no e-ticket flag, an apostrophe in the name, after a tab, in a URL and at the end of a log line
    paper = "M1JANSSENS/AN          PQR7ST LGWBRUSN 2094 300Y014F0041 100"
    assert rre.boarding_pass_barcode(paper) == [paper]
    oneil = "M1O'NEIL/SEAN         EK9Z2LM DUBAMSEI 0602 001Y002A0001 100"
    assert rre.boarding_pass_barcode("bcbp\t" + oneil) == [oneil]
    assert rre.boarding_pass_barcode("?barcode=" + _BP_ONE + "&next") == [_BP_ONE]
    assert rre.boarding_pass_barcode("2026-03-02 08:15 scanned " + paper) == [paper]
    # a flight date of 367, no legs, lowercase, a size that is no hex, two letters in front, a leg cut short
    assert rre.boarding_pass_barcode(_BP_ONE.replace("172Y", "367Y")) == []
    assert rre.boarding_pass_barcode("M0" + _BP_ONE[2:]) == []
    assert rre.boarding_pass_barcode(_BP_ONE.replace("BRUBCN", "brubcn")) == []
    assert rre.boarding_pass_barcode(_BP_ONE[:-2] + "G0") == []
    assert rre.boarding_pass_barcode("XM" + _BP_ONE[1:]) == []
    assert rre.boarding_pass_barcode(_BP_ONE[:50]) == []


def test_hard_booking_reference():
    # made up; a label in capitals or with number or no. after it
    assert rre.booking_reference("PNR NUMBER: XK7P2Q") == ["PNR NUMBER: XK7P2Q"]
    assert rre.booking_reference("YOUR PNR NUMBER IS XK7P2Q") == ["PNR NUMBER IS XK7P2Q"]
    assert rre.booking_reference("PNR No. XK7P2Q") == ["PNR No. XK7P2Q"]
    assert rre.booking_reference("Booking reference number: XK7P2Q.") == ["Booking reference number: XK7P2Q"]
    assert rre.booking_reference("Buchungsreferenz: ZX8Y7W") == ["Buchungsreferenz: ZX8Y7W"]
    assert rre.booking_reference("kod rezerwacji: QWE123") == ["kod rezerwacji: QWE123"]
    assert rre.booking_reference("cod rezervare ABC123") == ["cod rezervare ABC123"]
    # five and seven characters, lowercase, digits only, reservation alone, no label
    assert rre.booking_reference("PNR XK7P2") == []
    assert rre.booking_reference("PNR XK7P2QZ") == []
    assert rre.booking_reference("pnr xk7p2q") == []
    assert rre.booking_reference("Booking reference: 123456") == []
    assert rre.booking_reference("Reservation: XK7P2Q") == []
    assert rre.booking_reference("booking XK7P2Q") == []


def test_hard_cellebrite_datetime():
    assert rre.cellebrite_datetime("13/12/2026 8:15:12(UTC+1)") == ["13/12/2026 8:15:12(UTC+1)"]
    assert rre.cellebrite_datetime("12/31/2026 11:59:59 PM(UTC-5)") == ["12/31/2026 11:59:59 PM(UTC-5)"]
    assert rre.cellebrite_datetime("2-3-2026 8:15:12(UTC)") == ["2-3-2026 8:15:12(UTC)"]
    assert rre.cellebrite_datetime("2/3/26 8:15:12 PM(UTC-5)") == ["2/3/26 8:15:12 PM(UTC-5)"]
    assert rre.cellebrite_datetime("Read: 14/09/2026 09:15:00(UTC+05:30) by owner") == [
        "14/09/2026 09:15:00(UTC+05:30)"]
    assert rre.cellebrite_datetime('{"timestamp": "2/3/2026 8:15:12(UTC+1)"}') == ["2/3/2026 8:15:12(UTC+1)"]
    # no month 13 either way, day 32, hour 24, offset 15, inside a longer date, mixed separators, no seconds or brackets
    assert rre.cellebrite_datetime("13/13/2026 8:15:12(UTC+1)") == []
    assert rre.cellebrite_datetime("32/01/2026 8:15:12(UTC+1)") == []
    assert rre.cellebrite_datetime("2/3/2026 24:15:12(UTC+1)") == []
    assert rre.cellebrite_datetime("2/3/2026 8:15:12(UTC+15)") == []
    assert rre.cellebrite_datetime("1/12/02/2026 8:15:12(UTC+1)") == []
    assert rre.cellebrite_datetime("2/3.2026 8:15:12(UTC+1)") == []
    assert rre.cellebrite_datetime("2/3/2026 8:15(UTC+1)") == []
    assert rre.cellebrite_datetime("2/3/2026 8:15:12 UTC+1") == []


def test_hard_container_number():
    # CSQU3054383 is the ISO 6346 example; the others are made up
    assert rre.container_number("MSCU1234566") == ["MSCU1234566"]
    assert rre.container_number("TGHU 987654 2.") == ["TGHU 987654 2"]
    assert rre.container_number("reefer ABCZ0000010 (Z: chassis)") == ["ABCZ0000010"]
    assert rre.container_number("XYZJ5555556,") == ["XYZJ5555556"]
    assert rre.container_number("MSCU 123456-6") == ["MSCU 123456-6"]
    assert rre.container_number('{"container": "CSQU3054383"}') == ["CSQU3054383"]
    assert rre.container_number("mscu1234566") == ["mscu1234566"]
    # check digit wrong, category X, one digit more and less, inside a word, three letters, grouped otherwise
    assert rre.container_number("MSCU1234567") == []
    assert rre.container_number("MSCX1234566") == []
    assert rre.container_number("MSCU12345666") == []
    assert rre.container_number("MSCU123456") == []
    assert rre.container_number("XMSCU1234566") == []
    assert rre.container_number("MSC1234566") == []
    assert rre.container_number("MSCU 1234 566") == []


def test_hard_dhl_tracking_number():
    # made up
    assert rre.dhl_tracking_number("DHL 9876543213") == ["DHL 9876543213"]
    assert rre.dhl_tracking_number("JJD000390007826789345") == ["JJD000390007826789345"]
    assert rre.dhl_tracking_number("DHL Express waybill no. 98 7654 3213") == ["DHL Express waybill no. 98 7654 3213"]
    assert rre.dhl_tracking_number("DHL: 340123456788.") == ["DHL: 340123456788"]
    assert rre.dhl_tracking_number("(DHL 00340434000000000017)") == ["DHL 00340434000000000017"]
    # JJD too short, inside a word, 11 digits, DHLX, check digit wrong, JJD too long
    assert rre.dhl_tracking_number("JJD12345") == []
    assert rre.dhl_tracking_number("xJJD0099999999") == []
    assert rre.dhl_tracking_number("DHL 12345678901") == []
    assert rre.dhl_tracking_number("DHLX 9876543213") == []
    assert rre.dhl_tracking_number("DHL 9876543214") == []
    assert rre.dhl_tracking_number("JJD009999999999999999999") == []


def test_hard_dpd_tracking_number():
    # made up
    assert rre.dpd_tracking_number("DPD 099811112222331") == ["DPD 099811112222331"]
    assert rre.dpd_tracking_number("DPD 0998 1111 2222 33 1.") == ["DPD 0998 1111 2222 33 1"]
    assert rre.dpd_tracking_number("DPD Paketnummer: 01234567890123 3") == ["DPD Paketnummer: 01234567890123 3"]
    assert rre.dpd_tracking_number('{"carrier":"DPD","parcel":"09981111222233"}') == [
        'DPD","parcel":"09981111222233']
    # 13 digits, check character wrong, DPDX, no keyword, a digit after the check character, 13 grouped
    assert rre.dpd_tracking_number("DPD 0998111122223") == []
    assert rre.dpd_tracking_number("DPD 099811112222334") == []
    assert rre.dpd_tracking_number("DPDX 09981111222233") == []
    assert rre.dpd_tracking_number("Paketnummer 09981111222233") == []
    assert rre.dpd_tracking_number("DPD 0998111122223311") == []
    assert rre.dpd_tracking_number("DPD 0998 1111 2222 3") == []


def test_hard_exif_datetime():
    assert rre.exif_datetime("2026:03:02 08:15:12Z") == ["2026:03:02 08:15:12Z"]
    assert rre.exif_datetime("ModifyDate 1999:12:31 23:59:59") == ["1999:12:31 23:59:59"]
    assert rre.exif_datetime('{"DateTimeOriginal": "2026:03:02 08:15:13"}') == ["2026:03:02 08:15:13"]
    assert rre.exif_datetime("2026:03:02 08:15:12-05:00") == ["2026:03:02 08:15:12-05:00"]
    assert rre.exif_datetime("(2026:03:02 08:15:12.5)") == ["2026:03:02 08:15:12.5"]
    assert rre.exif_datetime("2026:03:02 08:15:14 IMG_0001.HEIC") == ["2026:03:02 08:15:14"]
    # month 0, day 32, hour 24, minute 60, the 1800s, T instead of a space, a longer number in front
    assert rre.exif_datetime("2026:00:02 08:15:12") == []
    assert rre.exif_datetime("2026:03:32 08:15:12") == []
    assert rre.exif_datetime("2026:03:02 24:15:12") == []
    assert rre.exif_datetime("2026:03:02 08:60:12") == []
    assert rre.exif_datetime("1899:03:02 08:15:12") == []
    assert rre.exif_datetime("2026:03:02T08:15:12") == []
    assert rre.exif_datetime("12026:03:02 08:15:12") == []


def test_hard_exif_gps_rational():
    # degrees as a decimal fraction, minutes with decimals, 180 degrees, no spaces, JSON
    assert rre.exif_gps_rational("51123456/1000000, 0/1, 0/1") == ["51123456/1000000, 0/1, 0/1"]
    assert rre.exif_gps_rational("GPSLatitude 51/1, 1530/100, 0/1") == ["51/1, 1530/100, 0/1"]
    assert rre.exif_gps_rational("180/1, 0/1, 0/1") == ["180/1, 0/1, 0/1"]
    assert rre.exif_gps_rational("GPSLongitude=3/1,43/1,234/10") == ["3/1,43/1,234/10"]
    assert rre.exif_gps_rational('{"GPSLatitude": "50/1, 50/1, 3012/100"}') == ["50/1, 50/1, 3012/100"]
    # dates and scores in tenths, 181 degrees, minutes or seconds of 60, two rationals, in a path, a fourth fraction
    assert rre.exif_gps_rational("1/10, 2/10, 3/10") == []
    assert rre.exif_gps_rational("scores 7/10, 8/10, 9/10") == []
    assert rre.exif_gps_rational("181/1, 0/1, 0/1") == []
    assert rre.exif_gps_rational("51/1, 60/1, 0/1") == []
    assert rre.exif_gps_rational("51/1, 15/1, 60/1") == []
    assert rre.exif_gps_rational("51/1, 15/1") == []
    assert rre.exif_gps_rational("/51/1, 15/1, 4536/100") == []
    assert rre.exif_gps_rational("51/1, 15/1, 4536/100/2") == []


def test_hard_fedex_tracking_number():
    # made up
    assert rre.fedex_tracking_number("FedEx 398765432103") == ["FedEx 398765432103"]
    # check digit wrong, 10 digits, a longer word, another carrier's keyword
    assert rre.fedex_tracking_number("FedEx 398765432104") == []
    assert rre.fedex_tracking_number("FedEx 3987654321") == []
    assert rre.fedex_tracking_number("FedExCup 398765432103") == []
    assert rre.fedex_tracking_number("UPS 398765432103") == []


def test_hard_flight_number():
    # airline codes with made-up flight numbers
    assert rre.flight_number("flight: 4U 1234") == ["flight: 4U 1234"]
    assert rre.flight_number("FLIGHT LH1234,") == ["FLIGHT LH1234"]
    # no number, a one-letter code, a longer word, seven digits, volume, a flight of stairs
    assert rre.flight_number("Flight LH") == []
    assert rre.flight_number("Flight: L 1234") == []
    assert rre.flight_number("Flugzeug LH 1234") == []
    assert rre.flight_number("Flight LH 1234567") == []
    assert rre.flight_number("volume AF 1234") == []
    assert rre.flight_number("a flight of 14 steps") == []
    assert rre.flight_number("flight lh1234") == []


def test_hard_gls_tracking_number():
    # made up
    assert rre.gls_tracking_number("GLS-Paket 500123456788") == ["GLS-Paket 500123456788"]
    assert rre.gls_tracking_number('{"carrier": "GLS", "parcel": "36631234567"}') == [
        'GLS", "parcel": "36631234567']
    assert rre.gls_tracking_number("gls: 987654321097.") == ["gls: 987654321097"]
    assert rre.gls_tracking_number("(GLS 12345678901)") == ["GLS 12345678901"]
    assert rre.gls_tracking_number("GLS Track&Trace 123456789011") == ["GLS Track&Trace 123456789011"]
    # 10 and 13 digits, GLSX, check digit wrong, no keyword, a letter after
    assert rre.gls_tracking_number("GLS 3663123456") == []
    assert rre.gls_tracking_number("GLS 3663123456731") == []
    assert rre.gls_tracking_number("GLSX 36631234567") == []
    assert rre.gls_tracking_number("GLS 500123456789") == []
    assert rre.gls_tracking_number("parcel 500123456788") == []
    assert rre.gls_tracking_number("GLS 50012345678a") == []


def test_hard_gps_coordinates():
    assert rre.gps_coordinates("(50.8467, 4.3525)") == ["50.8467, 4.3525"]
    assert rre.gps_coordinates("90.0000, 180.0000") == ["90.0000, 180.0000"]
    assert rre.gps_coordinates('{"loc": "51.05430,3.71740"}') == ["51.05430,3.71740"]
    assert rre.gps_coordinates("+48.8584, +2.2945") == ["+48.8584, +2.2945"]
    assert rre.gps_coordinates("-34.6037 , -58.3816 end") == ["-34.6037 , -58.3816"]
    # just above 90 and 180, three decimals, a semicolon, inside a version or a longer number
    assert rre.gps_coordinates("90.0001, 3.7174") == []
    assert rre.gps_coordinates("51.0543, 180.0001") == []
    assert rre.gps_coordinates("51.054, 3.7174") == []
    assert rre.gps_coordinates("51.0543, 3.717") == []
    assert rre.gps_coordinates("51.0543; 3.7174") == []
    assert rre.gps_coordinates("1.51.0543, 3.7174") == []
    assert rre.gps_coordinates("51.0543, 3.7174.5") == []
    assert rre.gps_coordinates("151.0543, 3.7174") == []


def test_hard_gps_dms():
    assert rre.gps_dms("51°03′15.5″N") == ["51°03′15.5″N"]
    assert rre.gps_dms("051° 03' 15\" N") == ["051° 03' 15\" N"]
    assert rre.gps_dms("180°00'00\"W") == ["180°00'00\"W"]
    assert rre.gps_dms("(48°51'29.5\"N, 2°17'40.2\"E)") == ["48°51'29.5\"N", "2°17'40.2\"E"]
    assert rre.gps_dms("33°52'08\"S") == ["33°52'08\"S"]
    assert rre.gps_dms("3°43'02\" O") == ["3°43'02\" O"]
    # inside a longer number, minutes 75 and seconds 60, 181 degrees, after a decimal point, no or a wrong direction
    assert rre.gps_dms("1251°03'15.5\"N") == []
    assert rre.gps_dms("51°75'15\"N") == []
    assert rre.gps_dms("51°03'60\"N") == []
    assert rre.gps_dms("181°03'15.5\"E") == []
    assert rre.gps_dms("3.51°03'15\"N") == []
    assert rre.gps_dms("51°03'15.5\"") == []
    assert rre.gps_dms("51°03'15.5\"X") == []


def test_hard_gtin():
    # made up, apart from the EAN-13 and UPC-A examples
    assert rre.gtin("GTIN-14: 00012345678905") == ["GTIN-14: 00012345678905"]
    assert rre.gtin("ean13: 8712345678906") == ["ean13: 8712345678906"]
    assert rre.gtin("UPC 0 36000 29145 2") == ["UPC 0 36000 29145 2"]
    assert rre.gtin('{"gtin": "4006381333931"}') == ['gtin": "4006381333931']
    assert rre.gtin("(GTIN 8712345678906)") == ["GTIN 8712345678906"]
    assert rre.gtin("EAN 4006381333931 1 pc") == ["EAN 4006381333931"]
    # 9, 15 and 7 digits, EANS, check digit wrong, no keyword, a letter after
    assert rre.gtin("EAN 400638133") == []
    assert rre.gtin("EAN 400638133393100") == []
    assert rre.gtin("EAN-8: 7351353") == []
    assert rre.gtin("EANS 4006381333931") == []
    assert rre.gtin("GTIN-14: 00012345678906") == []
    assert rre.gtin("item 8712345678906") == []
    assert rre.gtin("EAN 4006381333931X") == []


def test_hard_hex_color():
    assert rre.hex_color("paint it #C0FFEE.") == ["#C0FFEE"]
    assert rre.hex_color('<font color="#0f0">') == ["#0f0"]
    assert rre.hex_color("('#abc')") == ["#abc"]
    assert rre.hex_color("{color: #0f0a}") == ["#0f0a"]
    assert rre.hex_color("overlay #a1b2c3d4") == ["#a1b2c3d4"]
    # digits only, seven digits, not hex, inside a word, an HTML entity, a hyphen after, a short one without CSS
    assert rre.hex_color("#123456") == []
    assert rre.hex_color("#ff00001") == []
    assert rre.hex_color("#ff000g") == []
    assert rre.hex_color("a#ff0000") == []
    assert rre.hex_color("&#xfff;") == []
    assert rre.hex_color("#ff0000-x") == []
    assert rre.hex_color("see #ABC") == []
    assert rre.hex_color("##ff0000") == []


def test_hard_imo_number():
    # 9074729 is the usual example; the others are made up
    assert rre.imo_number("IMO9074729") == ["IMO9074729"]
    assert rre.imo_number("IMO: 9312341") == ["IMO: 9312341"]
    assert rre.imo_number("IMO No. 9176541,") == ["IMO No. 9176541"]
    assert rre.imo_number("(IMO 9800001)") == ["IMO 9800001"]
    assert rre.imo_number("IMO-nummer 9074729") == ["IMO-nummer 9074729"]
    assert rre.imo_number("IMO number: 9312341") == ["IMO number: 9312341"]
    # six and eight digits, lowercase, inside a word, check digit wrong, a regulation
    assert rre.imo_number("IMO 907472") == []
    assert rre.imo_number("IMO 90747291") == []
    assert rre.imo_number("imo 9074729") == []
    assert rre.imo_number("XIMO 9074729") == []
    assert rre.imo_number("IMO 9312342") == []
    assert rre.imo_number("IMO 2020 sulphur cap") == []


def test_hard_isbn():
    # 978-3-16-148410-0 is the usual example; the others are made up
    assert rre.isbn("isbn 9783161484100") == ["isbn 9783161484100"]
    assert rre.isbn("ISBN: 979-10-90636-07-1") == ["ISBN: 979-10-90636-07-1"]
    assert rre.isbn("ISBN 0 306 40615 2") == ["ISBN 0 306 40615 2"]
    assert rre.isbn("(ISBN 0-8044-2957-x)") == ["ISBN 0-8044-2957-x"]
    assert rre.isbn("ISBN-13: 978-3-16-148410-0.") == ["ISBN-13: 978-3-16-148410-0"]
    assert rre.isbn('{"isbn": "9783161484100"}') == ['isbn": "9783161484100']
    # check digits wrong, one digit short, an ISSN, inside a word, 977 (ISSN as EAN)
    assert rre.isbn("ISBN 978-3-16-148410-1") == []
    assert rre.isbn("ISBN 0-306-40615-3") == []
    assert rre.isbn("ISBN 978-0-306-40615") == []
    assert rre.isbn("ISSN 0317-8471") == []
    assert rre.isbn("XISBN 9783161484100") == []
    assert rre.isbn("ISBN 977-0-306-40615-7") == []


def test_hard_iso_datetime():
    assert rre.iso_datetime('"2024-03-01T14:30:05.123+01:00"') == ["2024-03-01T14:30:05.123+01:00"]
    assert rre.iso_datetime("2024-03-01 14:30") == ["2024-03-01 14:30"]
    assert rre.iso_datetime("2024-03-01T14:30:05+0100") == ["2024-03-01T14:30:05+0100"]
    assert rre.iso_datetime("(2024-12-31)") == ["2024-12-31"]
    assert rre.iso_datetime("created 2024-02-29T00:00Z") == ["2024-02-29T00:00Z"]
    assert rre.iso_datetime("2024-03-01T14:30:05-05:00 GET /") == ["2024-03-01T14:30:05-05:00"]
    # month 0, day 32, no leading zeros, slashes, no separators, inside a longer number, hour 24
    assert rre.iso_datetime("2024-00-10") == []
    assert rre.iso_datetime("2024-03-32") == []
    assert rre.iso_datetime("2024-3-1") == []
    assert rre.iso_datetime("2024/03/01") == []
    assert rre.iso_datetime("20240301") == []
    assert rre.iso_datetime("12024-03-01") == []
    assert rre.iso_datetime("2024-03-011") == []
    assert rre.iso_datetime("2024-03-01T24:00:00") == []


def test_hard_mac_absolute_time():
    # seven digits
    assert rre.mac_absolute_time("cocoa time: 7942219") == []


def test_hard_maps_link():
    assert rre.maps_link("https://www.google.co.uk/maps/@51.5,-0.12,15z") == [
        "https://www.google.co.uk/maps/@51.5,-0.12,15z"]
    assert rre.maps_link("http://maps.google.com/?q=50.8467,4.3525") == ["http://maps.google.com/?q=50.8467,4.3525"]
    assert rre.maps_link("https://goo.gl/maps/AbCdEf12345") == ["https://goo.gl/maps/AbCdEf12345"]
    assert rre.maps_link("https://maps.apple/p/AbCdEf") == ["https://maps.apple/p/AbCdEf"]
    assert rre.maps_link("(https://www.google.com.au/maps/@-33.86,151.2,12z)") == [
        "https://www.google.com.au/maps/@-33.86,151.2,12z"]
    assert rre.maps_link('<a href="https://ul.waze.com/ul?ll=50.85,4.35">') == ["https://ul.waze.com/ul?ll=50.85,4.35"]
    # a longer path, a longer domain, inside a word, a domain that is no Google one, no path, a search
    assert rre.maps_link("google.com/mapsearch") == []
    assert rre.maps_link("waze.company/x") == []
    assert rre.maps_link("notgoogle.com/maps/x") == []
    assert rre.maps_link("https://google.evil/maps/x") == []
    assert rre.maps_link("https://www.google.com/maps") == []
    assert rre.maps_link("https://maps.apple.com") == []
    assert rre.maps_link("https://www.google.com/search?q=maps+brussels") == []


def test_hard_mmsi():
    # MID 200 is not allocated: no real ship
    assert rre.mmsi("SAR aircraft MMSI 111200123") == ["MMSI 111200123"]
    assert rre.mmsi("(MMSI: 982001234)") == ["MMSI: 982001234"]
    # no MID, MID 99x and 81x, eight and ten digits, another keyword
    assert rre.mmsi("MMSI 000123456") == []
    assert rre.mmsi("MMSI 990123456") == []
    assert rre.mmsi("MMSI 812345678") == []
    assert rre.mmsi("MMSI 20012345") == []
    assert rre.mmsi("MMSI: 2001234560") == []
    assert rre.mmsi("IMO 200123456") == []
    assert rre.mmsi("MMSI 100123456") == []


def test_hard_multiple_punctuation():
    # for emphasis, trailing off and emoticons in messages
    assert rre.multiple_punctuation("what?!?!") == ["?!?!"]
    assert rre.multiple_punctuation("wait...") == ["..."]
    assert rre.multiple_punctuation("great :-)") == [":-)"]
    assert rre.multiple_punctuation("NO!!! and why??") == ["!!!", "??"]
    assert rre.multiple_punctuation("¿¡Qué!!") == ["!!"]
    assert rre.multiple_punctuation("line ---- break") == ["----"]
    # single marks: abbreviations, decimals, apostrophes, hyphens, quotes, a hashtag, thousands
    assert rre.multiple_punctuation("e.g. this") == []
    assert rre.multiple_punctuation("pi is 3.14") == []
    assert rre.multiple_punctuation("don't") == []
    assert rre.multiple_punctuation("a-b-c") == []
    assert rre.multiple_punctuation('"quoted"') == []
    assert rre.multiple_punctuation("#hashtag") == []
    assert rre.multiple_punctuation("1,000,000") == []


def test_hard_plus_code():
    # made up, apart from the Open Location Code examples
    assert rre.plus_code("8FVC9G8F+6XR") == ["8FVC9G8F+6XR"]
    assert rre.plus_code("(9G8F+6X)") == ["9G8F+6X"]
    assert rre.plus_code("https://plus.codes/8FVC9G8F+6X") == ["8FVC9G8F+6X"]
    assert rre.plus_code("Location: 9F4MGC2P+QV Amsterdam") == ["9F4MGC2P+QV"]
    assert rre.plus_code("CWC8+R9, Mountain View") == ["CWC8+R9"]
    # one character after +, letters outside the alphabet, inside a word, lowercase, a + after
    assert rre.plus_code("8FVC9G8F+6") == []
    assert rre.plus_code("8FVC9G8F+6XAB") == []
    assert rre.plus_code("A8FVC9G8F+6X") == []
    assert rre.plus_code("8fvc9g8f+6x") == []
    assert rre.plus_code("8IVC9G8F+6X") == []
    assert rre.plus_code("9G8F+6X+") == []


def test_hard_rfc2822_datetime():
    # a one-digit hour, second 60
    assert rre.rfc2822_datetime("Tue, 3 Mar 2026 9:12:44 +0100") == []
    assert rre.rfc2822_datetime("3 Mar 2026 09:12:60 +0100") == []


def test_hard_un_number():
    # a letter after, after the, above 3999, five digits, inside a word, lowercase, in UNIT
    assert rre.un_number("UN 1203a") == []
    assert rre.un_number("the UN 1945 charter") == []
    assert rre.un_number("UN 4123") == []
    assert rre.un_number("UN 12034") == []
    assert rre.un_number("FUN 1203") == []
    assert rre.un_number("un 1203") == []
    assert rre.un_number("UNIT 1203") == []


def test_hard_unix_timestamp():
    # a key that is an id, 9 digits before 2000, 14 digits, 2041, 1999, an id
    assert rre.unix_timestamp('{"update_id": 987654321}') == []
    assert rre.unix_timestamp("timestamp: 177240960") == []
    assert rre.unix_timestamp("timestamp: 17724096001234") == []
    assert rre.unix_timestamp("time: 2240611200") == []
    assert rre.unix_timestamp("ts=946684799") == []
    assert rre.unix_timestamp("id=1772409600") == []
    # but a key that ends in id as a word does count
    assert rre.unix_timestamp('"date_paid": 1772409600') == ['"date_paid": 1772409600']


def test_hard_ups_tracking_number():
    # 1Z999AA10123456784 is UPS's own test number; the others are made up
    assert rre.ups_tracking_number("1Z12345E0205271686") == ["1Z12345E0205271686"]
    assert rre.ups_tracking_number("(1Z4X57Y8A901234565)") == ["1Z4X57Y8A901234565"]
    assert rre.ups_tracking_number("?tracknum=1Z12345E0205271686&x") == ["1Z12345E0205271686"]
    assert rre.ups_tracking_number("1ZA1B2C3D4E5F6G7H0.") == ["1ZA1B2C3D4E5F6G7H0"]
    assert rre.ups_tracking_number('{"tracking": "1Z999AA10123456784"}') == ["1Z999AA10123456784"]
    assert rre.ups_tracking_number("UPS 1Z 12345E 02 0527 168 6") == ["1Z 12345E 02 0527 168 6"]
    # lowercase, inside a word, 19 and 17 characters, check digit wrong, a letter as check digit, 2Z
    assert rre.ups_tracking_number("1z12345e0205271686") == []
    assert rre.ups_tracking_number("X1Z12345E0205271686") == []
    assert rre.ups_tracking_number("1Z12345E02052716861") == []
    assert rre.ups_tracking_number("1Z12345E020527168") == []
    assert rre.ups_tracking_number("1Z12345E0205271687") == []
    assert rre.ups_tracking_number("1Z12345E020527168A") == []
    assert rre.ups_tracking_number("2Z12345E0205271686") == []


def test_hard_upu_tracking_number():
    # made up
    assert rre.upu_tracking_number("EE987654326NL") == ["EE987654326NL"]
    assert rre.upu_tracking_number("EE 987 654 326 NL") == ["EE 987 654 326 NL"]
    assert rre.upu_tracking_number("parcel CP111222332DE.") == ["CP111222332DE"]
    assert rre.upu_tracking_number("(LX555666772LU)") == ["LX555666772LU"]
    assert rre.upu_tracking_number("?barcode=RA000000014BE&lang=nl") == ["RA000000014BE"]
    # lowercase, 8 and 10 digits, inside a word, a one-letter country, check digit wrong, a digit as letter
    assert rre.upu_tracking_number("ee987654326nl") == []
    assert rre.upu_tracking_number("EE98765432NL") == []
    assert rre.upu_tracking_number("EE9876543261NL") == []
    assert rre.upu_tracking_number("XEE987654326NL") == []
    assert rre.upu_tracking_number("EE987654326N") == []
    assert rre.upu_tracking_number("EE987654327NL") == []
    assert rre.upu_tracking_number("E1987654326NL") == []


def test_hard_usps_tracking_number():
    # 21 and 23 digits, FedEx's 96
    assert rre.usps_tracking_number("9400 1123 4567 8901 2345 6") == []
    assert rre.usps_tracking_number("92055000000012345678961") == []
    assert rre.usps_tracking_number("9611 0201 2345 6776 5432 18") == []


def test_hard_vin():
    # made up
    assert rre.vin("WVWZZZ1JZXW000001") == ["WVWZZZ1JZXW000001"]
    assert rre.vin("VIN: VF1RFB00X56789012.") == ["VF1RFB00X56789012"]
    assert rre.vin('{"vin":"JH4KA7650MC012345"}') == ["JH4KA7650MC012345"]
    assert rre.vin("(SALLAAA146A123456)") == ["SALLAAA146A123456"]
    assert rre.vin("chassis no. TMBZZZ1Z0C1234567") == ["TMBZZZ1Z0C1234567"]
    assert rre.vin("registered with VIN 2T1BURHE0JC123456") == ["2T1BURHE0JC123456"]
    # a SEPA creditor ID, 16 and 18 characters, an O and an I, lowercase, digits only
    assert rre.vin("BE81ZZZ0123456749") == []
    assert rre.vin("1M8GDM9AXKP04278") == []
    assert rre.vin("1M8GDM9AXKP0427881") == []
    assert rre.vin("1M8GDM9AXKP04278O") == []
    assert rre.vin("IM8GDM9AXKP042788") == []
    assert rre.vin("1m8gdm9axkp042788") == []
    assert rre.vin("12345678901234567") == []


def test_hard_webkit_timestamp():
    # 1999
    assert rre.webkit_timestamp("WebKit timestamp: 12591150000000000") == []


def test_hard_what3words():
    # made up
    assert rre.what3words("///индекс.дом.плот") == ["///индекс.дом.плот"]
    assert rre.what3words("https://what3words.com/filled.count.soap") == ["https://what3words.com/filled.count.soap"]
    assert rre.what3words("www.w3w.co/Filled.Count.Soap") == ["www.w3w.co/Filled.Count.Soap"]
    assert rre.what3words("(///index.home.raft)") == ["///index.home.raft"]
    assert rre.what3words("meet at ///filled.count.soap.") == ["///filled.count.soap"]
    assert rre.what3words('"w3w": "///index.home.raft"') == ["///index.home.raft"]
    # two slashes, w3w.com, inside a word, two and four words, a digit after
    assert rre.what3words("//filled.count.soap") == []
    assert rre.what3words("w3w.com/filled.count.soap") == []
    assert rre.what3words("notw3w.co/filled.count.soap") == []
    assert rre.what3words("///filled.count") == []
    assert rre.what3words("///four.words.in.row") == []
    assert rre.what3words("///filled.count.soap1") == []


def test_hard_windows_timezone_name():
    # offset 15, minute 60, a time in front, lowercase, no colon, no brackets
    assert rre.windows_timezone_name("(UTC+15:00) Nowhere") == []
    assert rre.windows_timezone_name("(UTC+01:60) Brussels") == []
    assert rre.windows_timezone_name("12:00 (UTC+01:00) Brussels") == []
    assert rre.windows_timezone_name("(UTC+01:00) brussels") == []
    assert rre.windows_timezone_name("(UTC+0100) Brussels") == []
    assert rre.windows_timezone_name("UTC+01:00 Brussels") == []


def test_hard_regexes_stay_fast():
    start = time.perf_counter()
    for text in ('1/1/2026 1:01:01' * 6000, '1/1, ' * 20000, "51°03'" * 15000, 'IMO No ' * 14000, 'a_id: ' * 16000,
                 'PNR NUMBER ' * 9000, 'AWB "' * 20000, 'Mode S ' * 14000, 'google.co.' * 10000, '///a.b' * 16000,
                 '1.2345, ' * 12000, 'EAN": "' * 14000, 'ISBN": "1' * 11000, 'BE81ZZZ' * 14000, '1' * 100000):
        for f in (rre.cellebrite_datetime, rre.exif_gps_rational, rre.gps_dms, rre.imo_number, rre.unix_timestamp,
                  rre.booking_reference, rre.air_waybill, rre.aircraft_icao_address, rre.maps_link, rre.what3words,
                  rre.gps_coordinates, rre.gtin, rre.isbn, rre.vin):
            one = time.perf_counter()
            f(text)
            assert time.perf_counter() - one < 0.2, (f, text[:20])
    assert time.perf_counter() - start < 3


# hardening, phones and SIM cards, messaging and social media, web and network: every value made up, addresses from
# RFC 5737, RFC 3849 and RFC 7042, ASNs from RFC 5398, domains under example.*


def test_hard_asn():
    assert rre.asn("origin: AS64496") == ["AS64496"]
    assert rre.asn("(AS64511), 'AS65536' and \"AS65551\".") == ["AS64511", "AS65536", "AS65551"]
    assert rre.asn("ASN#64500 ASN:64501") == ["ASN#64500", "ASN:64501"]
    assert rre.asn("{'asn': 'AS64502'}") == ["'asn': 'AS64502'"]
    assert rre.asn("Autonomous System Number: 64503") == ["Autonomous System Number: 64503"]
    assert rre.asn("https://bgp.example.net/AS64504") == ["AS64504"]
    # the aerospace quality standard, a leading zero, a letter after, a space, a hyphen, above 32 bits
    assert rre.asn("AS9100:2016 certified") == []
    assert rre.asn("AS064496") == []
    assert rre.asn("AS64496x") == []
    assert rre.asn("AS 64496") == []
    assert rre.asn("AS-64496") == []
    assert rre.asn("AS4294967296") == []


def test_hard_automated_message_text():
    assert rre.automated_message_text("THIS IS AN AUTOMATED EMAIL") == ["AUTOMATED EMAIL"]
    assert rre.automated_message_text("(auto-generated) Do not reply to this message.") == [
        "auto-generated", "Do not reply to this"]
    assert rre.automated_message_text("This message was autogenerated") == ["autogenerated"]
    assert rre.automated_message_text("Ce courriel a été généré automatiquement.") == ["généré automatiquement"]
    assert rre.automated_message_text("Diese Nachricht wurde automatisch erstellt. Bitte nicht antworten!") == [
        "automatisch erstellt", "Bitte nicht antworten"]
    assert rre.automated_message_text('"Dit is een automatisch gegenereerd bericht, gelieve niet te antwoorden"') == [
        "automatisch gegenereerd", "niet te antwoorden"]
    assert rre.automated_message_text("Subject: automatically sent\nAntworten Sie nicht") == [
        "automatically sent", "Antworten Sie nicht"]
    # a renewal or a door done automatically, other words
    assert rre.automated_message_text("Votre abonnement sera renouvelé automatiquement") == []
    assert rre.automated_message_text("la porte est verrouillée automatiquement") == []
    assert rre.automated_message_text("an automated teller machine") == []
    assert rre.automated_message_text("the email was sent automatically by mistake") == []
    assert rre.automated_message_text("ne pas oublier de répondre") == []
    assert rre.automated_message_text("niet te geloven, bitte nicht stören") == []
    assert rre.automated_message_text("please reply, do not replace") == []


def test_hard_bluesky_handle():
    assert rre.bluesky_handle("Bluesky:jane.example.net") == ["Bluesky:jane.example.net"]
    assert rre.bluesky_handle('<a href="https://bsky.app/profile/jane.example.com/post/3kabc">') == [
        "https://bsky.app/profile/jane.example.com"]
    # inside a mail address, a longer word or domain, a did:plc too short, a leading hyphen, no domain
    assert rre.bluesky_handle("x@jane.bsky.social") == []
    assert rre.bluesky_handle("jane.bsky.socialx") == []
    assert rre.bluesky_handle("jane.bsky.social.example") == []
    assert rre.bluesky_handle("bsky.app/profile/did:plc:abcdefghijklmnopqrstuv") == []
    assert rre.bluesky_handle("@-jane.bsky.social") == []
    assert rre.bluesky_handle("Bluesky: jane") == []


def test_hard_cidr_range():
    assert rre.cidr_range("route 2001:db8:abcd::/48 via") == ["2001:db8:abcd::/48"]
    assert rre.cidr_range("(203.0.113.0/24)") == ["203.0.113.0/24"]
    # a letter after, inside a word, three parts, a second slash, a space, a leading zero
    assert rre.cidr_range("10.0.0.0/8a") == []
    assert rre.cidr_range("a10.0.0.0/8") == []
    assert rre.cidr_range("10.0.0/8") == []
    assert rre.cidr_range("192.0.2.0/24/") == []
    assert rre.cidr_range("10.0.0.0/ 8") == []
    assert rre.cidr_range("2001:db8::/0129") == []


def test_hard_discord_invite():
    assert rre.discord_invite("join discord.gg/AbCd12") == ["discord.gg/AbCd12"]
    assert rre.discord_invite("(https://discord.com/invite/abc-123).") == ["https://discord.com/invite/abc-123"]
    assert rre.discord_invite("DISCORD.GG/xyz789, discordapp.com/invite/Example_Server") == [
        "DISCORD.GG/xyz789", "discordapp.com/invite/Example_Server"]
    assert rre.discord_invite('"https://www.discord.com/invite/qwerty"') == ["https://www.discord.com/invite/qwerty"]
    assert rre.discord_invite("http://discord.gg/zz9?event=1") == ["http://discord.gg/zz9"]
    # no code, a channel, another domain ending in discord, discord.gg as a subdomain, no slash
    assert rre.discord_invite("discord.gg/") == []
    assert rre.discord_invite("discord.com/channels/412345678901234567/412345678901234568") == []
    assert rre.discord_invite("evil-discord.gg/abc123") == []
    assert rre.discord_invite("mydiscord.gg/abc123") == []
    assert rre.discord_invite("discord.gg.example.com/abc123") == []
    assert rre.discord_invite("discord.gg abc123") == []


def test_hard_discord_user_id():
    # 16 and 20 digits, a letter in the mention, a channel link, inside a word, no keyword
    assert rre.discord_user_id("discord.com/users/4123456789012345") == []
    assert rre.discord_user_id("discord_id=41234567890123456789") == []
    assert rre.discord_user_id("<@412345678901234567x>") == []
    assert rre.discord_user_id("discord.com/channels/412345678901234567") == []
    assert rre.discord_user_id("mydiscord 412345678901234567") == []
    assert rre.discord_user_id("id 412345678901234567") == []


def test_hard_drug_emoji():
    assert rre.drug_emoji("⛄ and ☃️") == ["⛄", "☃️"]
    assert rre.drug_emoji("(\U0001F489)\U0001F341.") == ["\U0001F489", "\U0001F341"]
    # other snowflakes, a clover, a battery, a herb, a hundred points
    assert rre.drug_emoji("❅") == []
    assert rre.drug_emoji("❆") == []
    assert rre.drug_emoji("\U0001F340") == []
    assert rre.drug_emoji("\U0001F50B") == []
    assert rre.drug_emoji("\U0001F33F") == []
    assert rre.drug_emoji("\U0001F4AF") == []


def test_hard_email():
    assert rre.email("Mail: Jan.Peeters@Example.BE") == ["Jan.Peeters@Example.BE"]
    assert rre.email("<jan_peeters@mail.example.com>") == ["jan_peeters@mail.example.com"]
    assert rre.email("mailto:info@example.org?subject=x") == ["info@example.org"]
    assert rre.email('{"email": "jan+tag@example.co.uk"}') == ["jan+tag@example.co.uk"]
    assert rre.email("From: jan-peeters@sub-domain.example.net.") == ["jan-peeters@sub-domain.example.net"]
    assert rre.email("schrijf naar józef@müller.example") == ["józef@müller.example"]
    # no top-level domain, a one-letter or numbered one, an underscore in the domain, a fediverse handle,
    # a WhatsApp JID, an IP address, a Telegram media file name
    assert rre.email("jan@example") == []
    assert rre.email("jan@example.c") == []
    assert rre.email("jan@example.com1") == []
    assert rre.email("jan@exa_mple.com") == []
    assert rre.email("@jane@mastodon.example") == []
    assert rre.email("32470123456@s.whatsapp.net, 120363012345678901@g.us") == []
    assert rre.email("jan@192.0.2.10") == []
    assert rre.email("audio_2@03-03-2026_09-12-44.ogg") == []


def test_hard_esim_eid():
    assert rre.esim_eid("eUICC: 89033023123456789012345678901212") == ["eUICC: 89033023123456789012345678901212"]
    # hyphens, another keyword, 31 digits, a wrong check
    assert rre.esim_eid("EID: 8904-9032-1234-5123-4512-3456-7890-1235") == []
    assert rre.esim_eid("IMEI: 89049032123451234512345678901235") == []
    assert rre.esim_eid("EID: 8904903212345123451234567890123") == []
    assert rre.esim_eid("EID 89044045111122223333444455556677") == []


def test_hard_esn():
    assert rre.esn("esn 1A2B3C4D") == ["esn 1A2B3C4D"]
    assert rre.esn("ESN(HEX): 9F1E2D3C, pESN: 80FEDCBA") == ["ESN(HEX): 9F1E2D3C", "pESN: 80FEDCBA"]
    assert rre.esn("ESN DEC 12816777215") == ["ESN DEC 12816777215"]
    assert rre.esn("(ESN=255 00000001)") == ["ESN=255 00000001"]
    assert rre.esn("ESN_HEX=8A1B2C3D") == ["ESN_HEX=8A1B2C3D"]
    # the decimal serial above 24 bits, 7 and 9 hex digits, a letter after, the manufacturer above 255,
    # a year, inside a word
    assert rre.esn("ESN 128 16777216") == []
    assert rre.esn("ESN: 80ABCDE") == []
    assert rre.esn("ESN: 80ABCDEFA") == []
    assert rre.esn("ESN: 80ABCDEG") == []
    assert rre.esn("ESN 25612345678") == []
    assert rre.esn("Erasmus ESN 2024") == []
    assert rre.esn("LESN: 80ABCDEF") == []


def test_hard_file_share_link():
    assert rre.file_share_link("https://www.dropbox.com/s/abc123/file.pdf?dl=0.") == [
        "https://www.dropbox.com/s/abc123/file.pdf?dl=0"]
    assert rre.file_share_link("MEGA.NZ/folder/AbCd#EfGh") == ["MEGA.NZ/folder/AbCd#EfGh"]
    assert rre.file_share_link("(1drv.ms/u/s!AbCd) https://gofile.io/d/AbC123") == [
        "1drv.ms/u/s!AbCd", "https://gofile.io/d/AbC123"]
    assert rre.file_share_link('"https://drive.proton.me/urls/ABCD#efgh"') == ["https://drive.proton.me/urls/ABCD#efgh"]
    # another domain ending in it, a longer domain, the site itself, no file
    assert rre.file_share_link("evil-mega.nz/file/Ab#Cd") == []
    assert rre.file_share_link("notpastebin.com/AbCd") == []
    assert rre.file_share_link("pastebin.com.example/AbCd") == []
    assert rre.file_share_link("drive.google.com/") == []
    assert rre.file_share_link("dropbox.com/home") == []
    assert rre.file_share_link("mega.nz/about") == []


def test_hard_hashtag():
    assert rre.hashtag("#Coke and #weed420") == ["#Coke", "#weed420"]
    assert rre.hashtag("(#420blazeit)") == ["#420blazeit"]
    assert rre.hashtag('"#party"') == ["#party"]
    assert rre.hashtag("#東京2020") == ["#東京2020"]
    assert rre.hashtag("Tags:#love,#summer.") == ["#love", "#summer"]
    assert rre.hashtag("#B2B #café") == ["#B2B", "#café"]
    # digits only, inside a word, a hex color, a URL fragment, an HTML entity, C# and F#, a double #
    assert rre.hashtag("#420") == []
    assert rre.hashtag("x#y") == []
    assert rre.hashtag("#1A2B3C") == []
    assert rre.hashtag("color: #ff000080") == []
    assert rre.hashtag("https://example.com/#section") == []
    assert rre.hashtag("&#x27;") == []
    assert rre.hashtag("C# and F#") == []
    assert rre.hashtag("##double") == []


def test_hard_iccid():
    assert rre.iccid("ICCID: 89320112345678901232") == ["89320112345678901232"]
    assert rre.iccid("iccid=8932011234567890122;") == ["8932011234567890122"]
    assert rre.iccid('"iccid": "89310412345678901230"') == ["89310412345678901230"]
    assert rre.iccid("(894902000012345679)") == ["894902000012345679"]
    assert rre.iccid("SIM 8944100000000000018, 8935201123456789011") == ["8944100000000000018", "8935201123456789011"]
    # a wrong check digit, 17 and 21 digits, another prefix, inside a longer number, spaced, padded with F
    assert rre.iccid("89320112345678901233") == []
    assert rre.iccid("89330112345678905") == []
    assert rre.iccid("893201123456789012320") == []
    assert rre.iccid("88320112345678901232") == []
    assert rre.iccid("1289320112345678901232") == []
    assert rre.iccid("8932 0112 3456 7890 1232") == []
    assert rre.iccid("8932011234567890122F") == []


def test_hard_imei():
    assert rre.imei("IMEI: 490154203237518,") == ["490154203237518"]
    assert rre.imei("imei=356938035643809;") == ["356938035643809"]
    assert rre.imei("(352099001761481)") == ["352099001761481"]
    assert rre.imei('{"imei":"351234567890124"}') == ["351234567890124"]
    assert rre.imei("IMEI1 860123456789014 / IMEI2 990000123456784") == ["860123456789014", "990000123456784"]
    # 14 and 16 digits, dashes, spaces, inside a word
    assert rre.imei("49015420323751") == []
    assert rre.imei("4901542032375180") == []
    assert rre.imei("IMEI 35-209900-176148-1") == []
    assert rre.imei("490154 203237 518") == []
    assert rre.imei("x490154203237518") == []
    assert rre.imei("490154203237518x") == []


def test_hard_imeisv():
    assert rre.imeisv("IMEISV 3520990017614823") == ["IMEISV 3520990017614823"]
    assert rre.imeisv("imei-sv: 35 209900 176148 23") == ["imei-sv: 35 209900 176148 23"]
    assert rre.imeisv("IMEI SVN: 3520990017614823") == ["IMEI SVN: 3520990017614823"]
    # 15 and 17 digits, an IMEI keyword, other groups, no keyword, inside a word
    assert rre.imeisv("IMEISV: 352099001761482") == []
    assert rre.imeisv("IMEISV: 35209900176148234") == []
    assert rre.imeisv("IMEI: 3520990017614823") == []
    assert rre.imeisv("IMEISV 35 2099 0017 6148 23") == []
    assert rre.imeisv("SV: 3520990017614823") == []
    assert rre.imeisv("XIMEISV: 3520990017614823") == []


def test_hard_ip_address():
    assert rre.ip_address("192.0.2.1:8080") == ["192.0.2.1"]
    assert rre.ip_address("(198.51.100.7)") == ["198.51.100.7"]
    assert rre.ip_address("http://203.0.113.10/login") == ["203.0.113.10"]
    assert rre.ip_address("X-Forwarded-For: 192.0.2.44, 198.51.100.2") == ["192.0.2.44", "198.51.100.2"]
    assert rre.ip_address("listen 0.0.0.0, lookup https://ip.example.com/check/192.0.2.9") == ["0.0.0.0", "192.0.2.9"]
    # a browser version in a user agent, a number above 255, three parts, a version, five parts, inside a word
    assert rre.ip_address("Mozilla/5.0 (X11) Chrome/120.0.0.0 Safari/537.36") == []
    assert rre.ip_address("192.0.2.256") == []
    assert rre.ip_address("192.0.2") == []
    assert rre.ip_address("v1.2.3.4") == []
    assert rre.ip_address("192.0.2.1.5") == []
    assert rre.ip_address("a192.0.2.1") == []


def test_hard_ipv6():
    assert rre.ipv6("[2001:db8::1]:443") == ["2001:db8::1"]
    assert rre.ipv6("ping ::1") == ["::1"]
    assert rre.ipv6("::ffff:192.0.2.1 (mapped)") == ["::ffff:192.0.2.1"]
    assert rre.ipv6("2001:DB8:0:0:8:800:200C:417A") == ["2001:DB8:0:0:8:800:200C:417A"]
    assert rre.ipv6("fe80::1%eth0") == ["fe80::1"]
    assert rre.ipv6('"2001:db8:85a3::8a2e:370:7334",') == ["2001:db8:85a3::8a2e:370:7334"]
    # a separator, a time, a MAC address, two ::, a five-digit group, a cut-off IPv4 part, nine groups
    assert rre.ipv6("Home :: About") == []
    assert rre.ipv6("12:30:45") == []
    assert rre.ipv6("00:00:5E:00:53:01") == []
    assert rre.ipv6("2001:db8::1::2") == []
    assert rre.ipv6("12345::1") == []
    assert rre.ipv6("::ffff:192.0.2") == []
    assert rre.ipv6("1:2:3:4:5:6:7:8:9") == []


def test_hard_mac_address():
    assert rre.mac_address("00:00:5E:00:53:01") == ["00:00:5E:00:53:01"]
    assert rre.mac_address("bssid=00-00-5e-00-53-af;") == ["00-00-5e-00-53-af"]
    assert rre.mac_address("MAC:00:00:5E:00:53:0A") == ["00:00:5E:00:53:0A"]
    assert rre.mac_address("(00:00:5E:00:53:FF)") == ["00:00:5E:00:53:FF"]
    assert rre.mac_address("HWaddr 00:00:5E:00:53:20 up") == ["00:00:5E:00:53:20"]
    assert rre.mac_address('{"wlan0": "00:00:5E:00:53:30"}') == ["00:00:5E:00:53:30"]
    # an SSH key fingerprint, mixed separators, five pairs, an EUI-64, a G, a placeholder
    assert rre.mac_address("MD5:43:51:43:a1:b5:fc:8b:b7:0a:3a:a9:b1:0f:66:73:a8") == []
    assert rre.mac_address("00:00-5E:00-53:01") == []
    assert rre.mac_address("00:00:5E:00:53") == []
    assert rre.mac_address("02-00-5E-10-00-00-00-01") == []
    assert rre.mac_address("00:00:5E:00:53:0G") == []
    assert rre.mac_address("02:00:00:00:00:00") == []


def test_hard_machine_sender():
    assert rre.machine_sender("<NoReply@Example.COM>") == ["NoReply@Example.COM"]
    # no top-level domain, the word inside another, a plural, a longer word, no domain, a person
    assert rre.machine_sender("noreply@example") == []
    assert rre.machine_sender("anoreply@example.com") == []
    assert rre.machine_sender("noreplies@example.com") == []
    assert rre.machine_sender("alertsystem@example.com") == []
    assert rre.machine_sender("notifications@") == []
    assert rre.machine_sender("jan.peeters@example.com") == []


def test_hard_magnet_link():
    v2 = "magnet:?xt=urn:btmh:1220" + "0123456789abcdef" * 4
    assert rre.magnet_link(v2) == [v2]
    assert rre.magnet_link("(magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=a)") == [
        "magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567&dn=a"]
    assert rre.magnet_link('"magnet:?xt=urn:btih:0123456789ABCDEF0123456789ABCDEF01234567&tr=udp://tracker.example.org:1337"') == [
        "magnet:?xt=urn:btih:0123456789ABCDEF0123456789ABCDEF01234567&tr=udp://tracker.example.org:1337"]
    assert rre.magnet_link("get magnet:?xt=urn:btih:abcdefghijklmnopqrstuvwxyz234567!") == [
        "magnet:?xt=urn:btih:abcdefghijklmnopqrstuvwxyz234567"]
    # 41 hex, 31 base32, a 1 in base32, another multihash, another urn, inside a word
    assert rre.magnet_link("magnet:?xt=urn:btih:0123456789abcdef0123456789abcdef012345678") == []
    assert rre.magnet_link("magnet:?xt=urn:btih:ABCDEFGHIJKLMNOPQRSTUVWXYZ23456") == []
    assert rre.magnet_link("magnet:?xt=urn:btih:ABCDEFGHIJKLMNOPQRSTUVWXYZ234561") == []
    assert rre.magnet_link("magnet:?xt=urn:btmh:1120" + "0" * 64) == []
    assert rre.magnet_link("magnet:?xt=urn:sha1:0123456789abcdef0123456789abcdef01234567") == []
    assert rre.magnet_link("xmagnet:?xt=urn:btih:0123456789abcdef0123456789abcdef01234567") == []


def test_hard_mastodon_handle():
    # no top-level domain, a mail provider, a dot before or after the name
    assert rre.mastodon_handle("@jane@mastodon") == []
    assert rre.mastodon_handle("@jane@proton.me") == []
    assert rre.mastodon_handle("@jane.@m.example.org") == []
    assert rre.mastodon_handle("@.jane@m.example.org") == []


def test_hard_matrix_id():
    assert rre.matrix_id('"@bob_1:matrix.example.net:8448"') == ["@bob_1:matrix.example.net:8448"]
    assert rre.matrix_id("https://matrix.to/#/@carol:example.com") == ["@carol:example.com"]
    assert rre.matrix_id("(@dave.smith:example.org)") == ["@dave.smith:example.org"]
    assert rre.matrix_id("MATRIX: @Erin:Example.ORG") == ["@Erin:Example.ORG"]
    # a room alias, a room ID, a digit after the domain, inside a word, no top-level domain, a space
    assert rre.matrix_id("#room:example.org") == []
    assert rre.matrix_id("!abcdef:example.org") == []
    assert rre.matrix_id("@alice:example.org1") == []
    assert rre.matrix_id("x@alice:example.org") == []
    assert rre.matrix_id("@alice:example") == []
    assert rre.matrix_id("@alice: example.org") == []


def test_hard_mcc_mnc():
    # a 4-digit network code, 4 digits after PLMN, a 4-digit country code, no network code,
    # a country code not assigned, no keyword
    assert rre.mcc_mnc("MCC 206 MNC 1234") == []
    assert rre.mcc_mnc("PLMN 2061") == []
    assert rre.mcc_mnc("MCC 2060 MNC 01") == []
    assert rre.mcc_mnc("mcc 206") == []
    assert rre.mcc_mnc("PLMN: 19901") == []
    assert rre.mcc_mnc("operator 20601") == []


def test_hard_meid():
    assert rre.meid("meid=A0000000002329") == ["meid=A0000000002329"]
    # hex starting below A0, 13 digits, a G after, the decimal manufacturer code above 32 bits, another keyword
    assert rre.meid("MEID: 9A0000009296F2") == []
    assert rre.meid("MEID 1234567890123") == []
    assert rre.meid("MEID: A10000009296F2G") == []
    assert rre.meid("MEID DEC 429496729616777215") == []
    assert rre.meid("IMEI: A10000009296F2") == []


def test_hard_mention():
    assert rre.mention("(@jane_doe)") == ["@jane_doe"]
    assert rre.mention("thanks @news_bot.") == ["@news_bot"]
    assert rre.mention("follow @jane.doe on Instagram") == ["@jane.doe"]
    assert rre.mention('"@JaneDoe"') == ["@JaneDoe"]
    assert rre.mention("RT @józef: hi") == ["@józef"]
    assert rre.mention("@abc") == ["@abc"]
    # an e-mail address, too short, a fediverse handle (also with a dot), inside a word, a double @, a link
    assert rre.mention("jan@test.be") == []
    assert rre.mention("@ab") == []
    assert rre.mention("@jane@mastodon.example") == []
    assert rre.mention("@jane.doe@mastodon.example") == []
    assert rre.mention("x@abc") == []
    assert rre.mention("@@abc") == []
    assert rre.mention("tiktok.com/@jane.example") == []


def test_hard_onion_address():
    v3 = ["a" * 54 + "id", "b" * 54 + "qd", "z2" * 27 + "yd"]
    assert rre.onion_address(f"http://{v3[0]}.onion/path") == [f"{v3[0]}.onion"]
    assert rre.onion_address(f"(www.{v3[1]}.onion)") == [f"{v3[1]}.onion"]
    assert rre.onion_address(f'"{v3[2]}.onion"') == [f"{v3[2]}.onion"]
    assert rre.onion_address("old abcdefghij234567.onion and exampleonion2345.onion.") == [
        "abcdefghij234567.onion", "exampleonion2345.onion"]
    assert rre.onion_address(f"{v3[0]}.onion.example") == [f"{v3[0]}.onion"]
    # 55 and 57 characters, no version byte 3 at the end, an 8, 15 characters, .onions
    assert rre.onion_address("a" * 53 + "id.onion") == []
    assert rre.onion_address("a" * 55 + "id.onion") == []
    assert rre.onion_address("a" * 54 + "ab.onion") == []
    assert rre.onion_address("a" * 54 + "bd.onion") == []
    assert rre.onion_address("abcdefghij234568.onion") == []
    assert rre.onion_address("abcdefghij23456.onion") == []
    assert rre.onion_address(f"{v3[0]}.onions") == []


def test_hard_phone_e164():
    assert rre.phone_e164("call +32470123456.") == ["+32470123456"]
    assert rre.phone_e164("(+12015550123)") == ["+12015550123"]
    assert rre.phone_e164("tel. +33612345678, +31612345678") == ["+33612345678", "+31612345678"]
    assert rre.phone_e164('{"phone":"+4917612345678"}') == ["+4917612345678"]
    assert rre.phone_e164("+353851234567") == ["+353851234567"]
    # spaced, one digit short or long, a 0 after +, 00 instead of +, a letter after, too long
    assert rre.phone_e164("+32 470 12 34 56") == []
    assert rre.phone_e164("+3247012345") == []
    assert rre.phone_e164("+324701234567") == []
    assert rre.phone_e164("+0470123456") == []
    assert rre.phone_e164("0032470123456") == []
    assert rre.phone_e164("+32470123456x") == []
    assert rre.phone_e164("+12015550123456789") == []


def test_hard_reddit_user():
    # inside a word, no name, after r/, after a number (a unit)
    assert rre.reddit_user("xu/jane_doe") == []
    assert rre.reddit_user("https://reddit.com/user/") == []
    assert rre.reddit_user("r/u/jane_doe") == []
    assert rre.reddit_user("2 u/jane_doe") == []


def test_hard_search_query_url():
    # a map, no query, another site, an empty query, no dot
    assert rre.search_query_url("https://www.google.com/maps?q=test") == []
    assert rre.search_query_url("https://www.google.com/search?hl=en") == []
    assert rre.search_query_url("https://example.com/search?q=test") == []
    assert rre.search_query_url("https://www.google.com/search?q=") == []
    assert rre.search_query_url("googlexcom/search?q=test") == []


def test_hard_signal_link():
    assert rre.signal_link("sgnl://signal.me/#p/+32470123456") == ["sgnl://signal.me/#p/+32470123456"]
    assert rre.signal_link("(https://signal.me/#p/+12015550123).") == ["https://signal.me/#p/+12015550123"]
    # no #, 6 and 16 digits, inside a word, a short group key, no call key
    assert rre.signal_link("signal.me/p/+32470123456") == []
    assert rre.signal_link("signal.me/#p/+123456") == []
    assert rre.signal_link("signal.me/#p/+1234567890123456") == []
    assert rre.signal_link("xsignal.me/#p/+32470123456") == []
    assert rre.signal_link("https://signal.group/#short") == []
    assert rre.signal_link("signal.link/call/#key=") == []


def test_hard_simplex_link():
    key = "Ab1_" * 10 + "Cd2"
    # another link type, a short key, no #, no queue, no version
    assert rre.simplex_link(f"https://smp4.simplex.im/b#{key}") == []
    assert rre.simplex_link(f"simplex:/a#{key[:-2]}") == []
    assert rre.simplex_link(f"https://smp4.simplex.im/a{key}") == []
    assert rre.simplex_link("https://simplex.chat/invitation#/?v=2-7") == []
    assert rre.simplex_link("simplex.chat/contact#/?v=&smp=smp%3A%2F%2Fx") == []


def test_hard_sip_uri():
    assert rre.sip_uri("sip:alice@[2001:db8::1]:5060") == ["sip:alice@[2001:db8::1]:5060"]
    assert rre.sip_uri("sips:alice@example.com?subject=hi") == ["sips:alice@example.com?subject=hi"]
    assert rre.sip_uri("(sip:alice:secret@example.com)") == ["sip:alice:secret@example.com"]
    # no host, nothing, another scheme, nothing after @, a SIP status line
    assert rre.sip_uri("sip:alice") == []
    assert rre.sip_uri("sip:") == []
    assert rre.sip_uri("tip:alice@example.com") == []
    assert rre.sip_uri("sip:alice@") == []
    assert rre.sip_uri("SIP/2.0 200 OK") == []


def test_hard_skype_id():
    assert rre.skype_id("live:jane_1") == ["live:jane_1"]
    assert rre.skype_id("(8:live:jane.example)") == ["8:live:jane.example"]
    # 7 hex digits, a Skype name too short, a cut-off orgid, a leading hyphen, inside a word, an e-mail address
    assert rre.skype_id("live:.cid.1a2b3c4") == []
    assert rre.skype_id("8:jane") == []
    assert rre.skype_id("8:orgid:2f1a2b3c-4d5e-4f60-8a7b-9c0d1e2f3a4") == []
    assert rre.skype_id("live:-jane") == []
    assert rre.skype_id("xlive:jane") == []
    assert rre.skype_id("live:jane@example.com") == []


def test_hard_social_media_profile():
    assert rre.social_media_profile("https://twitter.com/jane_example?lang=en") == ["https://twitter.com/jane_example"]
    assert rre.social_media_profile("FACEBOOK.COM/jane.example") == ["FACEBOOK.COM/jane.example"]
    assert rre.social_media_profile("(youtube.com/@jane-example)") == ["youtube.com/@jane-example"]
    assert rre.social_media_profile("snapchat.com/add/jane.example.") == ["snapchat.com/add/jane.example"]
    assert rre.social_media_profile('"linkedin.com/company/example-bv"') == ["linkedin.com/company/example-bv"]
    assert rre.social_media_profile("youtube.com/channel/UCabc123") == ["youtube.com/channel/UCabc123"]
    # the site's pages, another domain, a one-letter LinkedIn name
    assert rre.social_media_profile("instagram.com/explore") == []
    assert rre.social_media_profile("x.com/search?q=a") == []
    assert rre.social_media_profile("xx.com/jane") == []
    assert rre.social_media_profile("x.com/i/flow/login") == []
    assert rre.social_media_profile("instagram.com/reels/abc") == []
    assert rre.social_media_profile("linkedin.com/in/a") == []


def test_hard_tel_uri():
    assert rre.tel_uri("mmsto:+32470123456?body=x") == ["mmsto:+32470123456?body=x"]
    assert rre.tel_uri("tel:0470123456,1234") == ["tel:0470123456,1234"]
    assert rre.tel_uri("sms://+32470123456") == ["sms://+32470123456"]
    # no number, only +, another scheme, a longer word, inside a word, letters
    assert rre.tel_uri("tel:") == []
    assert rre.tel_uri("tel:+") == []
    assert rre.tel_uri("callto:+32470123456") == []
    assert rre.tel_uri("telephone:+32470123456") == []
    assert rre.tel_uri("xtel:+32470123456") == []
    assert rre.tel_uri("tel:abc") == []


def test_hard_telegram_link():
    assert rre.telegram_link("T.ME/Example_Channel") == ["T.ME/Example_Channel"]
    assert rre.telegram_link("(https://t.me/+AbCdEf123)") == ["https://t.me/+AbCdEf123"]
    assert rre.telegram_link('"t.me/example_bot"') == ["t.me/example_bot"]
    # another domain ending in t, inside a word, 2 characters, a longer domain, no name, no slash
    assert rre.telegram_link("x-t.me/abcdef") == []
    assert rre.telegram_link("at.me/abcdef") == []
    assert rre.telegram_link("t.me/ab") == []
    assert rre.telegram_link("t.mex/abcdef") == []
    assert rre.telegram_link("https://t.me/") == []
    assert rre.telegram_link("t.me abcdef") == []


def test_hard_threema_link():
    assert rre.threema_link("threema.id/ECHOECHO") == ["threema.id/ECHOECHO"]
    assert rre.threema_link("https://threema.id/*ABCDEFG") == ["https://threema.id/*ABCDEFG"]
    assert rre.threema_link("(threema.id/ABCD1234)") == ["threema.id/ABCD1234"]
    assert rre.threema_link('"https://threema.id/X9Y8Z7W6?text=hi"') == ["https://threema.id/X9Y8Z7W6"]
    assert rre.threema_link("http://threema.id/QWERTY12.") == ["http://threema.id/QWERTY12"]
    # 7 characters, inside a word, a hyphen, two stars, another domain, no ID
    assert rre.threema_link("threema.id/ECHOECH") == []
    assert rre.threema_link("xthreema.id/ECHOECHO") == []
    assert rre.threema_link("threema.id/ECHO-ECHO") == []
    assert rre.threema_link("threema.id/**ABCDEF") == []
    assert rre.threema_link("threema.ch/ECHOECHO") == []
    assert rre.threema_link("threema.id/") == []


def test_hard_tox_id():
    # made up: the SHA-256 of a word as public key, nospam 0A1B2C3D and its checksum
    alpha = "8ED3F6AD685B959EAD7022518E1AF76CD816F8E8EC7CCDDA1ED4018E8F2223F80A1B2C3DE712"
    bravo = "F144A6907DC4284D1F9FE6A7D9B9FF53C02C1D07BA68F24D413D7FF7F757A7820A1B2C3D00B8"
    charlie = "B9DD960C1753459A78115D3CB845A57D924B6877E805B08BD01086CCDF34433C0A1B2C3D0B4D"
    assert rre.tox_id(f"Tox: {alpha}.") == [alpha]
    assert rre.tox_id(f'{{"tox": "{bravo.lower()}"}}') == [bravo.lower()]
    assert rre.tox_id(f"({charlie})") == [charlie]
    # a wrong checksum, one character short, 0x in front, the wrong checksum in lower case
    assert rre.tox_id(alpha[:-1] + "3") == []
    assert rre.tox_id(f"tox:{bravo[:-1]}") == []
    assert rre.tox_id(f"0x{charlie}") == []
    assert rre.tox_id((alpha[:-1] + "3").lower()) == []


def test_hard_unsubscribe_text():
    # other words that start or end alike, signing up
    assert rre.unsubscribe_text("subscriber count") == []
    assert rre.unsubscribe_text("the outcome") == []
    assert rre.unsubscribe_text("an option out of town") == []
    assert rre.unsubscribe_text("meld je aan") == []
    assert rre.unsubscribe_text("s'abonner, inscription") == []
    assert rre.unsubscribe_text("Abmahnung") == []


def test_hard_url():
    assert rre.url("HTTPS://WWW.EXAMPLE.COM/path") == ["HTTPS://WWW.EXAMPLE.COM"]
    assert rre.url("(example.org)") == ["example.org"]
    assert rre.url('"sub.example.co.uk"') == ["sub.example.co.uk"]
    assert rre.url("visit example.museum.") == ["example.museum"]
    assert rre.url("xn--bcher-kva.example/x and example.com/file.pdf") == ["xn--bcher-kva.example", "example.com"]
    # .zip and .mov are top-level domains too
    assert rre.url("download example.zip") == ["example.zip"]
    # camera and WhatsApp file names, a document, a JavaScript library, an Android package, a digit after,
    # a what3words address, an ENS name
    assert rre.url("DSC01234.JPG") == []
    assert rre.url("IMG-20260303-WA0007.jpg") == []
    assert rre.url("report.final.docx") == []
    assert rre.url("built with Node.js") == []
    assert rre.url("com.example.app") == []
    assert rre.url("example.com123") == []
    assert rre.url("///filled.count.soap") == []
    assert rre.url("jane-example.eth") == []


def test_hard_url_shortener_link():
    # another domain ending in it, a code too short, no dot, no slash, a maps link
    assert rre.url_shortener_link("x-bit.ly/abc") == []
    assert rre.url_shortener_link("bit.ly/ab") == []
    assert rre.url_shortener_link("bitly/abc") == []
    assert rre.url_shortener_link("bit.ly abc") == []
    assert rre.url_shortener_link("goo.gl/maps/AbCdEf") == []


def test_hard_user_agent():
    # no brackets
    assert rre.user_agent("Mozilla/5.0 X11; Linux x86_64") == []


def test_hard_ussd_code():
    # doubled at the end, # after **, no closing #, inside a number, a secret code not closed, a hashtag
    assert rre.ussd_code("##4636##") == []
    assert rre.ussd_code("**#21#") == []
    assert rre.ussd_code("*#06") == []
    assert rre.ussd_code("1*100#") == []
    assert rre.ussd_code("*#*#4636#*#") == []
    assert rre.ussd_code("#tbt#") == []


def test_hard_verification_code_message():
    # an exit code, a postcode, a promo code, a code sent, too short, too long
    assert rre.verification_code_message("exit code 137") == []
    assert rre.verification_code_message("zip code 10001") == []
    assert rre.verification_code_message("your postal code is 2000") == []
    assert rre.verification_code_message("promo code SPRING24") == []
    assert rre.verification_code_message("verification code sent to +32470123456") == []
    assert rre.verification_code_message("Your code: 12") == []
    assert rre.verification_code_message("Your code is 123456789") == []


def test_hard_whatsapp_jid():
    # another domain, a longer domain, a short group ID, 0, inside a word, a leading 0
    assert rre.whatsapp_jid("32470123456@example.com") == []
    assert rre.whatsapp_jid("32470123456@s.whatsapp.network") == []
    assert rre.whatsapp_jid("12345@g.us") == []
    assert rre.whatsapp_jid("0@s.whatsapp.net") == []
    assert rre.whatsapp_jid("x32470123456@s.whatsapp.net") == []
    assert rre.whatsapp_jid("032470123456@s.whatsapp.net") == []


def test_hard_whatsapp_link():
    assert rre.whatsapp_link("https://WA.ME/12015550123?text=hi") == ["https://WA.ME/12015550123"]
    assert rre.whatsapp_link("(https://chat.whatsapp.com/AbCdEfGhIjKlMnOpQrStUv)") == [
        "https://chat.whatsapp.com/AbCdEfGhIjKlMnOpQrStUv"]
    assert rre.whatsapp_link('"http://wa.me/33612345678"') == ["http://wa.me/33612345678"]
    assert rre.whatsapp_link("wa.me/31612345678.") == ["wa.me/31612345678"]
    # 5 and 16 digits, another domain ending in wa, a longer domain, a short invite, no number
    assert rre.whatsapp_link("wa.me/12345") == []
    assert rre.whatsapp_link("wa.me/3247012345678901") == []
    assert rre.whatsapp_link("x-wa.me/32470123456") == []
    assert rre.whatsapp_link("wa.mex/32470123456") == []
    assert rre.whatsapp_link("chat.whatsapp.com/AbCdEf") == []
    assert rre.whatsapp_link("wa.me/+") == []


def test_hard_messaging_web_regexes_stay_fast():
    hostile = ('a' * 100000, '1' * 100000, '@a' * 50000, 'a.' * 50000, '#1' * 50000, '0:' * 50000, ':' * 100000,
               '00:' * 33333, '1.' * 50000, 'AS1' * 33333, 'ESN 1' * 20000, 'a@b.' * 25000, '@a.' * 33333,
               '/1.0.0.0' * 12500, 'automatisch ' * 8000, 'é automatiquement ' * 5000, 't.me/' * 20000,
               'wa.me/1' * 14000, 'discord.gg/' * 9000, 'a' * 54 + 'id.onion ' * 1000 + 'a2' * 40000)
    for name in ('asn', 'automated_message_text', 'discord_invite', 'email', 'esn', 'hashtag', 'ip_address', 'ipv6',
                 'mac_address', 'mention', 'onion_address', 'telegram_link', 'url', 'whatsapp_link'):
        for text in hostile:
            start = time.perf_counter()
            getattr(rre, name)(text)
            assert time.perf_counter() - start < 0.2, (name, text[:20])


def test_overlap_ip_address_and_url():
    # zero-padded parts are a Belgian phone number or establishment number, not an IPv4 address
    assert rre.ip_address("070.25.25.25 and 3.000.000.162") == []
    assert rre.ip_address("from 192.0.2.10 and 10.0.0.1") == ["192.0.2.10", "10.0.0.1"]
    # camera raw files and media are no domains
    assert rre.url("DSCF1234.RAF, IMG_0001.CR3, clip.mp4, voice.m4a") == []
    assert rre.url("see politie.be") == ["politie.be"]
