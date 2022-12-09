from pathlib import Path
from typing import TextIO


def load_asset(module, name) -> TextIO:
    asset: Path = Path(module).parent / "data" / name
    return asset.open()
