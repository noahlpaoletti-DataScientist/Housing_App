from app.formulas.renovation_formula import RENOVATION_VALUE_MULTIPLIERS


def calculate_renovation_roi(renovation_type: str, renovation_cost: float) -> dict[str, float]:
    multiplier = RENOVATION_VALUE_MULTIPLIERS.get(renovation_type.lower(), 0.55)
    value_added = round(renovation_cost * multiplier, 2)
    roi_percent = round((value_added / renovation_cost) * 100, 2) if renovation_cost else 0.0
    return {
        "value_multiplier": multiplier,
        "estimated_value_added": value_added,
        "roi_percent": roi_percent,
    }
