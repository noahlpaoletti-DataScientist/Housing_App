from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import RenovationComponent, RenovationEstimate
from app.formulas.renovation_formula import estimate_renovation_cost
from app.formulas.roi_formula import calculate_renovation_roi


def create_renovation_estimate(
    db: Session,
    renovation_type: str,
    inputs: dict[str, float],
    property_id: int | None = None,
    persist: bool = False,
) -> dict:
    cost_result = estimate_renovation_cost(renovation_type, inputs)
    roi_result = calculate_renovation_roi(renovation_type, cost_result["total_cost"])

    if persist:
        import json

        estimate_row = RenovationEstimate(
            property_id=property_id,
            renovation_type=renovation_type,
            total_cost=cost_result["total_cost"],
            value_added=roi_result["estimated_value_added"],
            roi_percent=roi_result["roi_percent"],
            assumptions_json=json.dumps(inputs),
        )
        db.add(estimate_row)
        db.flush()

        for component_name, component_cost in cost_result["base_components"].items():
            db.add(
                RenovationComponent(
                    estimate_id=estimate_row.id,
                    component_name=component_name,
                    component_cost=component_cost,
                    explanation=f"{component_name.replace('_', ' ').title()} cost input for {renovation_type}.",
                )
            )
        db.add(
            RenovationComponent(
                estimate_id=estimate_row.id,
                component_name="overhead",
                component_cost=cost_result["overhead"],
                explanation="Contractor overhead applied at 15 percent.",
            )
        )
        db.add(
            RenovationComponent(
                estimate_id=estimate_row.id,
                component_name="contingency",
                component_cost=cost_result["contingency"],
                explanation="Contingency applied at 10 percent.",
            )
        )
        db.commit()

    return {
        "renovation_type": renovation_type,
        "total_cost": cost_result["total_cost"],
        "value_added": roi_result["estimated_value_added"],
        "roi_percent": roi_result["roi_percent"],
        "value_multiplier": roi_result["value_multiplier"],
        "components": {
            **cost_result["base_components"],
            "overhead": cost_result["overhead"],
            "contingency": cost_result["contingency"],
        },
    }
