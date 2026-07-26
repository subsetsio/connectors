-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "weekdate",
    "num_peop_test",
    "num_peop_pos",
    "percent_positive",
    "incomplete"
FROM "nyc-open-data-cqhz-kkvd"
