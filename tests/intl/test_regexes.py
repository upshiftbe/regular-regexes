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
    assert rre.whatsapp_link("chat via wa.me/32470123456") == ["wa.me/32470123456"]
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
