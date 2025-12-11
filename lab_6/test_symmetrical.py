import pytest
from symmetrical import SymmetricCryptography


@pytest.mark.parametrize("key_size", [16, 24, 32])
@pytest.mark.parametrize("data", [b"", b"a", b"some long test data"])
def test_symmetric_encrypt_decrypt_roundtrip(key_size, data):
    key = SymmetricCryptography.generate_key(key_size)
    c = SymmetricCryptography.encrypt(data, key)
    dc = SymmetricCryptography.decrypt(c, key)
    assert dc == data


@pytest.mark.parametrize("bad_size", [0, 1, 15, 17, 25, 33])
def test_symmetric_wrong_key_size_raises(bad_size):
    key = b"\x00" * bad_size
    with pytest.raises(ValueError):
        SymmetricCryptography.encrypt(b"data", key)
