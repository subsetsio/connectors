"""Parsing helpers for the National Bank of Slovakia connector.

Kept out of the node module because the MEDB xlsx melt and the DSW / FX
parsers are long enough to dwarf the fetch fns. `src/` is on the runner path,
so `from utils import ...` resolves at validation and runtime.
"""
from __future__ import annotations

import csv
import datetime as _dt
import io
import numbers
import re
import zipfile


# ---------------------------------------------------------------------------
# Slovak-locale number parsing
# ---------------------------------------------------------------------------
def parse_number(raw) -> float | None:
    """Parse a value that may be a real number or a locale-formatted string.

    Handles Slovak decimal-comma and thousands separators, and treats Excel
    error strings (`#N/A`, `#DIV/0!`, ...) and blanks as null.
    """
    if raw is None:
        return None
    if isinstance(raw, bool):
        return None
    if isinstance(raw, numbers.Number):
        return float(raw)
    s = str(raw).strip()
    if not s or s.startswith("#") or s.upper() in {"N/A", "NA", "-"}:
        return None
    s = s.replace("\xa0", "").replace(" ", "")
    has_dot = "." in s
    has_comma = "," in s
    if has_dot and has_comma:
        # Whichever separator appears last is the decimal separator.
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")   # 1.234,56 -> 1234.56
        else:
            s = s.replace(",", "")                       # 1,234.56 -> 1234.56
    elif has_comma:
        s = s.replace(",", ".")                          # 1,0 -> 1.0
    try:
        return float(s)
    except ValueError:
        return None


def parse_dmy(raw) -> _dt.date | None:
    """Parse a 'dd.mm.yyyy' (or 'd.m.yyyy') string into a date."""
    if raw is None:
        return None
    if isinstance(raw, _dt.datetime):
        return raw.date()
    if isinstance(raw, _dt.date):
        return raw
    s = str(raw).strip()
    if not s:
        return None
    m = re.match(r"^(\d{1,2})\.(\d{1,2})\.(\d{4})$", s)
    if not m:
        return None
    d, mo, y = (int(x) for x in m.groups())
    try:
        return _dt.date(y, mo, d)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# MEDB macroeconomic-database xlsx: melt the M/Q/A "Level" sheets to long form
# ---------------------------------------------------------------------------
def _expand_2digit_year(yy: int) -> int:
    return 1900 + yy if yy >= 50 else 2000 + yy


def _period_to_date(label, frequency: str):
    """Map a period-header cell to (period_label, period_start_date).

    Frequencies: 'M' header cells are datetimes; 'Q' are 'nQyy' strings;
    'A' are integer years. Returns None for a non-period cell.
    """
    if label is None:
        return None
    if frequency == "M":
        if isinstance(label, _dt.datetime):
            d = label.date()
        elif isinstance(label, _dt.date):
            d = label
        else:
            return None
        return (d.strftime("%Y-%m"), _dt.date(d.year, d.month, 1))
    if frequency == "A":
        if isinstance(label, numbers.Number) and not isinstance(label, bool):
            y = int(label)
            if 1900 <= y <= 2100:
                return (str(y), _dt.date(y, 1, 1))
        return None
    if frequency == "Q":
        m = re.match(r"^\s*([1-4])Q(\d{2})\s*$", str(label))
        if not m:
            return None
        q, yy = int(m.group(1)), int(m.group(2))
        year = _expand_2digit_year(yy)
        return (f"{q}Q{yy:02d}", _dt.date(year, (q - 1) * 3 + 1, 1))
    return None


def melt_level_sheet(ws, frequency: str) -> list[dict]:
    """Melt one MEDB 'Level' worksheet into long-format observation dicts.

    Layout: a single period-header row (col C == 'variable', with a period
    label in col G onward). Metadata columns are label-mapped from that header
    row (classcode / variable / detail / source). Every subsequent row with a
    string `variable` is a series; each numeric period cell becomes one row.
    """
    header_idx = None
    meta_cols: dict[str, int] = {}
    periods: list[tuple[int, str, _dt.date]] = []

    rows_iter = ws.iter_rows(values_only=True)
    for ridx, row in enumerate(rows_iter, start=1):
        if len(row) > 6 and row[2] == "variable" and row[6] is not None:
            header_idx = ridx
            for cidx, val in enumerate(row[:6]):
                if isinstance(val, str):
                    meta_cols[val.strip().lower()] = cidx
            for cidx in range(6, len(row)):
                got = _period_to_date(row[cidx], frequency)
                if got:
                    periods.append((cidx, got[0], got[1]))
            break

    if header_idx is None:
        raise RuntimeError(f"MEDB {frequency}: no period-header row found")
    if not periods:
        raise RuntimeError(f"MEDB {frequency}: header row carried no period columns")

    var_c = meta_cols.get("variable", 2)
    cls_c = meta_cols.get("classcode", 1)
    det_c = meta_cols.get("detail", 4)
    src_c = meta_cols.get("source", 5)

    out: list[dict] = []
    for row in rows_iter:  # continues after the header row
        variable = row[var_c] if len(row) > var_c else None
        if not isinstance(variable, str) or not variable.strip():
            continue
        classcode = row[cls_c] if len(row) > cls_c else None
        detail = row[det_c] if len(row) > det_c else None
        source = row[src_c] if len(row) > src_c else None
        for cidx, plabel, pdate in periods:
            if cidx >= len(row):
                continue
            value = parse_number(row[cidx])
            if value is None:
                continue
            out.append({
                "frequency": frequency,
                "series_key": f"{frequency}|{variable.strip()}|{(detail or '').strip()}",
                "classcode": (str(classcode).strip() if classcode is not None else None),
                "variable": variable.strip(),
                "detail": (str(detail).strip() if detail is not None else None),
                "source": (str(source).strip() if source is not None else None),
                "period_label": plabel,
                "date": pdate,
                "value": value,
            })
    return out


# ---------------------------------------------------------------------------
# DSW supervised-entity reporting: three cp1250 semicolon CSVs inside one ZIP
# ---------------------------------------------------------------------------
def _dsw_reader(zbytes: bytes, member: str):
    with zipfile.ZipFile(io.BytesIO(zbytes)) as zf:
        raw = zf.read(member)
    text = raw.decode("cp1250")
    return csv.reader(io.StringIO(text), delimiter=";")


def parse_dsw_report(zbytes: bytes) -> list[dict]:
    reader = _dsw_reader(zbytes, "dsw_report_data.csv")
    header = next(reader)
    idx = {name: i for i, name in enumerate(header)}
    out = []
    for row in reader:
        if not row or len(row) < len(header):
            continue
        out.append({
            "period": parse_dmy(row[idx["PERIOD"]]),
            "subject_code": row[idx["SUBJECT_CODE"]] or None,
            "val_type": row[idx["VAL_TYPE"]] or None,
            "currency": row[idx["CURRENCY"]] or None,
            "num_value": parse_number(row[idx["NUM_VALUE"]]),
            "subject_name_act": row[idx["SUBJECT_NAME_ACT"]] or None,
            "subject_name_hist": row[idx["SUBJECT_NAME_HIST"]] or None,
            "deputy_subject_code": row[idx["DEPUTY_SUBJECT_CODE"]] or None,
            "deputy_subject_name": row[idx["DEPUTY_SUBJECT_NAME"]] or None,
            "grp_name": row[idx["GRP_NAME"]] or None,
            "grp_parent_name": row[idx["GRP_PARENT_NAME"]] or None,
        })
    return out


def parse_dsw_generic(zbytes: bytes, member: str) -> list[dict]:
    """Read a DSW reference CSV verbatim (all columns as strings, blanks->null)."""
    reader = _dsw_reader(zbytes, member)
    header = [h.strip() for h in next(reader)]
    out = []
    for row in reader:
        if not row:
            continue
        rec = {}
        for i, col in enumerate(header):
            val = row[i] if i < len(row) else None
            rec[col.lower()] = (val or None)
        out.append(rec)
    return out


# ---------------------------------------------------------------------------
# Exchange rates
# ---------------------------------------------------------------------------
def parse_fx_daily_csv(text: str) -> list[dict]:
    """Parse one NBS daily reference-rate CSV (semicolon, BOM) to long rows.

    Header: Date;USD;JPY;... ; a single data row of rates (EUR base). The
    currency set varies over time, which is why long format is right.
    """
    text = text.lstrip("﻿").strip()
    if not text:
        return []
    reader = list(csv.reader(io.StringIO(text), delimiter=";"))
    if len(reader) < 2:
        return []
    header = reader[0]
    currencies = [c.strip() for c in header[1:]]
    out = []
    for datarow in reader[1:]:
        if not datarow or not datarow[0].strip():
            continue
        d = parse_dmy(datarow[0])
        if d is None:
            continue
        for i, ccy in enumerate(currencies, start=1):
            if i >= len(datarow):
                continue
            rate = parse_number(datarow[i])
            if rate is None:
                continue
            out.append({"date": d, "currency": ccy, "rate": rate})
    return out


_NBS_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def parse_fx_foreign_xml(xml_bytes: bytes) -> list[dict]:
    """Parse one NBS 'selected foreign currencies' monthly XML to long rows."""
    import xml.etree.ElementTree as ET

    root = ET.fromstring(xml_bytes)
    vf_el = root.find(f"{_NBS_NS}validFrom")
    num_el = root.find(f"{_NBS_NS}number")
    if vf_el is None or not (vf_el.text or "").strip():
        return []
    valid_from = _dt.date.fromisoformat(vf_el.text.strip())
    month_number = int(num_el.text) if num_el is not None and num_el.text else valid_from.month
    out = []
    for rate in root.iter(f"{_NBS_NS}rate"):
        def _txt(tag):
            el = rate.find(f"{_NBS_NS}{tag}")
            return (el.text or "").strip() if el is not None and el.text else None
        value = parse_number(_txt("value"))
        ccy = _txt("ccyCode")
        if value is None or not ccy:
            continue
        out.append({
            "valid_from": valid_from,
            "month_number": month_number,
            "country": _txt("country"),
            "currency_code": ccy,
            "currency_name": _txt("currency"),
            "value": value,
        })
    return out
