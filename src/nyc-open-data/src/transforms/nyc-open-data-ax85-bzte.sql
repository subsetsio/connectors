-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "number_of_tb_cases",
    "rate_per_100000",
    "culturepositive_cases",
    "sputum_smearpositive_cases",
    "sputum_smearpositive_rate_per_100000",
    "multidrugresistance_cases"
FROM "nyc-open-data-ax85-bzte"
