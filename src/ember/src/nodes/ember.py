"""Ember electricity data connector.

Source: Ember (ember-energy.org), open CC-BY-4.0 bulk long-format CSVs served as
static files from files.ember-energy.org (GCS-backed). Six published subsets,
one per (geographic-scope x temporal-resolution):

  - global-yearly  : ~215 countries/regions, yearly from 2000
  - global-monthly : ~88 geographies, monthly from 2018
  - europe-yearly  : European countries + EU aggregate, yearly from 1990
  - europe-monthly : European countries + EU aggregate, monthly from 2015
  - us-yearly      : US state-level, yearly
  - us-monthly     : US state-level, monthly

The Europe files share the global files' column list but are a distinct Ember
product rather than a slice of them: they reach a decade further back, and they
disagree with the global file on the value of a few hundred overlapping
(Area, Year, Category, Subcategory, Variable) keys. They are therefore published
as their own tables rather than merged into the global ones.

Each file is one tidy/long table that bundles every metric Ember publishes
(generation, capacity, demand, power-sector emissions, carbon intensity) in the
Category/Subcategory/Variable columns. Unit belongs to the grain rather than
describing it: the same variable is published in several units (generation as
both TWh and % of the mix, emissions as both mtCO2 and gCO2/kWh).

Fetch shape: stateless full re-pull. Each CSV is a full snapshot (~8-105MB, no
incremental query support on the bulk path) re-fetched in full every run and
overwritten. Revisions/late corrections are picked up for free. No watermark,
no cursor.

US monthly extension: Ember stopped regenerating the US monthly bulk CSV
(last-modified 2026-03-19, data ending 2025-12) while its own US Electricity
Data Explorer kept publishing newer months through a datasette-style API
(generation_usa_monthly / overview_usa_monthly). Ember's documented API
(api.ember-energy.org) is country-grain only — it cannot serve this table's
state grain — and the site's download page still links the frozen file, so the
explorer API is the only upstream that carries current state-level months.
`fetch_one` therefore appends months AFTER the bulk file's max date, synthesized
from the explorer API into the exact bulk long format (validated cell-identical
against the bulk's own final month). Two deliberate reproductions of upstream
conventions:
  - The bulk file's 'Power sector emissions' Unit='%' rows carry the ktCO2
    value, not a share (an upstream defect present across the whole history);
    appended rows replicate it so the series stays internally consistent.
  - YoY absolute change = value - value(12 months earlier), YoY % change only
    when the prior value is > 0; both null for Unit='%' rows.
If the bulk file catches up past the explorer API, the extension appends
nothing and the connector degrades gracefully to bulk-only.
"""

import io

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_BASE = "https://files.ember-energy.org/public-downloads"

# The datasette-style API behind Ember's US Electricity Data Explorer — the only
# upstream serving state-level months past the frozen bulk CSV (see module doc).
_US_EXPLORER_API = (
    "https://ember-data-api-service-548422264620.europe-north1.run.app/ember"
)

_US_FUELS = (
    "'Bioenergy','Coal','Gas','Hydro','Nuclear',"
    "'Other Fossil','Other Renewables','Solar','Wind'"
)

ENTITY_URLS = {
    "global-yearly": f"{_BASE}/yearly_full_release_long_format.csv",
    "global-monthly": f"{_BASE}/monthly_full_release_long_format.csv",
    "europe-yearly": f"{_BASE}/europe_yearly_full_release_long_format.csv",
    "europe-monthly": f"{_BASE}/europe_monthly_full_release_long_format.csv",
    "us-yearly": f"{_BASE}/us_yearly_full_release_long_format.csv",
    "us-monthly": f"{_BASE}/us_monthly_full_release_long_format.csv",
}


@transient_retry()
def _download_csv(url: str) -> bytes:
    # Bulk static CSVs; generous read timeout for the ~105MB US monthly file.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _column_types(is_us: bool, is_monthly: bool) -> dict:
    """Explicit per-column types — the contract that keeps parquet stable across
    refreshes. The period column is the only structural difference between
    yearly (integer Year) and monthly (ISO-date string Date); the geographic
    columns differ between the country-level files (global, Europe) and the
    state-level US files.
    """
    period_col = "Date" if is_monthly else "Year"
    # Monthly periods are ISO first-of-month dates; parse them as real dates so
    # the raw carries the temporal type rather than a string that sorts by luck.
    period_type = pa.date32() if is_monthly else pa.int64()

    if is_us:
        geo = {
            "Country": pa.string(),
            "Country code": pa.string(),
            "State": pa.string(),
            "State code": pa.string(),
            "State type": pa.string(),
        }
    else:
        geo = {
            "Area": pa.string(),
            "ISO 3 code": pa.string(),
            "Area type": pa.string(),
            "Continent": pa.string(),
            "Ember region": pa.string(),
            "EU": pa.float64(),
            "OECD": pa.float64(),
            "G20": pa.float64(),
            "G7": pa.float64(),
            "ASEAN": pa.float64(),
        }

    types = dict(geo)
    types[period_col] = period_type
    types.update(
        {
            "Category": pa.string(),
            "Subcategory": pa.string(),
            "Variable": pa.string(),
            "Unit": pa.string(),
            "Value": pa.float64(),
            "YoY absolute change": pa.float64(),
            "YoY % change": pa.float64(),
        }
    )
    return types


@transient_retry()
def _fetch_explorer_csv(table_name: str, since: str, column_types: dict) -> pa.Table:
    """Stream rows with date > `since` from one US-explorer datasette table."""
    url = (
        f"{_US_EXPLORER_API}/{table_name}.csv"
        f"?date__gt={since}&_size=max&_stream=on"
    )
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return pacsv.read_csv(
        io.BytesIO(resp.content),
        convert_options=pacsv.ConvertOptions(
            column_types=column_types,
            strings_can_be_null=True,
        ),
    )


def _extend_us_monthly(bulk: pa.Table) -> pa.Table:
    """Append months newer than the frozen bulk CSV from the US-explorer API.

    Synthesizes the bulk long format (Category/Subcategory/Variable/Unit) from
    the explorer's wide tables, including the bulk file's own conventions —
    validated cell-identical against the bulk's final month (see module doc).
    """
    import duckdb

    bulk_max = pc.max(bulk.column("Date")).as_py()
    since = bulk_max.isoformat()

    gen = _fetch_explorer_csv(
        "generation_usa_monthly",
        since,
        {
            "rowid": pa.int64(),
            "country": pa.string(),
            "state": pa.string(),
            "date": pa.date32(),
            "variable": pa.string(),
            "generation_gwh": pa.float64(),
            "share_of_generation_pct": pa.float64(),
            "emissions_ktco2": pa.float64(),
            "share_of_emissions_pct": pa.float64(),
        },
    )
    if gen.num_rows == 0:
        return bulk  # bulk has caught up; nothing newer upstream
    ov = _fetch_explorer_csv(
        "overview_usa_monthly",
        since,
        {
            "rowid": pa.int64(),
            "country": pa.string(),
            "state": pa.string(),
            "date": pa.date32(),
            "demand_gwh": pa.float64(),
            "emissions_ktco2": pa.float64(),
            "emissions_intensity_gco2_per_kwh": pa.float64(),
        },
    )

    con = duckdb.connect()
    con.register("bulk", bulk)
    con.register("gen_api", gen)
    con.register("ov_api", ov)

    appended = con.sql(
        f"""
        with genr as (
            -- variable naming: the explorer says 'Wind and solar'; bulk says 'Wind and Solar'
            select state, date,
                   case variable when 'Wind and solar' then 'Wind and Solar'
                        else variable end as variable,
                   generation_gwh, share_of_generation_pct, emissions_ktco2
            from gen_api
            where date > date '{since}'
        ),
        ovr as (
            select state, date, emissions_ktco2, emissions_intensity_gco2_per_kwh
            from ov_api
            where date > date '{since}'
        ),
        -- aggregates the bulk file carries but the explorer does not
        derived as (
            select state, date, 'Gas and Other Fossil' as variable,
                   round(sum(generation_gwh), 2) as generation_gwh,
                   round(sum(share_of_generation_pct), 2) as share_of_generation_pct,
                   round(sum(emissions_ktco2), 2) as emissions_ktco2
            from genr where variable in ('Gas', 'Other Fossil') group by 1, 2
            union all
            select state, date, 'Hydro, Bioenergy and Other Renewables',
                   round(sum(generation_gwh), 2),
                   round(sum(share_of_generation_pct), 2),
                   round(sum(emissions_ktco2), 2)
            from genr where variable in ('Hydro', 'Bioenergy', 'Other Renewables')
            group by 1, 2
        ),
        wide as (select * from genr union all select * from derived),
        long as (
            select state, date, 'Electricity generation' as category,
                   case when variable in ({_US_FUELS}) then 'Fuel'
                        else 'Aggregate fuel' end as subcategory,
                   variable, 'GWh' as unit, generation_gwh as value
            from wide where generation_gwh is not null
            union all
            select state, date, 'Electricity generation',
                   case when variable in ({_US_FUELS}) then 'Fuel'
                        else 'Aggregate fuel' end,
                   variable, '%', share_of_generation_pct
            from wide where share_of_generation_pct is not null
            union all
            select state, date, 'Power sector emissions',
                   case when variable in ({_US_FUELS}) then 'Fuel'
                        else 'Aggregate fuel' end,
                   variable, 'ktCO2', emissions_ktco2
            from wide where emissions_ktco2 is not null
            union all
            -- upstream defect replicated deliberately: the bulk file's
            -- emissions '%' rows carry the ktCO2 value across the whole history
            select state, date, 'Power sector emissions',
                   case when variable in ({_US_FUELS}) then 'Fuel'
                        else 'Aggregate fuel' end,
                   variable, '%', emissions_ktco2
            from wide where emissions_ktco2 is not null
            union all
            select state, date, 'Electricity generation', 'Total',
                   'Total Generation', 'GWh', round(sum(generation_gwh), 2)
            from genr where variable in ('Fossil', 'Clean') group by state, date
            union all
            select state, date, 'Power sector emissions', 'Total',
                   'Total emissions', 'ktCO2', emissions_ktco2
            from ovr where emissions_ktco2 is not null
            union all
            select state, date, 'Power sector emissions', 'CO2 intensity',
                   'CO2 intensity', 'gCO2/kWh', emissions_intensity_gco2_per_kwh
            from ovr where emissions_intensity_gco2_per_kwh is not null
        ),
        states as (
            select distinct "Country" as country, "Country code" as country_code,
                   "State" as state, "State code" as state_code,
                   "State type" as state_type
            from bulk
        ),
        merged as (
            select state, date, category, subcategory, variable, unit, value from long
            union all
            select "State", "Date", "Category", "Subcategory", "Variable", "Unit",
                   "Value"
            from bulk
        )
        select s.country as "Country", s.country_code as "Country code",
               l.state as "State", s.state_code as "State code",
               s.state_type as "State type", l.date as "Date",
               l.category as "Category", l.subcategory as "Subcategory",
               l.variable as "Variable", l.unit as "Unit", l.value as "Value",
               case when l.unit <> '%' and p.value is not null
                    then round(l.value - p.value, 2)
               end as "YoY absolute change",
               case when l.unit <> '%' and p.value is not null and p.value > 0
                    then round((l.value - p.value) / p.value * 100, 2)
               end as "YoY % change"
        from long l
        join states s using (state)
        left join merged p
          on p.state = l.state
         and p.date + interval 1 year = l.date
         and p.category = l.category and p.subcategory = l.subcategory
         and p.variable = l.variable and p.unit = l.unit
        """
    ).fetch_arrow_table()

    appended = appended.select(bulk.column_names).cast(bulk.schema)
    return pa.concat_tables([bulk, appended])


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("ember-"):]
    url = ENTITY_URLS[entity]
    is_us = entity.startswith("us-")
    is_monthly = entity.endswith("-monthly")

    content = _download_csv(url)

    table = pacsv.read_csv(
        io.BytesIO(content),
        read_options=pacsv.ReadOptions(use_threads=True),
        convert_options=pacsv.ConvertOptions(
            column_types=_column_types(is_us, is_monthly),
            strings_can_be_null=True,
        ),
    )
    if entity == "us-monthly":
        table = _extend_us_monthly(table)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"ember-{entity}", fn=fetch_one, kind="download")
    for entity in ENTITY_URLS
]
