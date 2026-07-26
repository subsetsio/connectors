-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "report_date",
    "placements",
    "los"
FROM "nyc-open-data-5284-7vfz"
