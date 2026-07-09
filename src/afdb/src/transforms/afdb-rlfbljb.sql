-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "country_code",
    "indicator",
    "indicator_code",
    "sex",
    "sex_code",
    "urbanisation",
    "urbanisation_code",
    "education_level",
    "education_level_code",
    "wealth_quintile",
    "wealth_quintile_code",
    "unit",
    "frequency",
    "date",
    "value"
FROM "afdb-rlfbljb"
