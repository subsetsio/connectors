"""OpenPrescribing (NHS England) connector.

OpenPrescribing (Bennett Institute, University of Oxford) republishes NHS England
GP prescribing data (sourced from NHSBSA) as standardised prescribing measures.
The live API is currently not usable from GitHub Actions because Cloudflare
returns HTTP 403 to the runner, so this connector publishes the repo-backed
reference data that can be fetched reliably:

  measures        reference catalog of the curated prescribing measures
  bnf_codes       BNF classification reference (codes referenced by the measures)

The measure definitions live in the source repo and are not behind the
openprescribing.net Cloudflare challenge.
"""

import json

from subsets_utils import NodeSpec, get, save_raw_ndjson, transient_retry

# --- GitHub (Cloudflare-free) -------------------------------------------------
GH_REPO = "bennettoxford/openprescribing"
GH_TREE = f"https://api.github.com/repos/{GH_REPO}/git/trees/main?recursive=1"
GH_RAW = f"https://raw.githubusercontent.com/{GH_REPO}/main/"
DEF_PREFIX = "openprescribing/measures/definitions/"

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
@transient_retry()
def _get_json(url, headers=None):
    r = get(url, timeout=(10.0, 120.0), headers=headers)
    r.raise_for_status()
    return r.json()


@transient_retry()
def _get_text(url, headers=None):
    r = get(url, timeout=(10.0, 180.0), headers=headers)
    r.raise_for_status()
    return r.text


def _measure_def_paths():
    """All measure-definition file paths in the source repo (Cloudflare-free)."""
    tree = _get_json(GH_TREE)
    return [
        t["path"]
        for t in tree.get("tree", [])
        if t["path"].startswith(DEF_PREFIX) and t["path"].endswith(".json")
    ]


def _load_definitions():
    """slug -> parsed measure definition dict, from the repo."""
    out = {}
    for path in _measure_def_paths():
        slug = path.rsplit("/", 1)[-1][: -len(".json")]
        out[slug] = json.loads(_get_text(GH_RAW + path))
    return out


def _plain(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        value = " ".join(str(v) for v in value)
    text = str(value)
    # crude tag strip — definitions occasionally embed simple HTML
    out, depth = [], 0
    for ch in text:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return " ".join("".join(out).split()) or None


def _bnf_level(length):
    return {
        2: "chapter",
        4: "section",
        6: "paragraph",
        7: "subparagraph",
        9: "chemical",
        11: "product",
        15: "presentation",
    }.get(length, "other")


# ----------------------------------------------------------------------------
# fetch fns — GitHub-sourced (reliable)
# ----------------------------------------------------------------------------
def fetch_measures(node_id: str) -> None:
    """Reference catalog of standardised measures, from the repo definitions."""
    defs = _load_definitions()
    rows = []
    for slug, d in sorted(defs.items()):
        rows.append(
            {
                "measure_id": slug,
                "name": _plain(d.get("name")),
                "title": _plain(d.get("title")),
                "description": _plain(d.get("description")),
                "why_it_matters": _plain(d.get("why_it_matters")),
                "tags": ",".join(d.get("tags") or []) or None,
                "numerator_short": _plain(d.get("numerator_short")),
                "denominator_short": _plain(d.get("denominator_short")),
                "is_percentage": d.get("is_percentage"),
                "is_cost_based": d.get("is_cost_based"),
                "low_is_good": d.get("low_is_good"),
                "numerator_type": d.get("numerator_type"),
                "denominator_type": d.get("denominator_type"),
                "measure_type": d.get("measure_type"),
                "measure_complexity": d.get("measure_complexity"),
                "date_reviewed": (
                    str(d["date_reviewed"]) if d.get("date_reviewed") else None
                ),
            }
        )
    save_raw_ndjson(rows, node_id)


def fetch_bnf_codes(node_id: str) -> None:
    """BNF code reference, parsed from the numerator/denominator BNF-code filters
    declared in the repo measure definitions (Cloudflare-free)."""
    defs = _load_definitions()
    seen = {}
    for d in defs.values():
        for key in ("numerator_bnf_codes_filter", "denominator_bnf_codes_filter"):
            for entry in d.get(key) or []:
                code, _, comment = str(entry).partition("#")
                code = code.strip()
                if not code:
                    continue
                name = comment.strip() or None
                if code not in seen or (name and not seen[code]):
                    seen[code] = name
    rows = [
        {
            "bnf_code": code,
            "name": name,
            "code_length": len(code),
            "level": _bnf_level(len(code)),
        }
        for code, name in sorted(seen.items())
    ]
    save_raw_ndjson(rows, node_id)


# ----------------------------------------------------------------------------
# DAG
# ----------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id="openprescribing-measures", fn=fetch_measures, kind="download"),
    NodeSpec(id="openprescribing-bnf-codes", fn=fetch_bnf_codes, kind="download"),
]
