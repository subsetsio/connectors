"""Scripps CO2 Program connector.

Bulk-CSV source: every published subset is one or more CSV files under the open
Apache directory index https://keelinglabsites.ucsd.edu/websitedataco2/ . There
is no incremental query surface and each file is the complete record, so the
fetch is a **stateless full re-pull** — every refresh downloads each file in
full and overwrites. Files are small (KB to ~1MB); a full re-pull is seconds.

The CSVs are heterogeneous: each opens with a ~50-line quoted (`"`) or `%`
comment header, then a multi-row column-name header, then comma-separated data.
We classify each subset into a *format family* with a known fixed column layout
and parse data rows positionally into named NDJSON records; the SQL transforms
are then thin casts. Station-partitioned families (one CSV per sampling station,
identical schema) fold all stations into one table with a `station` column.

Missing values in source are `-99.99` / `-999.99` / `NaN` -> null.
"""

import re
from datetime import date as _date, datetime


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://keelinglabsites.ucsd.edu/websitedataco2/"
EARLY_LAJOLLA_BASE = (
    "https://www.scrippsco2.ucsd.edu/assets/data/atmospheric/stations/in_situ_co2"
)

# --- entity (subset) -> source CSV filenames (the rank-accepted entity union) ---
# Station-folded families list one CSV per sampling station; all share a schema.
NODE_FILES = {
    'scripps-co2-bats': ['BATS.csv'],
    'scripps-co2-berm': ['BERM.csv'],
    'scripps-co2-early-lajolla-co2-halfhourly-1958-1962': [f'{EARLY_LAJOLLA_BASE}/halfhourly/Early_LaJolla_CO2_halfhourly_1958-1962.csv'],
    'scripps-co2-early-lajolla-co2-monthly-1957-1962': [f'{EARLY_LAJOLLA_BASE}/monthly/Early_LaJolla_CO2_weekly_monthly_1957-1962.csv'],
    'scripps-co2-early-lajolla-co2-weekly-minima-1957-1962': [f'{EARLY_LAJOLLA_BASE}/weekly/Early_LaJolla_CO2_weekly_minima_1957-1962.csv'],
    'scripps-co2-hawi': ['HAWI.csv'],
    'scripps-co2-daily-flask-c13': ['daily_flask_c13_alt.csv', 'daily_flask_c13_bat.csv', 'daily_flask_c13_bcs.csv', 'daily_flask_c13_chr.csv', 'daily_flask_c13_cms.csv', 'daily_flask_c13_fan.csv', 'daily_flask_c13_hip.csv', 'daily_flask_c13_ker.csv', 'daily_flask_c13_kor.csv', 'daily_flask_c13_kum.csv', 'daily_flask_c13_lab.csv', 'daily_flask_c13_ljo.csv', 'daily_flask_c13_mhd.csv', 'daily_flask_c13_mko.csv', 'daily_flask_c13_mlo.csv', 'daily_flask_c13_nzd.csv', 'daily_flask_c13_psa.csv', 'daily_flask_c13_ptb.csv', 'daily_flask_c13_sam.csv', 'daily_flask_c13_spo.csv', 'daily_flask_c13_stp.csv'],
    'scripps-co2-daily-flask-c14': ['daily_flask_c14_alt.csv', 'daily_flask_c14_bat.csv', 'daily_flask_c14_bcs.csv', 'daily_flask_c14_chr.csv', 'daily_flask_c14_cms.csv', 'daily_flask_c14_fan.csv', 'daily_flask_c14_hip.csv', 'daily_flask_c14_ker.csv', 'daily_flask_c14_kor.csv', 'daily_flask_c14_kum.csv', 'daily_flask_c14_lab.csv', 'daily_flask_c14_ljo.csv', 'daily_flask_c14_mhd.csv', 'daily_flask_c14_mko.csv', 'daily_flask_c14_mlo.csv', 'daily_flask_c14_nzd.csv', 'daily_flask_c14_psa.csv', 'daily_flask_c14_ptb.csv', 'daily_flask_c14_sam.csv', 'daily_flask_c14_spo.csv', 'daily_flask_c14_stp.csv'],
    'scripps-co2-daily-flask-ch4': ['daily_flask_ch4_alt.csv', 'daily_flask_ch4_bat.csv', 'daily_flask_ch4_bcs.csv', 'daily_flask_ch4_chr.csv', 'daily_flask_ch4_cms.csv', 'daily_flask_ch4_fan.csv', 'daily_flask_ch4_hip.csv', 'daily_flask_ch4_ker.csv', 'daily_flask_ch4_kor.csv', 'daily_flask_ch4_kum.csv', 'daily_flask_ch4_lab.csv', 'daily_flask_ch4_ljo.csv', 'daily_flask_ch4_mhd.csv', 'daily_flask_ch4_mko.csv', 'daily_flask_ch4_mlo.csv', 'daily_flask_ch4_nzd.csv', 'daily_flask_ch4_psa.csv', 'daily_flask_ch4_ptb.csv', 'daily_flask_ch4_sam.csv', 'daily_flask_ch4_spo.csv', 'daily_flask_ch4_stp.csv'],
    'scripps-co2-daily-flask-co': ['daily_flask_co_alt.csv', 'daily_flask_co_bat.csv', 'daily_flask_co_bcs.csv', 'daily_flask_co_chr.csv', 'daily_flask_co_cms.csv', 'daily_flask_co_fan.csv', 'daily_flask_co_hip.csv', 'daily_flask_co_ker.csv', 'daily_flask_co_kor.csv', 'daily_flask_co_kum.csv', 'daily_flask_co_lab.csv', 'daily_flask_co_ljo.csv', 'daily_flask_co_mhd.csv', 'daily_flask_co_mko.csv', 'daily_flask_co_mlo.csv', 'daily_flask_co_nzd.csv', 'daily_flask_co_psa.csv', 'daily_flask_co_ptb.csv', 'daily_flask_co_sam.csv', 'daily_flask_co_spo.csv', 'daily_flask_co_stp.csv'],
    'scripps-co2-daily-flask-co2': ['daily_flask_co2_alt.csv', 'daily_flask_co2_bat.csv', 'daily_flask_co2_bcs.csv', 'daily_flask_co2_chr.csv', 'daily_flask_co2_cms.csv', 'daily_flask_co2_fan.csv', 'daily_flask_co2_hip.csv', 'daily_flask_co2_ker.csv', 'daily_flask_co2_kor.csv', 'daily_flask_co2_kum.csv', 'daily_flask_co2_lab.csv', 'daily_flask_co2_ljo.csv', 'daily_flask_co2_mhd.csv', 'daily_flask_co2_mko.csv', 'daily_flask_co2_mlo.csv', 'daily_flask_co2_nzd.csv', 'daily_flask_co2_psa.csv', 'daily_flask_co2_ptb.csv', 'daily_flask_co2_sam.csv', 'daily_flask_co2_spo.csv', 'daily_flask_co2_stp.csv'],
    'scripps-co2-daily-flask-o18': ['daily_flask_o18_alt.csv', 'daily_flask_o18_bat.csv', 'daily_flask_o18_bcs.csv', 'daily_flask_o18_chr.csv', 'daily_flask_o18_cms.csv', 'daily_flask_o18_fan.csv', 'daily_flask_o18_hip.csv', 'daily_flask_o18_ker.csv', 'daily_flask_o18_kor.csv', 'daily_flask_o18_kum.csv', 'daily_flask_o18_lab.csv', 'daily_flask_o18_ljo.csv', 'daily_flask_o18_mhd.csv', 'daily_flask_o18_mko.csv', 'daily_flask_o18_mlo.csv', 'daily_flask_o18_nzd.csv', 'daily_flask_o18_psa.csv', 'daily_flask_o18_ptb.csv', 'daily_flask_o18_sam.csv', 'daily_flask_o18_spo.csv', 'daily_flask_o18_stp.csv'],
    'scripps-co2-daily-flask-co2-isotopes': ['daily_flask_co2_isotopes_alt.csv', 'daily_flask_co2_isotopes_bcs.csv', 'daily_flask_co2_isotopes_chr.csv', 'daily_flask_co2_isotopes_fan.csv', 'daily_flask_co2_isotopes_ker.csv', 'daily_flask_co2_isotopes_kum.csv', 'daily_flask_co2_isotopes_ljo.csv', 'daily_flask_co2_isotopes_mlo.csv', 'daily_flask_co2_isotopes_nzd.csv', 'daily_flask_co2_isotopes_ptb.csv', 'daily_flask_co2_isotopes_sam.csv', 'daily_flask_co2_isotopes_spo.csv', 'daily_flask_co2_isotopes_stp.csv'],
    'scripps-co2-monthly-flask-c13': ['monthly_flask_c13_alt.csv', 'monthly_flask_c13_bat.csv', 'monthly_flask_c13_bcs.csv', 'monthly_flask_c13_chr.csv', 'monthly_flask_c13_cms.csv', 'monthly_flask_c13_fan.csv', 'monthly_flask_c13_hip.csv', 'monthly_flask_c13_ker.csv', 'monthly_flask_c13_kor.csv', 'monthly_flask_c13_kum.csv', 'monthly_flask_c13_lab.csv', 'monthly_flask_c13_ljo.csv', 'monthly_flask_c13_mhd.csv', 'monthly_flask_c13_mko.csv', 'monthly_flask_c13_mlo.csv', 'monthly_flask_c13_nzd.csv', 'monthly_flask_c13_psa.csv', 'monthly_flask_c13_ptb.csv', 'monthly_flask_c13_sam.csv', 'monthly_flask_c13_spo.csv', 'monthly_flask_c13_stp.csv'],
    'scripps-co2-monthly-flask-ch4': ['monthly_flask_ch4_alt.csv', 'monthly_flask_ch4_bat.csv', 'monthly_flask_ch4_bcs.csv', 'monthly_flask_ch4_chr.csv', 'monthly_flask_ch4_cms.csv', 'monthly_flask_ch4_fan.csv', 'monthly_flask_ch4_hip.csv', 'monthly_flask_ch4_ker.csv', 'monthly_flask_ch4_kor.csv', 'monthly_flask_ch4_kum.csv', 'monthly_flask_ch4_lab.csv', 'monthly_flask_ch4_ljo.csv', 'monthly_flask_ch4_mhd.csv', 'monthly_flask_ch4_mko.csv', 'monthly_flask_ch4_mlo.csv', 'monthly_flask_ch4_nzd.csv', 'monthly_flask_ch4_psa.csv', 'monthly_flask_ch4_ptb.csv', 'monthly_flask_ch4_sam.csv', 'monthly_flask_ch4_spo.csv', 'monthly_flask_ch4_stp.csv'],
    'scripps-co2-monthly-flask-co': ['monthly_flask_co_alt.csv', 'monthly_flask_co_bat.csv', 'monthly_flask_co_bcs.csv', 'monthly_flask_co_chr.csv', 'monthly_flask_co_cms.csv', 'monthly_flask_co_fan.csv', 'monthly_flask_co_hip.csv', 'monthly_flask_co_ker.csv', 'monthly_flask_co_kor.csv', 'monthly_flask_co_kum.csv', 'monthly_flask_co_lab.csv', 'monthly_flask_co_ljo.csv', 'monthly_flask_co_mhd.csv', 'monthly_flask_co_mko.csv', 'monthly_flask_co_mlo.csv', 'monthly_flask_co_nzd.csv', 'monthly_flask_co_psa.csv', 'monthly_flask_co_ptb.csv', 'monthly_flask_co_sam.csv', 'monthly_flask_co_spo.csv', 'monthly_flask_co_stp.csv'],
    'scripps-co2-monthly-flask-co2': ['monthly_flask_co2_alt.csv', 'monthly_flask_co2_bat.csv', 'monthly_flask_co2_bcs.csv', 'monthly_flask_co2_chr.csv', 'monthly_flask_co2_cms.csv', 'monthly_flask_co2_fan.csv', 'monthly_flask_co2_hip.csv', 'monthly_flask_co2_ker.csv', 'monthly_flask_co2_kor.csv', 'monthly_flask_co2_kum.csv', 'monthly_flask_co2_lab.csv', 'monthly_flask_co2_ljo.csv', 'monthly_flask_co2_mhd.csv', 'monthly_flask_co2_mko.csv', 'monthly_flask_co2_mlo.csv', 'monthly_flask_co2_nzd.csv', 'monthly_flask_co2_psa.csv', 'monthly_flask_co2_ptb.csv', 'monthly_flask_co2_sam.csv', 'monthly_flask_co2_spo.csv', 'monthly_flask_co2_stp.csv'],
    'scripps-co2-monthly-flask-o18': ['monthly_flask_o18_alt.csv', 'monthly_flask_o18_bat.csv', 'monthly_flask_o18_bcs.csv', 'monthly_flask_o18_chr.csv', 'monthly_flask_o18_cms.csv', 'monthly_flask_o18_fan.csv', 'monthly_flask_o18_hip.csv', 'monthly_flask_o18_ker.csv', 'monthly_flask_o18_kor.csv', 'monthly_flask_o18_kum.csv', 'monthly_flask_o18_lab.csv', 'monthly_flask_o18_ljo.csv', 'monthly_flask_o18_mhd.csv', 'monthly_flask_o18_mko.csv', 'monthly_flask_o18_mlo.csv', 'monthly_flask_o18_nzd.csv', 'monthly_flask_o18_psa.csv', 'monthly_flask_o18_ptb.csv', 'monthly_flask_o18_sam.csv', 'monthly_flask_o18_spo.csv', 'monthly_flask_o18_stp.csv'],
    'scripps-co2-daily-merge-co2': ['daily_merge_co2_ljo.csv', 'daily_merge_co2_ptb.csv', 'daily_merge_co2_spo.csv'],
    'scripps-co2-monthly-merge-co2': ['monthly_merge_co2_ljo.csv', 'monthly_merge_co2_ptb.csv', 'monthly_merge_co2_spo.csv'],
    'scripps-co2-daily-in-situ-co2': ['daily_in_situ_co2_mlo.csv', 'daily_in_situ_co2_ptb.csv'],
    'scripps-co2-weekly-in-situ-co2': ['weekly_in_situ_co2_mlo.csv'],
    'scripps-co2-monthly-in-situ-co2': ['monthly_in_situ_co2_mlo.csv'],
    'scripps-co2-intermittent-flask-c14': ['intermittent_flask_c14_kum.csv', 'intermittent_flask_c14_ljo.csv', 'intermittent_flask_c14_mlo.csv', 'intermittent_flask_c14_psa.csv', 'intermittent_flask_c14_ptb.csv', 'intermittent_flask_c14_ptb1.csv', 'intermittent_flask_c14_ptb2.csv', 'intermittent_flask_c14_sam.csv', 'intermittent_flask_c14_spo.csv'],
    'scripps-co2-intermittent-flask-c14-spline': ['intermittent_flask_c14_spline_kum.csv', 'intermittent_flask_c14_spline_ljo.csv', 'intermittent_flask_c14_spline_mlo.csv', 'intermittent_flask_c14_spline_psa.csv', 'intermittent_flask_c14_spline_ptb1.csv', 'intermittent_flask_c14_spline_ptb2.csv', 'intermittent_flask_c14_spline_sam.csv', 'intermittent_flask_c14_spline_spo.csv'],
    'scripps-co2-mlo-spo-annual-mean': ['mlo_spo_annual_mean.csv'],
    'scripps-co2-mlo-spo-monthly-mean': ['mlo_spo_monthly_mean.csv'],
    'scripps-co2-merged-ice-core-yearly': ['merged_ice_core_yearly.csv'],
    'scripps-co2-spline-merged-ice-core-yearly': ['spline_merged_ice_core_yearly.csv'],
}

# Families that carry a per-file `station` column (folded multi-station tables,
# or the seawater single-station files). Global/derived products (means, ice
# core) have no station.
_NO_STATION = {"ice_core", "mlo_spo_annual", "mlo_spo_monthly"}

_RE_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_RE_DMY = re.compile(r"^\d{1,2}-[A-Za-z]{3}-\d{2}$")


# --------------------------------------------------------------------------- #
# HTTP                                                                         #
# --------------------------------------------------------------------------- #


@transient_retry()
def _download(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _source_url(filename: str) -> str:
    if filename.startswith(("http://", "https://")):
        return filename
    return BASE + filename


# --------------------------------------------------------------------------- #
# Parsing helpers                                                              #
# --------------------------------------------------------------------------- #
def _num(x):
    """Float or None. Source missing-value sentinels (-99.99 / -999.99 / NaN)
    and blanks become None."""
    x = x.strip()
    if x in ("", "NaN", "nan", "NA", "*"):
        return None
    try:
        v = float(x)
    except ValueError:
        return None
    if abs(v + 99.99) < 0.01 or abs(v + 999.99) < 0.01:
        return None
    return v


def _int(x):
    x = x.strip()
    if x in ("", "NaN", "nan"):
        return None
    try:
        return int(x)
    except ValueError:
        try:
            return int(float(x))
        except ValueError:
            return None


def _is_year(t: str) -> bool:
    t = t.strip()
    if len(t) != 4 or not t.isdigit():
        return False
    return 1700 <= int(t) <= 2100


def _valid_date(s: str) -> bool:
    """True only for a real ISO calendar date. Guards against placeholder rows
    like '0000-00-00' that some flask files carry for undated samples."""
    if not _RE_ISO.match(s):
        return False
    try:
        _date.fromisoformat(s)
        return True
    except ValueError:
        return False


def _ymd(y, m, d):
    """Return ISO date string, or None if the y/m/d don't form a real date."""
    try:
        return _date(int(y), int(m), int(d)).isoformat()
    except (ValueError, TypeError):
        return None


def _dmy_to_iso(s: str):
    """'19-Nov-99' -> ISO date. Two-digit years that resolve into the future
    (strptime maps 00-68 -> 2000s) are pulled back a century."""
    dt = datetime.strptime(s.strip(), "%d-%b-%y")
    if dt.year > 2030:
        dt = dt.replace(year=dt.year - 100)
    return dt.date().isoformat()


# --- per-family data-row parsers: return dict, or None to skip the line ---
def _p_flask_std(f):
    if len(f) < 7 or not _valid_date(f[0]):
        return None
    return {
        "date": f[0],
        "decimal_date": _num(f[3]),
        "n_flasks": _int(f[4]),
        "flag": _int(f[5]),
        "value": _num(f[6]),
    }


def _p_flask_isotopes(f):
    if len(f) < 22 or not _valid_date(f[0]):
        return None
    return {
        "date": f[0],
        "decimal_date": _num(f[3]),
        "co2": _num(f[6]),
        "co2_flag": _int(f[5]),
        "ch4": _num(f[9]),
        "ch4_flag": _int(f[8]),
        "co": _num(f[12]),
        "co_flag": _int(f[11]),
        "c13_co2": _num(f[15]),
        "c13_flag": _int(f[14]),
        "o18_co2": _num(f[18]),
        "o18_flag": _int(f[17]),
        "c14_co2": _num(f[21]),
        "c14_flag": _int(f[20]),
    }


def _p_flask_monthly(f):
    if len(f) < 10 or not _is_year(f[0]):
        return None
    return {
        "year": _int(f[0]),
        "month": _int(f[1]),
        "decimal_date": _num(f[3]),
        "value": _num(f[4]),
        "value_seasonally_adjusted": _num(f[5]),
        "fit": _num(f[6]),
        "fit_seasonally_adjusted": _num(f[7]),
        "value_filled": _num(f[8]),
        "value_filled_seasonally_adjusted": _num(f[9]),
    }


def _p_insitu_monthly(f):
    if len(f) < 11 or not _is_year(f[0]):
        return None
    rec = _p_flask_monthly(f)
    rec["sub_station"] = f[10].strip() or None
    return rec


def _p_insitu_daily(f):
    if len(f) < 6 or not _is_year(f[0]):
        return None
    iso = _ymd(f[0], f[1], f[2])
    if iso is None:
        return None
    return {
        "date": iso,
        "value": _num(f[3]),
        "n_baseline": _int(f[4]),
        "scale": f[5].strip() or None,
    }


def _p_insitu_weekly(f):
    if len(f) < 2 or not _valid_date(f[0]):
        return None
    return {"date": f[0], "value": _num(f[1])}


def _p_intermittent_c14(f):
    if len(f) < 2 or not _RE_DMY.match(f[0]):
        return None
    return {"date": _dmy_to_iso(f[0]), "value": _num(f[1])}


def _p_decimal_value(f):
    """Two columns: decimal-year, value (intermittent spline + annual mean)."""
    if len(f) < 2:
        return None
    dv = _num(f[0])
    if dv is None or not (1700.0 <= dv <= 2100.0):
        return None
    return {"decimal_date": dv, "value": _num(f[1])}


def _p_mlo_spo_monthly(f):
    if len(f) < 6 or not _is_year(f[0]):
        return None
    return {
        "year": _int(f[0]),
        "month": _int(f[1]),
        "fill_flag": _int(f[2]),
        "mlo": _num(f[3]),
        "spo": _num(f[4]),
        "average": _num(f[5]),
    }


def _p_ice_core(f):
    if len(f) < 2:
        return None
    yr = _num(f[0])
    if yr is None:
        return None
    return {"year_ce": yr, "co2": _num(f[1])}


def _p_seawater(f):
    # Station, Sample-Date, Excel, Decimal, Depth, Salinity, Temp, d13C-DIC, DIC, ALK
    if len(f) < 10 or not _valid_date(f[1]):
        return None
    return {
        "sample_date": f[1],
        "depth": _num(f[4]),
        "salinity": _num(f[5]),
        "temperature": _num(f[6]),
        "d13c_dic": _num(f[7]),
        "dic": _num(f[8]),
        "alk": _num(f[9]),
    }


def _p_early_lajolla(f):
    if not f:
        return None
    if _valid_date(f[0]):
        value = _num(f[-1])
        if value is None:
            return None
        return {"date": f[0], "value": value}
    if len(f) >= 3 and _is_year(f[0]):
        year = _int(f[0])
        month = _int(f[1])
        day = _int(f[2]) if len(f) >= 4 else 15
        value = _num(f[-1])
        if value is None:
            return None
        rec = {
            "year": year,
            "month": month,
            "day": day,
            "date": _ymd(year, month, day),
            "value": value,
        }
        if len(f) >= 5:
            rec["hour"] = _int(f[3])
        if len(f) >= 6:
            rec["minute"] = _int(f[4])
        return rec if rec["date"] else None
    return None


_PARSERS = {
    "flask_std": _p_flask_std,
    "flask_isotopes": _p_flask_isotopes,
    "flask_monthly": _p_flask_monthly,
    "insitu_monthly": _p_insitu_monthly,
    "insitu_daily": _p_insitu_daily,
    "insitu_weekly": _p_insitu_weekly,
    "intermittent_c14": _p_intermittent_c14,
    "intermittent_c14_spline": _p_decimal_value,
    "mlo_spo_annual": _p_decimal_value,
    "mlo_spo_monthly": _p_mlo_spo_monthly,
    "ice_core": _p_ice_core,
    "seawater": _p_seawater,
    "early_lajolla": _p_early_lajolla,
}


def _family(node_id: str) -> str:
    n = node_id[len("scripps-co2-"):]
    if n.startswith("early-lajolla-co2-"):
        return "early_lajolla"
    if n in ("bats", "berm", "hawi"):
        return "seawater"
    if n in ("merged-ice-core-yearly", "spline-merged-ice-core-yearly"):
        return "ice_core"
    if n == "mlo-spo-annual-mean":
        return "mlo_spo_annual"
    if n == "mlo-spo-monthly-mean":
        return "mlo_spo_monthly"
    if n == "daily-in-situ-co2":
        return "insitu_daily"
    if n == "weekly-in-situ-co2":
        return "insitu_weekly"
    if n == "monthly-in-situ-co2":
        return "insitu_monthly"
    if n == "intermittent-flask-c14":
        return "intermittent_c14"
    if n == "intermittent-flask-c14-spline":
        return "intermittent_c14_spline"
    if n == "daily-flask-co2-isotopes":
        return "flask_isotopes"
    if n.startswith("daily-flask-") or n == "daily-merge-co2":
        return "flask_std"
    if n.startswith("monthly-flask-") or n == "monthly-merge-co2":
        return "flask_monthly"
    raise ValueError(f"no family for {node_id}")


def _station_of(filename: str, family: str):
    stem = filename[:-4]  # strip .csv
    if family == "seawater":
        return stem  # BATS / BERM / HAWI
    return stem.split("_")[-1]  # mlo, spo, ptb1, ...


# --------------------------------------------------------------------------- #
# Fetch — one shared fn for every subset                                      #
# --------------------------------------------------------------------------- #
def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    family = _family(node_id)
    parse = _PARSERS[family]
    with_station = family not in _NO_STATION

    rows = []
    for filename in NODE_FILES[node_id]:
        station = _station_of(filename, family) if with_station else None
        text = _download(_source_url(filename))
        for line in text.splitlines():
            s = line.lstrip()
            if not s or s[0] in ('"', "%"):
                continue  # comment / blank
            fields = [c.strip() for c in line.split(",")]
            rec = parse(fields)
            if rec is None:
                continue  # column-name header or non-data line
            if with_station:
                rec["station"] = station
            rows.append(rec)

    if not rows:
        raise AssertionError(f"{asset}: parsed 0 data rows from {NODE_FILES[node_id]}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=node_id, fn=fetch_one, kind="download")
    for node_id in NODE_FILES
]
