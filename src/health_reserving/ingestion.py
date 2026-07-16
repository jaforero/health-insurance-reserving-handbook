"""Local-only readers for the educational triangle application."""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd


TabularSource = str | Path | BinaryIO


def _extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def _rewind(source: TabularSource) -> None:
    if hasattr(source, "seek"):
        source.seek(0)


def excel_sheet_names(source: TabularSource) -> list[str]:
    """List Excel worksheets without persisting the uploaded file."""

    _rewind(source)
    book = pd.ExcelFile(source, engine="openpyxl")
    names = list(book.sheet_names)
    _rewind(source)
    return names


def read_tabular_file(
    source: TabularSource,
    filename: str,
    *,
    sheet_name: str | int = 0,
    separator: str = ",",
    decimal: str = ".",
    thousands: str | None = None,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """Read delimited text, XLSX or Parquet from a path or in-memory upload."""

    suffix = _extension(filename)
    _rewind(source)

    if suffix in {".csv", ".txt"}:
        sep = None if separator == "auto" else separator
        engine = "python" if sep is None else "c"
        options = {
            "sep": sep,
            "decimal": decimal,
            "thousands": thousands,
            "encoding": encoding,
            "engine": engine,
        }
        if engine == "c":
            options["low_memory"] = False
        frame = pd.read_csv(source, **options)
    elif suffix == ".xlsx":
        frame = pd.read_excel(
            source,
            sheet_name=sheet_name,
            engine="openpyxl",
        )
    elif suffix in {".parquet", ".pq"}:
        frame = pd.read_parquet(source, engine="pyarrow")
    else:
        raise ValueError(
            "Formato no soportado. Utilice CSV, TXT delimitado, XLSX o Parquet."
        )

    _rewind(source)
    if frame.empty:
        raise ValueError("El archivo no contiene filas de datos")
    if frame.columns.duplicated().any():
        duplicates = sorted(set(frame.columns[frame.columns.duplicated()].astype(str)))
        raise ValueError("El archivo contiene columnas repetidas: " + ", ".join(duplicates))

    frame.columns = [str(column).strip() for column in frame.columns]
    return frame
