-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "notice_id",
    "project_id",
    CAST("live_opportunity" AS BIGINT) AS live_opportunity,
    "notice_type",
    "country",
    "agency",
    "title",
    "description",
    "sector_name",
    "procurement_method",
    "bid_currency",
    CAST("bid_estimate" AS DOUBLE) AS bid_estimate,
    CAST("bid_estimate_gbp" AS DOUBLE) AS bid_estimate_gbp,
    "notice_date",
    "closing_date",
    "notice_url"
FROM "dbt-ukraine-world-bank--ukraine-world-bank-pdg"
