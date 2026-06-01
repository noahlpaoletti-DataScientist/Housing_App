from __future__ import annotations

from typing import Any

DEFAULT_OVERHEAD_PERCENT = 0.15
DEFAULT_CONTINGENCY_PERCENT = 0.10
DEFAULT_LABOR_RATE = 65.0

RENOVATION_VALUE_MULTIPLIERS = {
    "kitchen": 0.70,
    "bathroom": 0.65,
    "roof": 0.55,
    "paint": 0.50,
    "flooring": 0.60,
    "hvac": 0.50,
    "windows": 0.55,
    "basement": 0.65,
    "full_home": 0.75,
    "addition": 0.72,
    "new_build": 0.85,
}


def _sum_components(components: dict[str, float]) -> dict[str, Any]:
    subtotal = sum(components.values())
    overhead = subtotal * DEFAULT_OVERHEAD_PERCENT
    contingency = (subtotal + overhead) * DEFAULT_CONTINGENCY_PERCENT
    total = subtotal + overhead + contingency
    return {
        "base_components": components,
        "overhead": round(overhead, 2),
        "contingency": round(contingency, 2),
        "total_cost": round(total, 2),
    }


def estimate_renovation_cost(renovation_type: str, inputs: dict[str, float]) -> dict[str, Any]:
    renovation_type = renovation_type.lower()

    if renovation_type == "kitchen":
        components = {
            "materials": inputs.get("kitchen_square_feet", 180) * inputs.get("kitchen_cost_per_sqft", 140),
            "cabinets": inputs.get("cabinet_linear_feet", 24) * inputs.get("cabinet_cost_per_linear_foot", 220),
            "appliances": inputs.get("appliance_allowance", 9_500),
            "plumbing": inputs.get("plumbing_allowance", 2_400),
            "electrical": inputs.get("electrical_allowance", 1_800),
        }
    elif renovation_type == "bathroom":
        components = {
            "materials": inputs.get("bathroom_square_feet", 75) * inputs.get("bathroom_cost_per_sqft", 125),
            "fixtures": inputs.get("fixture_count", 5) * inputs.get("fixture_cost", 550),
            "tile": inputs.get("tile_square_feet", 95) * inputs.get("tile_cost_per_sqft", 18),
            "plumbing": inputs.get("plumbing_allowance", 1_750),
        }
    elif renovation_type == "new_build":
        components = {
            "structure": inputs.get("building_square_feet", 2400)
            * inputs.get("regional_construction_cost_per_sqft", 190),
            "land_prep": inputs.get("land_prep_cost", 18_000),
            "permits": inputs.get("permits", 7_500),
            "utilities": inputs.get("utility_connection_cost", 12_000),
            "design": inputs.get("design_architecture_fees", 22_000),
        }
    else:
        quantity = inputs.get("quantity", 1)
        material_unit_cost = inputs.get("material_unit_cost", 4_500)
        labor_hours = inputs.get("labor_hours", 40)
        permit_cost = inputs.get("permit_cost", 850)
        disposal_cost = inputs.get("disposal_cost", 500)
        components = {
            "materials": quantity * material_unit_cost,
            "labor": labor_hours * inputs.get("hourly_labor_rate", DEFAULT_LABOR_RATE),
            "permits": permit_cost,
            "disposal": disposal_cost,
        }

    result = _sum_components({key: round(value, 2) for key, value in components.items()})
    return result
