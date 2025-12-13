import argparse
from crypto_system import HybridCryptoSystem
from config import load_config


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--env",
        choices=["dev", "prod"],
        default=None,
        help="configuration environment (dev|prod)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-gen",
        "--generation",
        help="key generation mode",
        nargs="?",
        const=32,
        default=None,
        type=int,
        choices=[16, 24, 32],
    )  # default = 32, but still can be one of these
    group.add_argument(
        "-enc",
        "--encryption",
        help="encryption mode",
        action="store_true",
    )
    group.add_argument(
        "-dec",
        "--decryption",
        help="decryption mode",
        action="store_true",
    )

    args = parser.parse_args()

    cfg = load_config(args.env)
    paths = cfg.paths
    app_cfg = cfg.app

    args.generation_flag = args.generation is not None
    if args.generation_flag and args.generation is None:
        args.generation = app_cfg.default_key_size

    h = HybridCryptoSystem(
        paths.symmetric_key,
        paths.secret_key,
        paths.public_key,
    )

    if getattr(app_cfg, "debug", False):
        print(f"Environment: {app_cfg.env}")
        print(f"Symmetric key path: {paths.symmetric_key}")
        print(f"Public key path: {paths.public_key}")
        print(f"Secret key path: {paths.secret_key}")

    match (args.generation_flag, args.encryption, args.decryption):
        case (True, False, False):
            h.generate_keys(args.generation)
        case (False, True, False):
            h.encrypt(paths.initial_file, paths.encrypted_file)
        case (False, False, True):
            h.decrypt(paths.encrypted_file, paths.decrypted_file)


if __name__ == "__main__":
    main()
