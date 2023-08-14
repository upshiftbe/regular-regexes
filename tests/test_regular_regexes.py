from regular_regexes.regular_regexes import rre

def test_email():
    assert len(rre.email("test@test.com")) > 0