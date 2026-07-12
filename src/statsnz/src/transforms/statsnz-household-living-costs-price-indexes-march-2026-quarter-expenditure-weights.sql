-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "hlpi_name",
    CAST("year" AS BIGINT) AS year,
    "hlpi",
    "nzhec",
    "nzhec_name",
    "nzhec_short",
    "level",
    CAST("nzhec1" AS BIGINT) AS nzhec1,
    "nzhec1_name",
    "nzhec1_short",
    CAST("weight" AS DOUBLE) AS weight,
    "exp_pw",
    "eqv_exp_pw"
FROM "statsnz-household-living-costs-price-indexes-march-2026-quarter-expenditure-weights"
