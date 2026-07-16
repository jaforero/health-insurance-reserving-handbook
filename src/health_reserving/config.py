"""Configuration objects shared by the triangle workflow."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal


Frequency = Literal["M", "Q", "Y"]


@dataclass(frozen=True)
class TriangleConfig:
    """User-confirmed mapping and actuarial scope for one triangle run."""

    origin_column: str
    movement_column: str
    amount_column: str
    valuation_date: str
    frequency: Frequency = "M"
    maximum_development: int | None = None
    id_column: str | None = None
    movement_type_column: str | None = None
    segment_column: str | None = None
    segment_value: str | None = None
    dayfirst: bool = True
    date_format: str | None = None
    allow_negative_amounts: bool = False
    obligation_defined: bool = False
    origin_semantics_confirmed: bool = False
    movement_semantics_confirmed: bool = False
    amount_semantics_confirmed: bool = False
    complete_through_valuation: bool = False
    representative_history: bool = False
    currency: str = "COP"
    measure: str = "PAGADO_INCREMENTAL"
    minimum_origin_periods: int = 36
    minimum_development_periods: int = 12

    def __post_init__(self) -> None:
        required = {
            "origin_column": self.origin_column,
            "movement_column": self.movement_column,
            "amount_column": self.amount_column,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError("Faltan campos requeridos: " + ", ".join(missing))
        if self.frequency not in {"M", "Q", "Y"}:
            raise ValueError("La frecuencia debe ser M, Q o Y")
        if self.maximum_development is not None and self.maximum_development < 0:
            raise ValueError("La edad máxima de desarrollo no puede ser negativa")

        mapped = [
            value
            for value in (
                self.origin_column,
                self.movement_column,
                self.amount_column,
                self.id_column,
                self.movement_type_column,
                self.segment_column,
            )
            if value
        ]
        if len(mapped) != len(set(mapped)):
            raise ValueError("Una columna fuente no puede mapearse a dos campos canónicos")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


FREQUENCY_LABELS: dict[Frequency, str] = {
    "M": "Mensual",
    "Q": "Trimestral",
    "Y": "Anual",
}
