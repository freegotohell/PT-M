import argparse

from crypto_system import HybridCryptoSystem
from work_file import *


def main():
    paths = read_json("settings.json")
    main_parser = argparse.ArgumentParser()
    group = main_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", help="key generation mode", nargs='?', const=None, type=int,
                       choices=[128, 192, 256])
    group.add_argument("-enc", "--encryption", help="encryption mode", action="store_true")
    group.add_argument("-dec", "--decryption", help="decryption mode", action="store_true")

    args = main_parser.parse_args()
    match (args.generation, args.encryption, args.decryption):
        case (True, False, False):
            key_size = args.generation
            h = HybridCryptoSystem(paths["symmetric_key"], paths["secret_key"], paths["public_key"])
            h.generate_keys(key_size)
        case (False, True, False):
            h = HybridCryptoSystem(paths["symmetric_key"], paths["secret_key"], paths["public_key"])
            h.encrypt(paths["initial_file"], paths["encrypted_file"])
        case (False, False, True):
            h = HybridCryptoSystem(paths["symmetric_key"], paths["secret_key"], paths["public_key"])
            h.decrypt(paths["encrypted_file"], paths["decrypted_file"])


if __name__ == '__main__':
    main()
