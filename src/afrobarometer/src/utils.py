"""Shared helpers for the Afrobarometer connector.

All access goes through the public Online Data Analysis (ODA) JSON web service
(collection 7) at afrobarometer-online-analysis.com/odav2. See the research
handoff for the protocol. Both download nodes (`questions`, `values`) build the
same catalog from a union of the 10 survey-round indices, so that logic lives
here.
"""

import json
import re

from subsets_utils import get, post, transient_retry

WS = "https://afrobarometer-online-analysis.com/odav2/ws/oda/"
CONFIG_URL = "https://afrobarometer-online-analysis.com/odav2/oda.jsp?config=7"
COLLECTION = "7"
COUNTRY_CROSS = -999999          # ODA sentinel: break a question down by country
HTTP_TIMEOUT = (10.0, 120.0)     # (connect, read)


@transient_retry()
def fetch_config() -> dict:
    """Parse the JS `config:{...}` object embedded in the ODA bootstrap page.

    Carries the survey rounds (internal ids + labels) and the 'regions'
    (countries with a #-delimited bitmask of the rounds they appear in).
    """
    resp = get(CONFIG_URL, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    html = resp.text
    i = html.find("config:")
    if i < 0:
        raise RuntimeError("ODA config object not found on bootstrap page")
    start = html.find("{", i)
    depth = 0
    end = None
    for j in range(start, len(html)):
        c = html[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    if end is None:
        raise RuntimeError("could not balance ODA config object braces")
    return json.loads(html[start:end])


@transient_retry()
def open_session() -> int:
    """Open an ODA stats session; the returned sid authorizes every later call
    via the `odaSession` header."""
    resp = post(WS + "stats/session/" + COLLECTION, json={}, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    sid = data.get("sid")
    if not sid:
        raise RuntimeError("ODA session response carried no sid: %r" % data)
    return sid


@transient_retry()
def fetch_index(sid: int, round_id: int, amids: str) -> dict:
    """Question catalog for one round. `amids` is a comma-joined list of region
    `valor`s present in the round."""
    resp = post(
        WS + "index/%s/%s/1" % (COLLECTION, round_id),
        data="amids=%s" % amids,
        headers={
            "odaSession": str(sid),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def fetch_question_timeseries(sid: int, qid: int, round_id: int, saids: str) -> dict:
    """One question, broken down by country (tables) x round (columns).

    timeseries=True with roundEquiv=0 makes the columns the survey rounds and
    cross1=COUNTRY_CROSS makes each result table a country, so a single call
    yields the full country x round matrix for the question.
    """
    body = {
        "cuid": round_id,
        "amids": "",
        "saids": saids,
        "idioma": 1,
        "roundEquiv": 0,
        "cross1": COUNTRY_CROSS,
        "cross2": 0,
        "showEmpty": True,
        "timeseries": True,
        "maps": False,
        "mapa": 0,
        "trad": -1,
    }
    resp = post(
        WS + "question/%s/%s" % (COLLECTION, qid),
        json=body,
        headers={"odaSession": str(sid)},
        timeout=HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


_ROUND_NUM = re.compile(r"R(\d+)")
_COUNTRY_PAREN = re.compile(r"\s*\(.*\)\s*$")


def round_num(label: str):
    """'R10 2024/2025' -> 10."""
    m = _ROUND_NUM.search(label or "")
    return int(m.group(1)) if m else None


def build_catalog(sid: int) -> dict:
    """Walk the 10 round indices once and assemble the connector's catalog.

    Returns:
      rounds        : list of internal round ids in R1..R10 order
      round_labels  : parallel list of human labels
      variables     : {variable_code -> {qid, round_id, round_idx, title,
                       group, n_rounds, round_nums}}  (representative qid is
                       the latest round the code appears in; the ODA timeseries
                       call linked to it returns every round it spans)
      country_said  : {country_name -> said}  (latest round's sample id per
                       country; one said suffices because the ODA maps a sample
                       across rounds)
    """
    config = fetch_config()
    rounds = config["rounds"]
    round_labels = config["titrounds"]
    regions = config["regions"]

    variables = {}
    country_said = {}
    for ridx, rid in enumerate(rounds):
        valors = [
            str(r["valor"])
            for r in regions
            if ("#%s#" % rid) in (r.get("rounds") or "")
        ]
        amids = ",".join(valors) if valors else str(regions[0]["valor"])
        idx = fetch_index(sid, rid, amids)

        for s in idx.get("samples", {}).get("rows", []):
            data = s.get("data") or []
            label = (data[1] if len(data) > 1 else "") or ""
            country = _COUNTRY_PAREN.sub("", label).strip()
            if country and country != "(N)":
                country_said[country] = s["id"]   # latest round wins

        for it in idx.get("lista", []):
            if it.get("formato") != "P":
                continue
            vc = it.get("variable")
            if not vc:
                continue
            rec = variables.get(vc)
            if rec is None:
                variables[vc] = {
                    "qid": it["id"],
                    "round_id": rid,
                    "round_idx": ridx,
                    "title": it.get("title") or "",
                    "group": it.get("grupo") or "",
                    "round_nums": {ridx + 1},
                }
            else:
                rec["round_nums"].add(ridx + 1)
                if ridx > rec["round_idx"]:        # keep the latest round's id
                    rec["qid"] = it["id"]
                    rec["round_id"] = rid
                    rec["round_idx"] = ridx
                    rec["title"] = it.get("title") or rec["title"]
                    rec["group"] = it.get("grupo") or rec["group"]

    for rec in variables.values():
        rec["n_rounds"] = len(rec["round_nums"])

    return {
        "rounds": rounds,
        "round_labels": round_labels,
        "variables": variables,
        "country_said": country_said,
    }
