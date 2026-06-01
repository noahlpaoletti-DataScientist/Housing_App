from app.formulas.renovation_formula import estimate_renovation_cost


def estimate_new_build_cost(inputs: dict[str, float]) -> dict:
    return estimate_renovation_cost("new_build", inputs)
