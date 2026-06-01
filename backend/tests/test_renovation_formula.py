from app.formulas.new_build_formula import estimate_new_build_cost
from app.formulas.renovation_formula import estimate_renovation_cost
from app.formulas.roi_formula import calculate_renovation_roi


def test_kitchen_renovation_formula():
    result = estimate_renovation_cost("kitchen", {"kitchen_square_feet": 180})
    assert result["total_cost"] > 0
    assert "materials" in result["base_components"]


def test_renovation_roi_formula():
    result = calculate_renovation_roi("kitchen", 50000)
    assert result["estimated_value_added"] == 35000
    assert result["roi_percent"] == 70.0


def test_new_build_cost_formula():
    result = estimate_new_build_cost({"building_square_feet": 2500})
    assert result["total_cost"] > 400000
