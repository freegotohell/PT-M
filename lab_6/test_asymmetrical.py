from asymmetrical import AsymmetricCryptography


def test_asymmetric_generate_and_roundtrip():
    priv, pub = AsymmetricCryptography.generate_key()
    data = b"test rsa"
    c = AsymmetricCryptography.encrypt(data, pub)
    dc = AsymmetricCryptography.decrypt(c, priv)
    assert dc == data
