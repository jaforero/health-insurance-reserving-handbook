"""In-memory exports for the local triangle workshop."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone

import pandas as pd

from .benktander import BenktanderResult
from .bornhuetter_ferguson import BornhuetterFergusonResult
from .chain_ladder import ChainLadderConfig, ChainLadderResult
from .config import TriangleConfig
from .data_scope import assess_triangle_input
from .triangles import TriangleResult
from .validation import PreparedClaims


def _csv_bytes(frame: pd.DataFrame, *, include_index: bool = False) -> bytes:
    return frame.to_csv(index=include_index, encoding="utf-8", lineterminator="\n").encode("utf-8")


def _precise_chain_ladder_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Expose precise r2 terminology while preserving internal compatibility."""

    columns = [
        "ultima_edad_observada",
        "acumulado_observado",
        "madurez",
        "costo_proyectado_horizonte_seleccionado",
        "pasivo_no_pagado_estimado",
        "participacion_pasivo_no_pagado",
    ]
    available = [column for column in columns if column in frame]
    output = frame.loc[:, available].copy()
    output.insert(
        3,
        "cdf_total_seleccionado",
        frame["cdf_a_ultimate"],
    )
    return output


def _precise_bf_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rename = {
        "cdf_a_ultimate": "cdf_total_seleccionado",
        "porcentaje_no_desarrollado": "proporcion_no_desarrollada",
        "diferencia_ultimate_bf_vs_cl": "diferencia_costo_proyectado_bf_vs_cl",
        "diferencia_ibnr_bf_vs_cl": "diferencia_pasivo_no_pagado_bf_vs_cl",
    }
    legacy = {
        "ultimate_esperado_prior", "ultimate_bf", "ibnr_bf", "ultimate_chain_ladder",
        "ibnr_chain_ladder", "participacion_ibnr_bf",
    }
    return frame.drop(columns=[column for column in legacy if column in frame]).rename(columns=rename)


def _precise_benktander_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rename = {
        "cdf_a_ultimate": "cdf_total_seleccionado",
        "porcentaje_no_desarrollado": "proporcion_no_desarrollada",
        "diferencia_ibnr_bk_vs_cl": "diferencia_pasivo_no_pagado_bk_vs_cl",
        "diferencia_ibnr_bk_vs_bf": "diferencia_pasivo_no_pagado_bk_vs_bf",
    }
    legacy = {
        "ultimate_esperado_prior", "ultimate_chain_ladder", "ibnr_chain_ladder",
        "ultimate_bf", "ibnr_bf", "ultimate_benktander_iterativo",
        "ultimate_benktander_cerrado", "ultimate_benktander", "ibnr_benktander",
    }
    return frame.drop(columns=[column for column in legacy if column in frame]).rename(columns=rename)


def _precise_totals(frame: pd.DataFrame) -> pd.DataFrame:
    """Prefer r2 indicators and suppress duplicate legacy totals from exports."""

    precise = frame.loc[
        ~frame["indicador"].astype(str).str.contains(r"(?:^|_)ibnr(?:$|_)|ultimate", regex=True)
    ].copy()
    if precise.empty:
        precise = frame.copy()
    return precise


def _precise_diagnostics(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame.copy()
    if "codigo" in output:
        output["codigo"] = output["codigo"].astype(str).str.replace("IBNR", "PASIVO_NO_PAGADO")
    if "mensaje" in output:
        output["mensaje"] = output["mensaje"].astype(str).str.replace(
            "IBNR", "pasivo no pagado", regex=False
        )
    return output


def build_results_zip(
    prepared: PreparedClaims,
    result: TriangleResult,
    config: TriangleConfig,
    *,
    include_detail: bool = False,
) -> bytes:
    """Build a downloadable ZIP without persisting user data on disk."""

    aggregated_bytes = _csv_bytes(result.aggregated_long)
    digest = hashlib.sha256(aggregated_bytes).hexdigest()
    manifest = {
        "demo": "Demo 5 — De datos propios a triángulos actuariales",
        "version_motor": "0.1.1",
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "hash_datos_agregados_sha256": digest,
        "incluye_detalle_canonico": include_detail,
        "reconciliado": result.reconciled,
        "configuracion": config.to_dict(),
    }
    readme = """DEMO 5 — RESULTADOS LOCALES

Este paquete fue generado en el computador del usuario.
No contiene el archivo fuente original.

Archivos:
- 01_validaciones.csv: controles previos y advertencias.
- 02_datos_largos_agregados.csv: celdas observadas en formato largo.
- 03_triangulo_incremental.csv: importes por edad de desarrollo.
- 04_triangulo_acumulado.csv: importes acumulados por edad.
- 05_mascara_observada.csv: 1 observado; 0 futuro no observado.
- 06_diagnostico.csv: suficiencia y reconciliación.
- 07_gates.csv: gates relevantes de preparación.
- 08_configuracion.json: decisiones y mapeo de la ejecución.
- 09_manifiesto.json: versión, hash y trazabilidad.

El triángulo es una estructura descriptiva. Su construcción no aprueba por sí
misma el uso de Chain Ladder ni constituye una estimación actuarial profesional.
"""

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("LEEME.txt", readme)
        archive.writestr("01_validaciones.csv", _csv_bytes(prepared.issues_frame()))
        archive.writestr("02_datos_largos_agregados.csv", aggregated_bytes)
        archive.writestr(
            "03_triangulo_incremental.csv",
            _csv_bytes(result.incremental, include_index=True),
        )
        archive.writestr(
            "04_triangulo_acumulado.csv",
            _csv_bytes(result.cumulative, include_index=True),
        )
        archive.writestr(
            "05_mascara_observada.csv",
            _csv_bytes(result.observed_mask.astype(int), include_index=True),
        )
        archive.writestr("06_diagnostico.csv", _csv_bytes(result.diagnostics))
        archive.writestr("07_gates.csv", _csv_bytes(result.gates))
        archive.writestr(
            "08_configuracion.json",
            json.dumps(config.to_dict(), ensure_ascii=False, indent=2).encode("utf-8"),
        )
        archive.writestr(
            "09_manifiesto.json",
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"),
        )
        if include_detail:
            archive.writestr("10_datos_canonicos_detalle.csv", _csv_bytes(result.canonical_detail))
    return buffer.getvalue()


def build_chain_ladder_zip(
    result: ChainLadderResult,
    config: ChainLadderConfig,
    *,
    source_metadata: dict[str, object] | None = None,
) -> bytes:
    """Build a non-record-level Chain Ladder result package in memory."""

    observed_bytes = _csv_bytes(result.observed_cumulative, include_index=True)
    manifest = {
        "demo": "Demo 6 — Chain Ladder con datos propios",
        "version_motor": "0.6.0-sprint2-r2",
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "hash_triangulo_observado_sha256": hashlib.sha256(observed_bytes).hexdigest(),
        "configuracion": config.to_dict(),
        "fuente_agregada": source_metadata or {},
        "nombre_resultado_principal": "pasivo_no_pagado_estimado_basado_en_datos_pagados",
        "no_identifica": ["IBNR puro", "RBNS", "IBNER"],
        "costo_final_requiere_cola_explicita": True,
    }
    readme = """DEMO 6 — RESULTADOS CHAIN LADDER

Este paquete fue generado localmente a partir de un triángulo acumulado.
No contiene el archivo fuente original ni movimientos fila a fila.

Archivos:
- 01_triangulo_acumulado_observado.csv: valores utilizados para estimar factores.
- 02_mascara_observada.csv: 1 observado; 0 futuro no observado.
- 03_factores_individuales.csv: ratios por origen y enlace.
- 04_seleccion_factores.csv: candidatos, selección, suficiencia y alertas.
- 05_cdf_total_seleccionado.csv: factores acumulados, incluida la cola seleccionada.
- 06_triangulo_acumulado_proyectado.csv: celdas futuras completadas.
- 07_triangulo_incremental_proyectado.csv: incrementos observados y proyectados.
- 08_resultados_por_origen.csv: costo proyectado al horizonte y pasivo no pagado estimado.
- 09_totales.csv: resumen agregado.
- 10_diagnosticos.csv: alertas automáticas que requieren interpretación.
- 11_configuracion.json: selección, cola y parámetros.
- 12_manifiesto.json: versión, hash, trazabilidad y límites de interpretación.
- 13_informacion_recibida.csv: inventario de la base cargada.
- 14_informacion_faltante_deseable.csv: datos adicionales y su impacto.
- 15_alcance_calculable.csv: resultados posibles, condicionales y no identificables.

Chain Ladder es una estimación determinística y no cuantifica por sí solo la
incertidumbre. Los factores, la cola y la representatividad histórica requieren
juicio actuarial documentado y validación independiente.

Un triángulo agregado exclusivamente pagado estima el pasivo no pagado total.
No separa IBNR puro, RBNS e IBNER. Si no existe una cola explícita y sustentada,
el resultado termina en la edad visible y no debe denominarse costo final.
"""

    cdf_frame = result.cdf_to_ultimate.rename("cdf_total_seleccionado").rename_axis("edad_desarrollo").reset_index()
    assessment = assess_triangle_input(
        result.observed_cumulative,
        result.observed_mask,
        triangle_config=config.to_dict(),
        manifest=source_metadata or {},
        source_type=str((source_metadata or {}).get("tipo", "triangulo_agregado")),
    )
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("LEEME.txt", readme)
        archive.writestr("01_triangulo_acumulado_observado.csv", observed_bytes)
        archive.writestr(
            "02_mascara_observada.csv",
            _csv_bytes(result.observed_mask.astype(int), include_index=True),
        )
        archive.writestr(
            "03_factores_individuales.csv",
            _csv_bytes(result.individual_factors, include_index=True),
        )
        archive.writestr("04_seleccion_factores.csv", _csv_bytes(result.factor_summary))
        archive.writestr("05_cdf_total_seleccionado.csv", _csv_bytes(cdf_frame))
        archive.writestr(
            "06_triangulo_acumulado_proyectado.csv",
            _csv_bytes(result.projected_cumulative, include_index=True),
        )
        archive.writestr(
            "07_triangulo_incremental_proyectado.csv",
            _csv_bytes(result.projected_incremental, include_index=True),
        )
        archive.writestr(
            "08_resultados_por_origen.csv",
            _csv_bytes(_precise_chain_ladder_summary(result.origin_summary), include_index=True),
        )
        archive.writestr("09_totales.csv", _csv_bytes(_precise_totals(result.totals)))
        archive.writestr("10_diagnosticos.csv", _csv_bytes(_precise_diagnostics(result.diagnostics)))
        archive.writestr(
            "11_configuracion.json",
            json.dumps(config.to_dict(), ensure_ascii=False, indent=2).encode("utf-8"),
        )
        archive.writestr(
            "12_manifiesto.json",
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"),
        )
        archive.writestr("13_informacion_recibida.csv", _csv_bytes(assessment.received))
        archive.writestr(
            "14_informacion_faltante_deseable.csv",
            _csv_bytes(assessment.missing_desirable),
        )
        archive.writestr("15_alcance_calculable.csv", _csv_bytes(assessment.calculation_scope))
    return buffer.getvalue()


def build_classical_methods_zip(
    chain_ladder: ChainLadderResult,
    chain_ladder_config: ChainLadderConfig,
    bornhuetter_ferguson: BornhuetterFergusonResult,
    *,
    benktander: BenktanderResult | None = None,
    source_metadata: dict[str, object] | None = None,
    prior_metadata: dict[str, object] | None = None,
) -> bytes:
    """Build a joint aggregate CL/BF package, optionally including Benktander."""

    if benktander is not None and not isinstance(benktander, BenktanderResult):
        raise TypeError("Se requiere un resultado válido de Benktander")

    observed_bytes = _csv_bytes(chain_ladder.observed_cumulative, include_index=True)
    prior_bytes = _csv_bytes(bornhuetter_ferguson.prior_input, include_index=True)
    includes_benktander = benktander is not None
    manifest = {
        "demo": (
            "Demo 6 — Comparación Chain Ladder, Bornhuetter-Ferguson y Benktander"
            if includes_benktander
            else "Demo 6 — Comparación Chain Ladder y Bornhuetter-Ferguson"
        ),
        "version_motor": "0.6.0-sprint2-r2",
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "hash_triangulo_observado_sha256": hashlib.sha256(observed_bytes).hexdigest(),
        "hash_prior_normalizado_sha256": hashlib.sha256(prior_bytes).hexdigest(),
        "configuracion_chain_ladder": chain_ladder_config.to_dict(),
        "configuracion_bornhuetter_ferguson": bornhuetter_ferguson.config.to_dict(),
        "fuente_agregada": source_metadata or {},
        "fuente_prior": prior_metadata or {},
        "incluye_archivos_fuente_originales": False,
        "nombre_resultado_principal": "pasivo_no_pagado_estimado_basado_en_datos_pagados",
        "no_identifica": ["IBNR puro", "RBNS", "IBNER"],
        "costo_final_requiere_cola_explicita": True,
    }
    if benktander is not None:
        manifest["configuracion_benktander"] = benktander.config.to_dict()
    readme = """DEMO 6 — COMPARACIÓN CHAIN LADDER Y BORNHUETTER-FERGUSON

Este paquete fue generado localmente con información agregada por periodo de origen.
No contiene los archivos fuente originales ni movimientos fila a fila.

Archivos:
- 01_triangulo_acumulado_observado.csv: valores utilizados por Chain Ladder.
- 02_mascara_observada.csv: 1 observado; 0 futuro no observado.
- 03_factores_individuales.csv: ratios por origen y enlace.
- 04_seleccion_factores.csv: candidatos, selección, suficiencia y alertas.
- 05_cdf_total_seleccionado.csv: factores acumulados, incluida la cola seleccionada.
- 06_triangulo_acumulado_proyectado.csv: celdas futuras completadas.
- 07_triangulo_incremental_proyectado.csv: incrementos observados y proyectados.
- 08_resultados_chain_ladder_por_origen.csv: costo y pasivo no pagado Chain Ladder.
- 09_totales_chain_ladder.csv: resumen Chain Ladder.
- 10_diagnosticos_chain_ladder.csv: alertas del patrón de desarrollo.
- 11_prior_bf_normalizado.csv: prior agregado utilizado por BF.
- 12_resultados_bf_por_origen.csv: madurez, prior, costo y pasivo no pagado BF.
- 13_totales_bf.csv: resumen BF y diferencias contra Chain Ladder.
- 14_sensibilidad_prior_bf.csv: shocks configurados de la expectativa previa.
- 15_diagnosticos_bf.csv: alertas de prior, CDF y pasivo no pagado BF.
- 16_configuracion_chain_ladder.json: selección, cola y parámetros.
- 17_configuracion_bf.json: definición del prior, columnas y shocks.
- 18_manifiesto.json: versión, hashes y trazabilidad de fuentes agregadas.
- 24_informacion_recibida.csv: inventario estructural y metadatos disponibles.
- 25_informacion_faltante_deseable.csv: brechas y su impacto actuarial.
- 26_alcance_calculable.csv: resultados posibles, condicionales y no identificables.

Ambos métodos son determinísticos. La fuente del prior, la exposición, los factores,
la cola y la representatividad histórica requieren juicio actuarial documentado,
reconciliación independiente y gobierno antes de cualquier uso profesional.

El residual de datos exclusivamente pagados es pasivo no pagado total; no separa
IBNR puro, RBNS e IBNER. El costo final exige una cola explícita y sustentada.
"""
    if benktander is not None:
        readme += """

EXTENSIÓN BENKTANDER

- 19_resultados_benktander_por_origen.csv: pesos, costo y pasivo no pagado Benktander.
- 20_totales_benktander.csv: resumen y diferencias frente a CL y BF.
- 21_sensibilidad_iteraciones_benktander.csv: convergencia desde el prior hacia Chain Ladder.
- 22_diagnosticos_benktander.csv: conciliación, pesos, signos y estabilidad numérica.
- 23_configuracion_benktander.json: iteraciones, escenarios, moneda y medida.

La iteración no crea información nueva. La selección debe justificarse y someterse a
sensibilidad, backtesting y revisión independiente.
"""

    cdf_frame = chain_ladder.cdf_to_ultimate.rename("cdf_total_seleccionado").rename_axis("edad_desarrollo").reset_index()
    assessment = assess_triangle_input(
        chain_ladder.observed_cumulative,
        chain_ladder.observed_mask,
        triangle_config=chain_ladder_config.to_dict(),
        manifest=source_metadata or {},
        source_type=str((source_metadata or {}).get("tipo", "triangulo_agregado")),
    )
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("LEEME.txt", readme)
        archive.writestr("01_triangulo_acumulado_observado.csv", observed_bytes)
        archive.writestr(
            "02_mascara_observada.csv",
            _csv_bytes(chain_ladder.observed_mask.astype(int), include_index=True),
        )
        archive.writestr(
            "03_factores_individuales.csv",
            _csv_bytes(chain_ladder.individual_factors, include_index=True),
        )
        archive.writestr("04_seleccion_factores.csv", _csv_bytes(chain_ladder.factor_summary))
        archive.writestr("05_cdf_total_seleccionado.csv", _csv_bytes(cdf_frame))
        archive.writestr(
            "06_triangulo_acumulado_proyectado.csv",
            _csv_bytes(chain_ladder.projected_cumulative, include_index=True),
        )
        archive.writestr(
            "07_triangulo_incremental_proyectado.csv",
            _csv_bytes(chain_ladder.projected_incremental, include_index=True),
        )
        archive.writestr(
            "08_resultados_chain_ladder_por_origen.csv",
            _csv_bytes(_precise_chain_ladder_summary(chain_ladder.origin_summary), include_index=True),
        )
        archive.writestr("09_totales_chain_ladder.csv", _csv_bytes(_precise_totals(chain_ladder.totals)))
        archive.writestr("10_diagnosticos_chain_ladder.csv", _csv_bytes(_precise_diagnostics(chain_ladder.diagnostics)))
        archive.writestr("11_prior_bf_normalizado.csv", prior_bytes)
        archive.writestr(
            "12_resultados_bf_por_origen.csv",
            _csv_bytes(_precise_bf_summary(bornhuetter_ferguson.origin_summary), include_index=True),
        )
        archive.writestr("13_totales_bf.csv", _csv_bytes(_precise_totals(bornhuetter_ferguson.totals)))
        archive.writestr(
            "14_sensibilidad_prior_bf.csv",
            _csv_bytes(
                bornhuetter_ferguson.sensitivity.rename(
                    columns={
                        "ultimate_esperado_prior_total": "costo_final_esperado_prior_total",
                        "ultimate_bf_total": "costo_proyectado_horizonte_seleccionado_bf_total",
                        "ibnr_bf_total": "pasivo_no_pagado_estimado_bf_total",
                        "diferencia_ibnr_vs_base": "diferencia_pasivo_no_pagado_vs_base",
                        "diferencia_ultimate_vs_base": "diferencia_costo_proyectado_vs_base",
                    }
                )
            ),
        )
        archive.writestr(
            "15_diagnosticos_bf.csv",
            _csv_bytes(_precise_diagnostics(bornhuetter_ferguson.diagnostics)),
        )
        archive.writestr(
            "16_configuracion_chain_ladder.json",
            json.dumps(chain_ladder_config.to_dict(), ensure_ascii=False, indent=2).encode("utf-8"),
        )
        archive.writestr(
            "17_configuracion_bf.json",
            json.dumps(
                bornhuetter_ferguson.config.to_dict(),
                ensure_ascii=False,
                indent=2,
            ).encode("utf-8"),
        )
        archive.writestr(
            "18_manifiesto.json",
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"),
        )
        if benktander is not None:
            archive.writestr(
                "19_resultados_benktander_por_origen.csv",
                _csv_bytes(_precise_benktander_summary(benktander.origin_summary), include_index=True),
            )
            archive.writestr(
                "20_totales_benktander.csv",
                _csv_bytes(_precise_totals(benktander.totals)),
            )
            archive.writestr(
                "21_sensibilidad_iteraciones_benktander.csv",
                _csv_bytes(
                    benktander.sensitivity.rename(
                        columns={
                            "ultimate_total": "costo_proyectado_horizonte_seleccionado_total",
                            "ibnr_total": "pasivo_no_pagado_estimado_total",
                            "diferencia_ibnr_vs_cl": "diferencia_pasivo_no_pagado_vs_cl",
                            "diferencia_ibnr_vs_bf": "diferencia_pasivo_no_pagado_vs_bf",
                        }
                    )
                ),
            )
            archive.writestr(
                "22_diagnosticos_benktander.csv",
                _csv_bytes(_precise_diagnostics(benktander.diagnostics)),
            )
            archive.writestr(
                "23_configuracion_benktander.json",
                json.dumps(
                    benktander.config.to_dict(),
                    ensure_ascii=False,
                    indent=2,
                ).encode("utf-8"),
            )
        archive.writestr("24_informacion_recibida.csv", _csv_bytes(assessment.received))
        archive.writestr(
            "25_informacion_faltante_deseable.csv",
            _csv_bytes(assessment.missing_desirable),
        )
        archive.writestr("26_alcance_calculable.csv", _csv_bytes(assessment.calculation_scope))
    return buffer.getvalue()
