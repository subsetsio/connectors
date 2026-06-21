"""BSP per-table statistical workbooks (the parametric Excel family).

The bsp.gov.ph statistics portal is a SharePoint site whose statistical
time-series live in per-table Excel workbooks (one stable URL per table, linked
from each catalog item's EXCEL field). Most are legacy binary .xls; some .xlsx.

DuckDB's SQL transforms can only read parquet/ndjson/csv, so all Excel parsing
happens in Python (see ``utils._melt_workbook``). Each workbook is "melted" into
a uniform long format — (sheet, row_label, column_header, value) — which is
robust across the many heterogeneous BSP table layouts. The thin SQL transform
then casts/filters and publishes one Delta table per subset.

The consolidated Reference Exchange Rate Bulletin workbook
(``/Statistics/RERB/RERB.xlsx``) shares this exact melt + schema, so it is
fetched here too via a fixed URL.

Fetch shape: stateless full re-pull. Each workbook is small (KBs-MB) and
re-fetched in full every run; raw is overwritten. No watermark/cursor — BSP
publishes revisions in place. 18 catalog entries whose EXCEL+HTML links 404
upstream were dropped at rank time and are not part of the coverage set.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _excel_url, _get_bytes, _melt_workbook

# entity_id -> relative EXCEL path (from the SharePoint catalog). Built from the
# rank-accepted entity union; dead-link entries were dropped before this stage.
ENTITY_EXCEL = {
    "banking-20statistics-loan-20accounts-2-4": "/Statistics/Banking%20Statistics/Loan%20Accounts/2.4.xls",
    "banking-20statistics-physical-20network-1-1": "/Statistics/Banking%20Statistics/Physical%20Network/1.1.xls",
    "banking-20statistics-physical-20network-1-2": "/Statistics/Banking%20Statistics/Physical%20Network/1.2.xlsx",
    "banking-20statistics-physical-20network-2": "/Statistics/Banking%20Statistics/Physical%20Network/2.xls",
    "banking-20statistics-physical-20network-2-1": "/Statistics/Banking%20Statistics/Physical%20Network/2.1.xlsx",
    "banking-20statistics-physical-20network-2-2": "/Statistics/Banking%20Statistics/Physical%20Network/2.2.xlsx",
    "deposit-20accounts-2-3": "/Statistics/Deposit%20Accounts/2.3.xls",
    "external-bop-new": "/Statistics/external/bop-new.xls",
    "external-bop-pos": "/statistics/external/bop_pos.xls",
    "external-dailycrossrates": "/statistics/external/dailycrossrates.xlsx",
    "external-eer-new": "/statistics/external/eer_new.xlsx",
    "external-extdebt": "/statistics/external/extdebt.xls",
    "external-extdebt-country": "/statistics/external/extdebt_country.xls",
    "external-extdebt-creditor": "/statistics/external/extdebt_creditor.xls",
    "external-extdebt-currency": "/statistics/external/extdebt_currency.xls",
    "external-extdebt-mcb": "/statistics/external/extdebt_mcb.xls",
    "external-extdebtratios": "/Statistics/External/extdebtratios.xls",
    "external-fcdu-loans": "/statistics/external/fcdu-loans.xls",
    "external-fdi-country": "/statistics/external/fdi-country.xls",
    "external-fdi-country2": "/Statistics/External/fdi-country2.xls",
    "external-fdi-industrybpm6": "/statistics/external/fdi-industrybpm6.xls",
    "external-fpiflows": "/statistics/external/fpiflows.xls",
    "external-generalgovtextdebt": "/Statistics/External/generalgovtextdebt.xlsx",
    "external-gir": "/Statistics/External/gir.xls",
    "external-iip": "/statistics/external/iip.xls",
    "external-iip-bpm6": "/statistics/external/iip_bpm6.xls",
    "external-it-bpo": "/statistics/external/it-bpo.xls",
    "external-nfpi": "/statistics/external/nfpi.xls",
    "external-ofw": "/Statistics/External/ofw.xls",
    "external-ofwp": "/Statistics/External/ofwp.xls",
    "external-outstandingfcduloans-historical": "/statistics/external/outstandingFCDUloans_historical.xlsx",
    "external-pesocross": "/statistics/external/pesocross.xlsx",
    "external-pesodollar": "/statistics/external/pesodollar.xlsx",
    "external-sddsextdebt": "/Statistics/External/sddsextdebt.xls",
    "external-table1": "/Statistics/external/table1.xls",
    "external-table1-1": "/Statistics/external/table1.1.xls",
    "external-table1-10": "/Statistics/external/table1.10.xls",
    "external-table1-2": "/Statistics/external/table1.2.xls",
    "external-table1-3": "/Statistics/external/table1.3.xls",
    "external-table1-4": "/Statistics/external/table1.4.xls",
    "external-table1-5": "/Statistics/external/table1.5.xls",
    "external-table1-6": "/Statistics/external/table1.6.xls",
    "external-table1-7": "/Statistics/external/table1.7.xls",
    "external-table1-8": "/Statistics/external/table1.8.xls",
    "external-table1-9": "/Statistics/external/table1.9.xls",
    "external-totalextdebt": "/statistics/external/totalextdebt.xls",
    "external-uscross": "/statistics/external/uscross.xlsx",
    "financial-20statements-balance-20sheet-2-5": "/Statistics/Financial%20Statements/Balance%20Sheet/2.5.xlsx",
    "financial-20system-20accounts-bsa": "/Statistics/Financial%20System%20Accounts/bsa.xlsx",
    "financial-20system-20accounts-bspal": "/Statistics/Financial%20System%20Accounts/bspal.xls",
    "financial-20system-20accounts-bspinc": "/Statistics/Financial%20System%20Accounts/bspinc.xls",
    "financial-20system-20accounts-bsprates": "/Statistics/Financial%20System%20Accounts/bsprates.xls",
    "financial-20system-20accounts-dcs": "/Statistics/Financial%20System%20Accounts/dcs.xls",
    "financial-20system-20accounts-dcs-srf": "/Statistics/Financial%20System%20Accounts/dcs_srf.xlsx",
    "financial-20system-20accounts-fof-bpm6-historical": "/Statistics/Financial%20System%20Accounts/FOF_BPM6_Historical.xlsx",
    "financial-20system-20accounts-ibcl": "/Statistics/Financial%20System%20Accounts/ibcl.xls",
    "financial-20system-20accounts-kbloans2009": "/Statistics/Financial%20System%20Accounts/kbloans2009.xls",
    "financial-20system-20accounts-kbloanspbs": "/Statistics/Financial%20System%20Accounts/kbloanspbs.xls",
    "financial-20system-20accounts-mas": "/Statistics/Financial%20System%20Accounts/mas.xls",
    "financial-20system-20accounts-mas-srf": "/Statistics/Financial%20System%20Accounts/mas_srf.xlsx",
    "financial-20system-20accounts-monthlylendingratestype": "/Statistics/Financial%20System%20Accounts/monthlylendingratestype.xls",
    "financial-20system-20accounts-ms": "/Statistics/Financial%20System%20Accounts/ms.xls",
    "financial-20system-20accounts-nfi": "/Statistics/Financial%20System%20Accounts/nfi.xls",
    "financial-20system-20accounts-ofcs": "/statistics/financial%20system%20accounts/ofcs.xls",
    "financial-20system-20accounts-rel": "/Statistics/Financial%20System%20Accounts/rel.xls",
    "financial-20system-20accounts-rrmatrix": "/Statistics/Financial%20System%20Accounts/RRMatrix.xls",
    "financial-20system-20accounts-sdir": "/Statistics/Financial%20System%20Accounts/sdir.xls",
    "financial-20system-20accounts-weeklylendingratestype": "/Statistics/Financial%20System%20Accounts/weeklylendingratestype.xls",
    "otherrealsectoraccounts-labor": "/Statistics/OtherRealSectorAccounts/labor.xlsx",
    "otherrealsectoraccounts-ppi-2018": "/Statistics/OtherRealSectorAccounts/ppi_2018.xls",
    "prices-coreinflation2012": "/Statistics/Prices/coreinflation2012.xls",
    "prices-coreinflation2018": "/Statistics/Prices/coreinflation2018.xls",
    "prices-inf-bottom30-2018": "/Statistics/Prices/inf_bottom30_2018.xls",
    "prices-infrate-comm2012": "/Statistics/Prices/infrate_comm2012.xls",
    "prices-infrate-comm2018": "/Statistics/Prices/infrate_comm2018.xls",
    "prices-infrate2012": "/Statistics/Prices/infrate2012.xls",
    "prices-infrate2018": "/Statistics/Prices/infrate2018.xls",
    "prices-prices2012": "/Statistics/Prices/prices2012.xls",
    "prices-prices2018": "/Statistics/Prices/prices2018.xls",
    "prices-rppi": "/Statistics/Prices/RPPI.xlsx",
    "real-sector-accounts-gnicon2018-exp": "/Statistics/Real Sector Accounts/gnicon2018_exp.xls",
    "real-sector-accounts-gnicon2018-ind": "/Statistics/Real Sector Accounts/gnicon2018_ind.xls",
    "real-sector-accounts-gnicurrent-exp": "/Statistics/Real Sector Accounts/gnicurrent_exp.xls",
    "real-sector-accounts-gnicurrent-ind": "/Statistics/Real Sector Accounts/gnicurrent_ind.xls",
}

# Non-Excel-catalog entity handled by a dedicated fetch function (same melt).
RERB_XLSX = "/Statistics/RERB/RERB.xlsx"


# ---------------------------------------------------------------------------
# Fetch functions
# ---------------------------------------------------------------------------
def fetch_one(node_id: str) -> None:
    """Generic per-table Excel fetch + melt to long format."""
    asset = node_id
    entity_id = node_id[len("bangko-sentral-pilipinas-"):]
    rel = ENTITY_EXCEL[entity_id]
    content = _get_bytes(_excel_url(rel))
    rows = _melt_workbook(content, rel)
    if not rows:
        raise AssertionError(f"{entity_id}: parsed 0 numeric rows from {rel}")
    save_raw_ndjson(rows, asset)


def fetch_rerb(node_id: str) -> None:
    """Consolidated Reference Exchange Rate Bulletin workbook."""
    asset = node_id
    content = _get_bytes(_excel_url(RERB_XLSX))
    rows = _melt_workbook(content, RERB_XLSX)
    if not rows:
        raise AssertionError("RERB: parsed 0 numeric rows")
    save_raw_ndjson(rows, asset)


# ---------------------------------------------------------------------------
# DOWNLOAD_SPECS — one per Excel-family entity in the union
# ---------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bangko-sentral-pilipinas-{eid}",
        fn=fetch_one,
        kind="download",
    )
    for eid in sorted(ENTITY_EXCEL)
] + [
    NodeSpec(
        id="bangko-sentral-pilipinas-reference-exchange-rate-bulletin",
        fn=fetch_rerb,
        kind="download",
    ),
]


# ---------------------------------------------------------------------------
# TRANSFORM_SPECS — one published Delta table per subset
# ---------------------------------------------------------------------------
def _generic_sql(dep_id: str) -> str:
    # row_label/column_header are forced to VARCHAR: read_json_auto infers DATE
    # for tables whose labels are all dates, which would break TRIM and cause
    # schema drift across subsets.
    return f'''
        SELECT
            CAST(sheet AS VARCHAR)          AS sheet,
            CAST(row_label AS VARCHAR)      AS row_label,
            CAST(column_header AS VARCHAR)  AS column_header,
            TRY_CAST(value AS DOUBLE)       AS value,
            CAST(row_index AS INTEGER)      AS row_index,
            CAST(col_index AS INTEGER)      AS col_index
        FROM "{dep_id}"
        WHERE value IS NOT NULL
          AND row_label IS NOT NULL
          AND TRIM(CAST(row_label AS VARCHAR)) <> ''
          AND TRY_CAST(value AS DOUBLE) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_generic_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
