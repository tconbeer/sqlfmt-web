from pathlib import Path


def load_asset(filename: str) -> str:
    """
    Read the asset file as a string and return it
    """
    asset_path = Path(__file__).parent / filename
    with open(asset_path) as f:
        return f.read()
