"""Describe what an aggregate triangle supports before an actuarial projection.

The assessment is intentionally descriptive.  It does not turn an aggregate
paid triangle into claim-level reporting data and it never labels the residual
paid liability as pure IBNR.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd


@dataclass(frozen=True)
class InputScopeAssessment:
    """Three audit tables rendered after a sample or user package is loaded."""

    received: pd.DataFrame
    missing_desirable: pd.DataFrame
    calculation_scope: pd.DataFrame


def _first(mapping: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return value
    return None


def assess_triangle_input(
    cumulative: pd.DataFrame,
    observed_mask: pd.DataFrame,
    *,
    triangle_config: Mapping[str, Any] | None = None,
    manifest: Mapping[str, Any] | None = None,
    source_type: str = "archivo_cargado",
) -> InputScopeAssessment:
    """Summarize received information, gaps and defensible calculations.

    Parameters are aggregate by design.  The function therefore distinguishes
    an estimate of total unpaid claim liability from the narrower pure-IBNR
    component, which cannot be isolated without report-status information.
    """

    if cumulative.empty:
        raise ValueError("El triángulo acumulado está vacío")
    if cumulative.shape != observed_mask.shape:
        raise ValueError("El triángulo y la máscara observada deben tener la misma dimensión")

    config = dict(triangle_config or {})
    trace = dict(manifest or {})
    measure = str(_first(config, "measure", "value_column", "medida") or "no declarada")
    currency = str(_first(config, "currency", "moneda") or "no declarada")
    valuation = str(
        _first(config, "valuation_date", "valuation_month", "fecha_valuacion")
        or _first(trace, "fecha_valuacion", "valuation_date")
        or "no declarada"
    )
    segment = str(_first(config, "segment", "segmento") or "agregado/no declarado")
    observed_cells = int(observed_mask.astype(bool).sum().sum())
    rows, columns = cumulative.shape
    first_origin = str(cumulative.index[0])
    last_origin = str(cumulative.index[-1])
    first_development = str(cumulative.columns[0])
    last_development = str(cumulative.columns[-1])

    received_rows = [
        {
            "elemento": "Fuente",
            "estado": "RECIBIDO",
            "detalle": source_type,
            "implicacion": "Identifica si la base es sintética o proviene de un paquete del usuario.",
        },
        {
            "elemento": "Triángulo acumulado agregado",
            "estado": "RECIBIDO",
            "detalle": f"{rows} periodos de origen × {columns} edades de desarrollo",
            "implicacion": "Permite estimar factores edad-a-edad si la historia es representativa.",
        },
        {
            "elemento": "Celdas observadas",
            "estado": "RECIBIDO",
            "detalle": f"{observed_cells:,} celdas; origen {first_origin} a {last_origin}",
            "implicacion": "La suficiencia debe revisarse por enlace, no solo por dimensión total.",
        },
        {
            "elemento": "Rango de desarrollo",
            "estado": "RECIBIDO",
            "detalle": f"{first_development} a {last_development}",
            "implicacion": "La última edad visible no equivale automáticamente al costo final.",
        },
        {
            "elemento": "Medida declarada",
            "estado": "RECIBIDO" if measure != "no declarada" else "NO DECLARADO",
            "detalle": measure,
            "implicacion": "Debe distinguir pagado, incurrido u otra medida antes de interpretar el residual.",
        },
        {
            "elemento": "Moneda, valuación y segmento",
            "estado": "PARCIAL" if "no declarada" in (currency, valuation) else "RECIBIDO",
            "detalle": f"moneda={currency}; valuación={valuation}; segmento={segment}",
            "implicacion": "Son necesarios para reconciliar, comparar y documentar la estimación.",
        },
        {
            "elemento": "Trazabilidad del paquete",
            "estado": "RECIBIDO" if trace else "NO DECLARADO",
            "detalle": (
                "manifiesto disponible; reconciliado=" + str(trace.get("reconciliado", "no declarado"))
                if trace
                else "sin manifiesto o hash informado"
            ),
            "implicacion": "Apoya reproducibilidad; no valida por sí sola la aptitud actuarial.",
        },
    ]

    missing_rows = [
        {
            "elemento": "Fecha de reporte o aviso por reclamación",
            "prioridad": "NECESARIA PARA IBNR PURO",
            "por_que": "Sin ella no se separan reclamaciones ocurridas no reportadas de las ya reportadas.",
        },
        {
            "elemento": "Reserva caso / incurrido reportado",
            "prioridad": "NECESARIA PARA RBNS/IBNER",
            "por_que": "Permite distinguir saldo de casos reportados y desarrollo sobre reservas caso.",
        },
        {
            "elemento": "Estado de la reclamación y fechas de cierre/reapertura",
            "prioridad": "DESEABLE",
            "por_que": "Mejora el entendimiento de cierres, reaperturas y cambios operativos.",
        },
        {
            "elemento": "Exposición y base de prima o costo esperado",
            "prioridad": "DESEABLE PARA BF/BENKTANDER",
            "por_que": "Permite construir y validar un prior independiente del propio triángulo.",
        },
        {
            "elemento": "Segmentación homogénea",
            "prioridad": "DESEABLE",
            "por_que": "Cobertura, prestador, contrato, región y población pueden tener desarrollos distintos.",
        },
        {
            "elemento": "Bruto/neto, recuperaciones y reclamaciones grandes",
            "prioridad": "DESEABLE",
            "por_que": "Evita mezclar recuperaciones, cambios de signo y severidades no homogéneas.",
        },
        {
            "elemento": "Runoff posterior y base explícita del factor de cola",
            "prioridad": "NECESARIA PARA COSTO FINAL",
            "por_que": "Sin cola sustentada el resultado termina en la última edad visible, no en el costo final.",
        },
        {
            "elemento": "Cambios de operación, tarifas, beneficios y adjudicación",
            "prioridad": "DESEABLE",
            "por_que": "Ayuda a evaluar si la experiencia histórica sigue siendo representativa.",
        },
    ]

    scope_rows = [
        {
            "resultado": "Factores edad-a-edad y proyección del triángulo",
            "estado": "POSIBLE CON REVISIÓN",
            "nombre_preciso": "Proyección determinística del acumulado pagado",
            "limitacion": "Depende de homogeneidad, volumen, estabilidad y selección actuarial.",
        },
        {
            "resultado": "Residual entre acumulado proyectado y pagado observado",
            "estado": "POSIBLE CON REVISIÓN",
            "nombre_preciso": "Pasivo no pagado estimado basado en datos pagados",
            "limitacion": "Incluye conjuntamente componentes reportados y no reportados; no es IBNR puro.",
        },
        {
            "resultado": "Costo final",
            "estado": "CONDICIONAL",
            "nombre_preciso": "Costo final técnico estimado con cola explícita",
            "limitacion": "Si la cola es 1 sin sustento, usar acumulado proyectado a edad terminal.",
        },
        {
            "resultado": "IBNR puro, RBNS e IBNER por separado",
            "estado": "NO IDENTIFICABLE",
            "nombre_preciso": "No calculable con un triángulo agregado exclusivamente pagado",
            "limitacion": "Requiere al menos reporte/aviso, reserva caso o incurrido y estado de reclamación.",
        },
        {
            "resultado": "Estimación para estados financieros",
            "estado": "FUERA DEL ALCANCE DEL DEMO",
            "nombre_preciso": "Resultado educativo no contabilizable",
            "limitacion": "Requiere datos reconciliados, gobierno, supuestos aprobados y revisión independiente.",
        },
    ]

    return InputScopeAssessment(
        received=pd.DataFrame(received_rows),
        missing_desirable=pd.DataFrame(missing_rows),
        calculation_scope=pd.DataFrame(scope_rows),
    )
