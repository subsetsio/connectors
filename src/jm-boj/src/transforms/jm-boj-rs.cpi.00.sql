-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `series` values are CPI commodity groups for Greater Kingston and Metro Area; distinguish groups from all-items totals before aggregating.
SELECT
    "date",
    "subtable",
    "series",
    "value",
    "frequency",
    "unit"
FROM "jm-boj-rs.cpi.00"
