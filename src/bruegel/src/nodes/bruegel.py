"""Bruegel connector — the single node module the harness introspects and the
runtime DAG loads.

Each Bruegel dataset has its own module under ``src/datasets/`` holding the
parse/reshape logic, its resolved page path, and the publishing SQL. Those live
outside ``src/nodes/`` on purpose: ``load_nodes()`` globs every ``*.py`` under
``nodes/`` and fails on duplicate spec ids, so this file is the *only* spec
producer in ``nodes/``.

It wires each dataset into the DAG by defining one uniquely-named, top-level
``fetch_*`` wrapper per dataset — spawn-context execution and the harness's
top-level-function check both require a real module-level function (not a
closure or a re-exported ``fetch`` shared by every module) — and assembling the
two spec lists from the per-dataset modules' constants.
"""
from subsets_utils import NodeSpec, SqlNodeSpec
from utils import run_download
from datasets import (
    china, cleantech, divisia, energy_crisis, fms, gas_demand, gas_imports,
    gini, labour_market, reer, renewables, russian_trade, sovereign, trade,
)


# --- Bruegel-hosted datasets: resolve the page, then parse the linked file ---
def fetch_energy_crisis(node_id: str) -> None:
    run_download(node_id, energy_crisis.PAGE_PATH, energy_crisis.parse)


def fetch_divisia(node_id: str) -> None:
    run_download(node_id, divisia.PAGE_PATH, divisia.parse)


def fetch_labour_market(node_id: str) -> None:
    run_download(node_id, labour_market.PAGE_PATH, labour_market.parse)


def fetch_renewables(node_id: str) -> None:
    run_download(node_id, renewables.PAGE_PATH, renewables.parse)


def fetch_gas_imports(node_id: str) -> None:
    run_download(node_id, gas_imports.PAGE_PATH, gas_imports.parse)


def fetch_gini(node_id: str) -> None:
    run_download(node_id, None, gini.parse, direct_links=[gini.FILE_URL])


def fetch_trade(node_id: str) -> None:
    run_download(node_id, trade.PAGE_PATH, trade.parse)


def fetch_reer(node_id: str) -> None:
    run_download(node_id, reer.PAGE_PATH, reer.parse)


def fetch_russian_trade(node_id: str) -> None:
    run_download(node_id, russian_trade.PAGE_PATH, russian_trade.parse)


def fetch_sovereign(node_id: str) -> None:
    run_download(node_id, None, sovereign.parse,
                 direct_links=[sovereign.FILE_URL])


def fetch_fms(node_id: str) -> None:
    run_download(node_id, fms.PAGE_PATH, fms.parse)


# --- External-source datasets: no Bruegel page link (parse ignores links) ---
def fetch_china(node_id: str) -> None:
    run_download(node_id, None, china.parse)


def fetch_cleantech(node_id: str) -> None:
    run_download(node_id, None, cleantech.parse)


def fetch_gas_demand(node_id: str) -> None:
    run_download(node_id, None, gas_demand.parse)


DOWNLOAD_SPECS = [
    NodeSpec(id=energy_crisis.DEP, fn=fetch_energy_crisis, kind="download"),
    NodeSpec(id=china.DEP, fn=fetch_china, kind="download"),
    NodeSpec(id=divisia.DEP, fn=fetch_divisia, kind="download"),
    NodeSpec(id=labour_market.DEP, fn=fetch_labour_market, kind="download"),
    NodeSpec(id=renewables.DEP, fn=fetch_renewables, kind="download"),
    NodeSpec(id=cleantech.DEP, fn=fetch_cleantech, kind="download"),
    NodeSpec(id=gas_demand.DEP, fn=fetch_gas_demand, kind="download"),
    NodeSpec(id=gas_imports.DEP, fn=fetch_gas_imports, kind="download"),
    NodeSpec(id=gini.DEP, fn=fetch_gini, kind="download"),
    NodeSpec(id=trade.DEP, fn=fetch_trade, kind="download"),
    NodeSpec(id=reer.DEP, fn=fetch_reer, kind="download"),
    NodeSpec(id=russian_trade.DEP, fn=fetch_russian_trade, kind="download"),
    NodeSpec(id=sovereign.DEP, fn=fetch_sovereign, kind="download"),
    NodeSpec(id=fms.DEP, fn=fetch_fms, kind="download"),
]


# Per-dataset grain declarations (purely declarative; keyed by dataset module).
# Only the key=/temporal= kwargs are supplied — nothing else about the spec
# changes. Datasets whose grain is not confidently unique are left key-less;
# generic long extractions with no period column (china, cleantech) get neither.
_GRAIN = {
    energy_crisis: {"temporal": "date_announced"},
    divisia: {"temporal": "date"},
    labour_market: {"temporal": "year"},
    renewables: {"temporal": "year"},
    gas_demand: {"temporal": "date"},
    gas_imports: {"temporal": "date"},
    gini: {"temporal": "year"},
    trade: {"temporal": "date"},
    reer: {"temporal": "period"},
    russian_trade: {"temporal": "date"},
    sovereign: {"temporal": "date"},
    fms: {"key": ("id",), "temporal": "year"},
}


def _transform(mod) -> SqlNodeSpec:
    """Build the publishing leaf for a dataset module from its `_SQL` template."""
    return SqlNodeSpec(id=f"{mod.DEP}-transform", deps=[mod.DEP],
                       sql=mod._SQL.replace("{dep}", mod.DEP),
                       **_GRAIN.get(mod, {}))


TRANSFORM_SPECS = [
    _transform(mod) for mod in (
        energy_crisis, china, divisia, labour_market, renewables, cleantech,
        gas_demand, gas_imports, gini, trade, reer, russian_trade, sovereign, fms,
    )
]
