-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "basin",
    "permits_issued",
    "seasonal_tags",
    "temporary_tags",
    "canoes",
    "kayaks",
    "rowboats",
    "sailboats",
    "sculls"
FROM "nyc-open-data-idfb-y78n"
