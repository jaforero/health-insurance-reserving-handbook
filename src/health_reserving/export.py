"""In-memory exports for the local triangle workshop."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone

import pandas as pd

from .bornhuetter_ferguson import BornhuetterFergusonResult
from .chain_ladder import ChainLadderConfig, ChainLadderResult
from .config import TriangleConfig
from .triangles import TriangleResult
from .validation import PreparedClaims


def _csv_bytes(frame: pd.DataFrame, *, include_index: bool = False) -> bytes:
    return frame.to_csv(index=include_index, encoding="utf-8", lineterminator="\n").encode("utf-8")


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
        "version_motor": "0.2.0",
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "hash_triangulo_observado_sha256": hashlib.sha256(observed_bytes).hexdigest(),
        "configuracion": config.to_dict(),
        "fuente_agregada": source_metadata or {},
    }
    readme = """DEMO 6 — RESULTADOS CHAIN LADDER

Este paquete fue generado localmente a partir de un triángulo acumulado.
No contiene el archivo fuente original ni movimientos fila a fila.

Archivos:
- 01_triangulo_acumulado_observado.csv: valores utilizados para estimar factores.
- 02_mascara_observada.csv: 1 observado; 0 futuro no observado.
- 03_factores_individuales.csv: ratios por origen y enlace.
- 04_seleccion_factores.csv: candidatos, selección, suficiencia y alertas.
- 05_cdf_a_ultimate.csv: factores acumulados desde cada edad.
- 06_triangulo_acumulado_proyectado.csv: celdas futuras completadas.
- 07_triangulo_incremental_proyectado.csv: incrementos observados y proyectados.
- 08_resultados_por_origen.csv: madurez, ultimate e IBNR.
- 09_totales.csv: resumen agregado.
- 10_diagnosticos.csv: alertas automáticas que requieren interpretación.
- 11_configuracion.json: selección, cola y parámetros.
- 12_manifiesto.json: versión, hash y trazabilidad.

Chain Ladder es una estimación determinística y no cuantifica por sí solo la
incertidumbre. Los factores, la cola y la representatividad histórica requieren
juicio actuarial documentado y validación independiente.
"""

    cdf_frame = result.cdf_to_ultimate.rename_axis("edad_desarrollo").reset_index()
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
        archive.writestr("05_cdf_a_ultimate.csv", _csv_bytes(cdf_frame))
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
            _csv_bytes(result.origin_summary, include_index=True),
        )
        archive.writestr("09_totales.csv", _csv_bytes(result.totals))
        archive.writestr("10_diagnosticos.csv", _csv_bytes(result.diagnostics))
        archive.writestr(
            "11_configuracion.json",
            json.dumps(config.to_dict(), ensure_ascii=False, indent=2).encode("utf-8"),
        )
        archive.writestr(
            "12_manifiesto.json",
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"),
        )
    return buffer.getvalue()


def build_classical_methods_zip(
    chain_ladder: ChainLadderResult,
    chain_ladder_config: ChainLadderConfig,
    bornhuetter_ferguson: BornhuetterFergusonResult,
    *,
    source_metadata: dict[str, object] | None = None,
    prior_metadata: dict[str, object] | None = None,
) -> bytes:
    """Build a joint aggregate Chain Ladder and BF package in memory."""

    observed_bytes = _csv_bytes(chain_ladder.observed_cumulative, include_index=True)
    prior_bytes = _csv_bytes(bornhuetter_ferguson.prior_input, include_index=True)
    manifest = {
        "demo": "Demo 6 — Comparación Chain Ladder y Bornhuetter-Ferguson",
        "version_motor": "0.3.0",
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "hash_triangulo_observado_sha256": hashlib.sha256(observed_bytes).hexdigest(),
        "hash_prior_normalizado_sha256": hashlib.sha256(prior_bytes).hexdigest(),
        "configuracion_chain_ladder": chain_ladder_config.to_dict(),
        "configuracion_bornhuetter_ferguson": bornhuetter_ferguson.config.to_dict(),
        "fuente_agregada": source_metadata or {},
        "fuente_prior": prior_metadata or {},
        "incluye_archivos_fuente_originales": False,
    }
    readme = """DEMO 6 — COMPARACIÓN CHAIN LADDER Y BORNHUETTER-FERGUSON

Este paquete fue generado localmente con información agregada por periodo de origen.
No contiene los archivos fuente originales ni movimientos fila a fila.

Archivos:
- 01_triangulo_acumulado_observado.csv: valores utilizados por Chain Ladder.
- 02_mascara_observada.csv: 1 observado; 0 futuro no observado.
- 03_factores_individuales.csv: ratios por origen y enlace.
- 04_seleccion_factores.csv: candidatos, selección, suficiencia y alertas.
- 05_cdf_a_ultimate.csv: factores acumulados desde cada edad.
- 06_triangulo_acumulado_proyectado.csv: celdas futuras completadas.
- 07_triangulo_incremental_proyectado.csv: incrementos observados y proyectados.
- 08_resultados_chain_ladder_por_origen.csv: ultimate e IBNR Chain Ladder.
- 09_totales_chain_ladder.csv: resumen Chain Ladder.
- 10_diagnosticos_chain_ladder.csv: alertas del patrón de desarrollo.
- 11_prior_bf_normalizado.csv: prior agregado utilizado por BF.
- 12_resultados_bf_por_origen.csv: madurez, prior, ultimate e IBNR BF y comparación.
- 13_totales_bf.csv: resumen BF y diferencias contra Chain Ladder.
- 14_sensibilidad_prior_bf.csv: shocks configurados de la expectativa previa.
- 15_diagnosticos_bf.csv: alertas de prior, CDF e IBNR BF.
- 16_configuracion_chain_ladder.json: selección, cola y parámetros.
- 17_configuracion_bf.json: definición del prior, columnas y shocks.
- 18_manifiesto.json: versión, hashes y trazabilidad de fuentes agregadas.

Ambos métodos son determinísticos. La fuente del prior, la exposición, los factores,
la cola y la representatividad histórica requieren juicio actuarial documentado,
reconciliación independiente y gobierno antes de cualquier uso profesional.
"""

    cdf_frame = chain_ladder.cdf_to_ultimate.rename_axis("edad_desarrollo").reset_index()
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
        archive.writestr("05_cdf_a_ultimate.csv", _csv_bytes(cdf_frame))
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
            _csv_bytes(chain_ladder.origin_summary, include_index=True),
        )
        archive.writestr("09_totales_chain_ladder.csv", _csv_bytes(chain_ladder.totals))
        archive.writestr("10_diagnosticos_chain_ladder.csv", _csv_bytes(chain_ladder.diagnostics))
        archive.writestr("11_prior_bf_normalizado.csv", prior_bytes)
        archive.writestr(
            "12_resultados_bf_por_origen.csv",
            _csv_bytes(bornhuetter_ferguson.origin_summary, include_index=True),
        )
        archive.writestr("13_totales_bf.csv", _csv_bytes(bornhuetter_ferguson.totals))
        archive.writestr(
            "14_sensibilidad_prior_bf.csv",
            _csv_bytes(bornhuetter_ferguson.sensitivity),
        )
        archive.writestr(
            "15_diagnosticos_bf.csv",
            _csv_bytes(bornhuetter_ferguson.diagnostics),
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
    return buffer.getvalue()
