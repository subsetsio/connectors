-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "project_id",
    "title",
    "notice_type",
    "notice_url",
    "closing_date",
    "procurement_method",
    "notice_date",
    "agency",
    "sector_name",
    CAST("bid_estimate" AS DOUBLE) AS bid_estimate,
    "bid_currency",
    CAST("bid_estimate_gbp" AS DOUBLE) AS bid_estimate_gbp,
    "description",
    "status",
    "source"
FROM "dbt-ukraine-combined-contract-opportunites--ukraine-combined-contract-opportunities-pdg"
