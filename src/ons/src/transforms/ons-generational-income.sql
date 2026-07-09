-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    "yyyy_to_yyyy_yy",
    "time",
    "uk_only",
    "geography",
    CAST("single_year_of_age" AS BIGINT) AS single_year_of_age,
    CAST("age" AS BIGINT) AS age,
    "tax_benefit_type",
    "typeoftaxorbenefit",
    "decade",
    "decade_1"
FROM "ons-generational-income"
