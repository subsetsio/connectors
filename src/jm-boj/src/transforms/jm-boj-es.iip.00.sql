-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `series` values are international-investment-position components; distinguish assets, liabilities, and totals before aggregating.
SELECT
    "date",
    "subtable",
    "series",
    "value",
    "frequency",
    "unit"
FROM "jm-boj-es.iip.00"
