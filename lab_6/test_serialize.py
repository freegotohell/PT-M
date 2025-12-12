from serialize import Serialization
from asymmetrical import AsymmetricCryptography
from symmetrical import SymmetricCryptography


def test_save_load_symmetric_key(tmp_path):
    path = tmp_path / "sym.key"
    key = SymmetricCryptography.generate_key(16)
    Serialization.save_symmetric_key(str(path), key)
    loaded = Serialization.load_symmetric_key(str(path))
    assert loaded == key


def test_save_load_rsa_keys(tmp_path):
    priv, pub = AsymmetricCryptography.generate_key()
    priv_path = tmp_path / "priv.pem"
    pub_path = tmp_path / "pub.pem"

    Serialization.save_private_key(str(priv_path), priv)
    Serialization.save_public_key(str(pub_path), pub)

    loaded_priv = Serialization.load_private_key(str(priv_path))
    loaded_pub = Serialization.load_public_key(str(pub_path))

    msg = b"test rsa"
    c = AsymmetricCryptography.encrypt(msg, loaded_pub)
    dc = AsymmetricCryptography.decrypt(c, loaded_priv)
    assert dc == msg

    assert loaded_priv.key_size == priv.key_size
    assert loaded_pub.key_size == pub.key_size

