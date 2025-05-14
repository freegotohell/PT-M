from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class AsymmetricCryptography:
    """
    class for asymmetric encryption using RSA
    """
    def __init__(self, private_key_path: str, public_key_path: str) -> None:
        """
        initializes AsymmetricCryptography class object
        :param private_key_path: path for saving private key
        :param public_key_path: path for saving public key
        """
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    @staticmethod
    def generate_key(size: int = 2048) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """
        generates a pair of RSA keys
        :param size: size of keys in bits
        :return: tuple of private and public keys
        """
        try:
            if size < 2048:
                raise ValueError("the key size must be at least 2048 bits")
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=size)
            public_key = private_key.public_key()
            return private_key, public_key
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def encrypt(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        """
        encrypts data using a public RSA key
        :param data: data to encrypt
        :param public_key: public key for encryption
        :return: encrypted data
        """
        try:
            c_data = public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )
            return c_data
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def decrypt(data: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        """
        decrypts data using a private RSA key
        :param data: encrypted data
        :param private_key: private key for decryption
        :return: decrypted data
        """
        try:
            dc_data = private_key.decrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                )
            )
            return dc_data
        except Exception as e:
            print("Error:", e)
            raise
