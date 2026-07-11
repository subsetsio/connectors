-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `series` values identify parish-level remittance inflows; distinguish parish rows from any total row before aggregating.
SELECT
    "date",
    "subtable",
    "series",
    "value",
    "frequency",
    "unit"
FROM "jm-boj-es.rmt.03"
