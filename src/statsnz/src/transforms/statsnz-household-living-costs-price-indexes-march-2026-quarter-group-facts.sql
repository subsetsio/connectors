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
    CAST("tot_hhs" AS BIGINT) AS tot_hhs,
    CAST("own" AS BIGINT) AS own,
    CAST("own_wm" AS BIGINT) AS own_wm,
    CAST("own_prop" AS DOUBLE) AS own_prop,
    CAST("own_wm_prop" AS DOUBLE) AS own_wm_prop,
    CAST("prop_hhs" AS DOUBLE) AS prop_hhs,
    CAST("age" AS DOUBLE) AS age,
    CAST("size" AS DOUBLE) AS size,
    CAST("income" AS BIGINT) AS income,
    CAST("expenditure" AS BIGINT) AS expenditure,
    CAST("eqv_income" AS BIGINT) AS eqv_income,
    CAST("eqv_exp" AS BIGINT) AS eqv_exp
FROM "statsnz-household-living-costs-price-indexes-march-2026-quarter-group-facts"
