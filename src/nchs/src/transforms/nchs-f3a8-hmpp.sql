-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "measure_id",
    "measure_statement_full",
    "measures_statement_short",
    "category",
    "population",
    "year",
    "estimate",
    "se",
    "unit",
    "flag"
FROM "nchs-f3a8-hmpp"
