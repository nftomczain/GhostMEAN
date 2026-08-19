"""mm <-> inch conversion. Internal math always uses mm."""

MM_PER_INCH = 25.4


def to_mm(value: float, unit: str) -> float:
    if unit == "mm":
        return value
    if unit == "in":
        return value * MM_PER_INCH
    raise ValueError(f"unknown unit: {unit}")


def from_mm(value_mm: float, unit: str) -> float:
    if unit == "mm":
        return value_mm
    if unit == "in":
        return value_mm / MM_PER_INCH
    raise ValueError(f"unknown unit: {unit}")
