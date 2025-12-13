from pathlib import Path
from omegaconf import OmegaConf


CONFIG_DIR = Path(__file__).parent / "configs"


def load_config(env: str | None = None):
    """
    Load layered configuration: base + (dev|prod).
    If env is not provided, use app.env from base.yaml.
    """
    base_cfg = OmegaConf.load(CONFIG_DIR / "base.yaml")

    if env is None:
        env = base_cfg.app.env

    env_path = CONFIG_DIR / f"{env}.yaml"
    if env_path.exists():
        env_cfg = OmegaConf.load(env_path)
        cfg = OmegaConf.merge(base_cfg, env_cfg)
    else:
        cfg = base_cfg

    return cfg
