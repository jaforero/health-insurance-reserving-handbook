"""Canonical mapping and conservative data-readiness validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from .config import TriangleConfig


BLOCKING = "BLOQUEANTE"
WARNING = "ADVERTENCIA"
INFO = "INFORMATIVO"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: str
    count: int
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "codigo": self.code,
            "severidad": self.severity,
            "registros": self.count,
            "mensaje": self.message,
        }


@dataclass
class PreparedClaims:
    data: pd.DataFrame
    issues: tuple[ValidationIssue, ...]
    summary: dict[str, Any]

    @property
    def blocking_issues(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == BLOCKING)

    @property
    def has_blocking_issues(self) -> bool:
        return bool(self.blocking_issues)

    def issues_frame(self) -> pd.DataFrame:
        columns = ["codigo", "severidad", "registros", "mensaje"]
        return pd.DataFrame([issue.to_dict() for issue in self.issues], columns=columns)


def parse_date_series(
    values: pd.Series,
    *,
    dayfirst: bool = True,
    date_format: str | None = None,
) -> pd.Series:
    """Parse ISO dates deterministically while supporting day-first local dates."""

    if pd.api.types.is_datetime64_any_dtype(values):
        return pd.to_datetime(values, errors="coerce")
    if date_format:
        return pd.to_datetime(values, errors="coerce", dayfirst=dayfirst, format=date_format)

    text = values.astype("string").str.strip()
    iso_mask = text.str.match(r"^\d{4}-\d{1,2}(?:-\d{1,2})?(?:[ T].*)?$", na=False)
    parsed = pd.Series(pd.NaT, index=values.index, dtype="datetime64[ns]")
    if iso_mask.any():
        parsed.loc[iso_mask] = pd.to_datetime(
            text.loc[iso_mask], errors="coerce", dayfirst=False, format="mixed"
        )
    if (~iso_mask).any():
        parsed.loc[~iso_mask] = pd.to_datetime(
            text.loc[~iso_mask], errors="coerce", dayfirst=dayfirst, format="mixed"
        )
    return parsed


def _add_issue(
    issues: list[ValidationIssue],
    code: str,
    severity: str,
    count: int,
    message: str,
) -> None:
    if count:
        issues.append(ValidationIssue(code, severity, int(count), message))


def _semantic_issues(config: TriangleConfig) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    confirmations = (
        ("SEM_G0", config.obligation_defined, "Defina la obligación que representa el triángulo."),
        (
            "SEM_ORIGEN",
            config.origin_semantics_confirmed,
            "Confirme que la fecha de origen representa ocurrencia, servicio "
            "u otra base declarada.",
        ),
        (
            "SEM_MOVIMIENTO",
            config.movement_semantics_confirmed,
            "Confirme que la fecha de movimiento representa el eje calendario elegido.",
        ),
        (
            "SEM_IMPORTE",
            config.amount_semantics_confirmed,
            "Confirme que el importe es incremental y corresponde a la medida declarada.",
        ),
        (
            "SEM_CORTE",
            config.complete_through_valuation,
            "Confirme que el archivo está completo hasta la fecha de valoración.",
        ),
    )
    for code, confirmed, message in confirmations:
        if not confirmed:
            issues.append(ValidationIssue(code, BLOCKING, 1, message))
    return issues


def prepare_and_validate_claims(
    source: pd.DataFrame,
    config: TriangleConfig,
) -> PreparedClaims:
    """Map user columns to canonical fields and execute conservative controls."""

    missing = [
        column
        for column in (
            config.origin_column,
            config.movement_column,
            config.amount_column,
            config.id_column,
            config.movement_type_column,
            config.segment_column,
        )
        if column and column not in source.columns
    ]
    if missing:
        raise ValueError("No se encontraron las columnas: " + ", ".join(sorted(missing)))

    selected = {
        config.origin_column: "fecha_origen",
        config.movement_column: "fecha_movimiento",
        config.amount_column: "importe_incremental",
    }
    optional = (
        (config.id_column, "id_movimiento"),
        (config.movement_type_column, "tipo_movimiento"),
        (config.segment_column, "segmento"),
    )
    for original, canonical in optional:
        if original:
            selected[original] = canonical

    data = source[list(selected)].rename(columns=selected).copy()
    data.insert(0, "fila_fuente", np.arange(2, len(data) + 2))

    if config.segment_column and config.segment_value is not None:
        mask = data["segmento"].astype("string") == str(config.segment_value)
        data = data.loc[mask].copy()
        if data.empty:
            issue = ValidationIssue(
                "SEGMENTO_VACIO",
                BLOCKING,
                1,
                "El segmento seleccionado no contiene registros.",
            )
            summary = {"filas_fuente": len(source), "filas_segmento": 0}
            return PreparedClaims(data, (issue,), summary)

    raw_origin = data["fecha_origen"].copy()
    raw_movement = data["fecha_movimiento"].copy()
    raw_amount = data["importe_incremental"].copy()

    data["fecha_origen"] = parse_date_series(
        data["fecha_origen"], dayfirst=config.dayfirst, date_format=config.date_format
    )
    data["fecha_movimiento"] = parse_date_series(
        data["fecha_movimiento"], dayfirst=config.dayfirst, date_format=config.date_format
    )
    data["importe_incremental"] = pd.to_numeric(
        data["importe_incremental"], errors="coerce"
    )

    if "id_movimiento" in data:
        data["id_movimiento"] = data["id_movimiento"].astype("string").str.strip()
    if "tipo_movimiento" in data:
        data["tipo_movimiento"] = (
            data["tipo_movimiento"].astype("string").str.strip().str.upper()
        )
    if "segmento" in data:
        data["segmento"] = data["segmento"].astype("string").str.strip()

    issues = _semantic_issues(config)
    origin_invalid = data["fecha_origen"].isna() & raw_origin.notna()
    movement_invalid = data["fecha_movimiento"].isna() & raw_movement.notna()
    amount_invalid = data["importe_incremental"].isna() & raw_amount.notna()

    _add_issue(issues, "FECHA_ORIGEN_NULA", BLOCKING, data["fecha_origen"].isna().sum(),
               "Existen fechas de origen nulas o no interpretables.")
    _add_issue(issues, "FECHA_MOVIMIENTO_NULA", BLOCKING,
               data["fecha_movimiento"].isna().sum(),
               "Existen fechas de movimiento nulas o no interpretables.")
    _add_issue(issues, "FECHA_ORIGEN_FORMATO", INFO, origin_invalid.sum(),
               "Revise el formato de las fechas de origen no interpretables.")
    _add_issue(issues, "FECHA_MOVIMIENTO_FORMATO", INFO, movement_invalid.sum(),
               "Revise el formato de las fechas de movimiento no interpretables.")
    _add_issue(issues, "IMPORTE_NULO", BLOCKING, data["importe_incremental"].isna().sum(),
               "Existen importes nulos o no numéricos.")
    _add_issue(issues, "IMPORTE_FORMATO", INFO, amount_invalid.sum(),
               "Revise separadores decimales y de miles en los importes.")

    finite_mask = np.isfinite(data["importe_incremental"].fillna(0.0))
    _add_issue(issues, "IMPORTE_NO_FINITO", BLOCKING, (~finite_mask).sum(),
               "Existen importes infinitos o no finitos.")

    valid_dates = data["fecha_origen"].notna() & data["fecha_movimiento"].notna()
    negative_lag = valid_dates & (data["fecha_movimiento"] < data["fecha_origen"])
    _add_issue(issues, "REZAGO_NEGATIVO", BLOCKING, negative_lag.sum(),
               "La fecha de movimiento es anterior a la fecha de origen.")

    valuation = pd.Timestamp(config.valuation_date)
    after_valuation = data["fecha_movimiento"].notna() & (
        data["fecha_movimiento"] > valuation
    )
    _add_issue(issues, "POSTERIOR_VALORACION", BLOCKING, after_valuation.sum(),
               "Existen movimientos posteriores a la fecha de valoración.")

    origin_after_valuation = data["fecha_origen"].notna() & (data["fecha_origen"] > valuation)
    _add_issue(issues, "ORIGEN_POSTERIOR_VALORACION", BLOCKING,
               origin_after_valuation.sum(),
               "Existen fechas de origen posteriores a la fecha de valoración.")

    negatives = data["importe_incremental"].lt(0).fillna(False)
    if negatives.any():
        severity = WARNING if config.allow_negative_amounts else BLOCKING
        message = (
            "Los importes negativos fueron aceptados como ajustes o reversos declarados."
            if config.allow_negative_amounts
            else "Existen importes negativos; clasifíquelos y confirme su inclusión."
        )
        _add_issue(issues, "IMPORTES_NEGATIVOS", severity, negatives.sum(), message)

    duplicate_columns = [
        column
        for column in (
            "id_movimiento",
            "fecha_origen",
            "fecha_movimiento",
            "importe_incremental",
            "tipo_movimiento",
            "segmento",
        )
        if column in data.columns
    ]
    exact_duplicates = data.duplicated(subset=duplicate_columns, keep=False)
    _add_issue(issues, "DUPLICADO_EXACTO", BLOCKING, exact_duplicates.sum(),
               "Existen registros duplicados según los campos mapeados.")

    if "id_movimiento" in data:
        blank_ids = data["id_movimiento"].isna() | data["id_movimiento"].eq("")
        _add_issue(issues, "ID_MOVIMIENTO_NULO", WARNING, blank_ids.sum(),
                   "Hay identificadores de movimiento vacíos.")
        duplicated_ids = data["id_movimiento"].notna() & data["id_movimiento"].duplicated(
            keep=False
        )
        _add_issue(issues, "ID_MOVIMIENTO_DUPLICADO", BLOCKING, duplicated_ids.sum(),
                   "El identificador de movimiento no es único.")
    else:
        issues.append(
            ValidationIssue(
                "ID_MOVIMIENTO_AUSENTE",
                WARNING,
                1,
                "No se mapeó un identificador único; la integridad solo puede "
                "evaluarse parcialmente.",
            )
        )

    summary: dict[str, Any] = {
        "filas_fuente": int(len(source)),
        "filas_segmento": int(len(data)),
        "importe_total_parseado": float(data["importe_incremental"].sum(skipna=True)),
        "fecha_origen_minima": data["fecha_origen"].min(),
        "fecha_origen_maxima": data["fecha_origen"].max(),
        "fecha_movimiento_minima": data["fecha_movimiento"].min(),
        "fecha_movimiento_maxima": data["fecha_movimiento"].max(),
        "importes_negativos": int(negatives.sum()),
        "duplicados_exactos": int(exact_duplicates.sum()),
    }
    return PreparedClaims(data.reset_index(drop=True), tuple(issues), summary)
