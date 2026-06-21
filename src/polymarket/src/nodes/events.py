"""Polymarket events — Gamma /events/keyset, one row per event."""
import json

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer

from utils import _date, _f, _i, _keyset_pages


def _event_row(e: dict) -> dict:
    markets = e.get("markets") or []
    return {
        "event_id": e.get("id"),
        "ticker": e.get("ticker"),
        "slug": e.get("slug"),
        "title": e.get("title"),
        "category": e.get("category"),
        "description": e.get("description"),
        "volume_usd": _f(e.get("volume")),
        "volume_24h_usd": _f(e.get("volume24hr")),
        "volume_1wk_usd": _f(e.get("volume1wk")),
        "volume_1mo_usd": _f(e.get("volume1mo")),
        "volume_1yr_usd": _f(e.get("volume1yr")),
        "liquidity_usd": _f(e.get("liquidity")),
        "open_interest": _f(e.get("openInterest")),
        "comment_count": _i(e.get("commentCount")),
        "competitive": _f(e.get("competitive")),
        "neg_risk": bool(e.get("enableNegRisk") or e.get("negRisk") or e.get("negRiskAugmented")),
        "is_active": bool(e.get("active")),
        "is_closed": bool(e.get("closed")),
        "is_archived": bool(e.get("archived")),
        "is_featured": bool(e.get("featured")),
        "is_restricted": bool(e.get("restricted")),
        "market_count": len(markets),
        "start_date": _date(e.get("startDate")),
        "end_date": _date(e.get("endDate")),
        "creation_date": _date(e.get("creationDate")),
        "created_at": e.get("createdAt"),
        "updated_at": e.get("updatedAt"),
    }


def fetch_events(node_id: str) -> None:
    asset = node_id  # "polymarket-events"
    total = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        for rows in _keyset_pages("events"):
            for e in rows:
                if not e.get("id"):
                    continue
                f.write(json.dumps(_event_row(e)) + "\n")
                total += 1
            print(f"    events: {total:,} written")
    print(f"  events: wrote {total:,} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="polymarket-events", fn=fetch_events, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="polymarket-events-transform",
        deps=["polymarket-events"],
        sql='''
            SELECT * EXCLUDE (_rn) FROM (
                SELECT
                    CAST(event_id AS VARCHAR)       AS event_id,
                    CAST(ticker AS VARCHAR)         AS ticker,
                    CAST(slug AS VARCHAR)           AS slug,
                    CAST(title AS VARCHAR)          AS title,
                    CAST(category AS VARCHAR)       AS category,
                    CAST(description AS VARCHAR)    AS description,
                    CAST(volume_usd AS DOUBLE)      AS volume_usd,
                    CAST(volume_24h_usd AS DOUBLE)  AS volume_24h_usd,
                    CAST(volume_1wk_usd AS DOUBLE)  AS volume_1wk_usd,
                    CAST(volume_1mo_usd AS DOUBLE)  AS volume_1mo_usd,
                    CAST(volume_1yr_usd AS DOUBLE)  AS volume_1yr_usd,
                    CAST(liquidity_usd AS DOUBLE)   AS liquidity_usd,
                    CAST(open_interest AS DOUBLE)   AS open_interest,
                    CAST(comment_count AS BIGINT)   AS comment_count,
                    CAST(competitive AS DOUBLE)     AS competitive,
                    CAST(neg_risk AS BOOLEAN)       AS neg_risk,
                    CAST(is_active AS BOOLEAN)      AS is_active,
                    CAST(is_closed AS BOOLEAN)      AS is_closed,
                    CAST(is_archived AS BOOLEAN)    AS is_archived,
                    CAST(is_featured AS BOOLEAN)    AS is_featured,
                    CAST(is_restricted AS BOOLEAN)  AS is_restricted,
                    CAST(market_count AS BIGINT)    AS market_count,
                    TRY_CAST(start_date AS DATE)    AS start_date,
                    TRY_CAST(end_date AS DATE)      AS end_date,
                    TRY_CAST(creation_date AS DATE) AS creation_date,
                    TRY_CAST(created_at AS TIMESTAMP) AS created_at,
                    TRY_CAST(updated_at AS TIMESTAMP) AS updated_at,
                    row_number() OVER (
                        PARTITION BY event_id ORDER BY updated_at DESC NULLS LAST
                    ) AS _rn
                FROM "polymarket-events"
                WHERE event_id IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
