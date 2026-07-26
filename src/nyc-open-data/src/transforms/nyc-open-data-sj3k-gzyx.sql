-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "ili_pne_admit",
    "baseline",
    "percent_change",
    "status",
    "etldate"
FROM "nyc-open-data-sj3k-gzyx"
