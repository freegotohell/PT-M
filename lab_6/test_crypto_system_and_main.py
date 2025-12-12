import pytest
from crypto_system import HybridCryptoSystem
from work_file import write_txt, read_txt, read_json
from serialize import Serialization
from asymmetrical import AsymmetricCryptography
from symmetrical import SymmetricCryptography
import main as main_module


def test_hybrid_encrypt_decrypt_cycle(tmp_path, monkeypatch):
    settings = {
        "initial_file": str(tmp_path / "plain.txt"),
        "encrypted_file": str(tmp_path / "enc.bin"),
        "decrypted_file": str(tmp_path / "dec.txt"),
        "symmetric_key": str(tmp_path / "sym.key"),
        "secret_key": str(tmp_path / "priv.pem"),
        "public_key": str(tmp_path / "pub.pem"),
    }
    (tmp_path / "settings.json").write_text(
        '{"initial_file": "%s", "encrypted_file": "%s", "decrypted_file": "%s", '
        '"symmetric_key": "%s", "secret_key": "%s", "public_key": "%s"}'
        % (settings["initial_file"], settings["encrypted_file"],
           settings["decrypted_file"], settings["symmetric_key"],
           settings["secret_key"], settings["public_key"]),
        encoding="utf-8",
    )
    text = "hybrid crypto test"
    write_txt(text, settings["initial_file"])

    h = HybridCryptoSystem(
        settings["symmetric_key"],
        settings["secret_key"],
        settings["public_key"],
    )

    h.generate_keys(16)
    h.encrypt(settings["initial_file"], settings["encrypted_file"])
    h.decrypt(settings["encrypted_file"], settings["decrypted_file"])

    assert read_txt(settings["decrypted_file"]) == text


@pytest.mark.parametrize(
    "argv",
    [
        ["prog", "-gen", "16"],
        ["prog", "-enc"],
        ["prog", "-dec"],
    ],
)
def test_main_cli_entry(monkeypatch, tmp_path, argv):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        '{"initial_file": "init.txt", "encrypted_file": "enc.bin", '
        '"decrypted_file": "dec.txt", "symmetric_key": "sym.key", '
        '"secret_key": "priv.pem", "public_key": "pub.pem"}',
        encoding="utf-8",
    )

    def fake_read_json(_):
        import json
        return json.loads(settings_path.read_text(encoding="utf-8"))

    monkeypatch.setattr("main.read_json", fake_read_json)

    class DummyH:
        def __init__(self, *_, **__):
            self.called = []

        def generate_keys(self, size):
            self.called.append(("gen", size))

        def encrypt(self, *_):
            self.called.append(("enc",))

        def decrypt(self, *_):
            self.called.append(("dec",))

    monkeypatch.setattr("main.HybridCryptoSystem", DummyH)

    monkeypatch.setattr("sys.argv", argv)
    main_module.main()
