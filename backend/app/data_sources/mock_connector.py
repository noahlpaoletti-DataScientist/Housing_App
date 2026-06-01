from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_properties() -> list[dict]:
    with (DATA_DIR / "sample_properties.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def load_comparables() -> list[dict]:
    with (DATA_DIR / "sample_comps.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def load_market_trends() -> list[dict]:
    with (DATA_DIR / "sample_market_trends.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def load_material_costs() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sample_material_costs.csv")
