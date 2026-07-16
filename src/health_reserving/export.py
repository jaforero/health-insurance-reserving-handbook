"""In-memory exports for the local triangle workshop."""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone

import pandas as pd

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
