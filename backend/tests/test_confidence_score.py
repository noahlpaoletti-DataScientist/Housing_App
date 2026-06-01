from app.formulas.confidence_formula import calculate_confidence_score


def test_confidence_score_formula():
    result = calculate_confidence_score(100, 80, 90, 95)
    assert result["score"] == 91.0
    assert "confidence" in result["explanation"].lower()
