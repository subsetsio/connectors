-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ljnsy",
    "nationality",
    "lnw",
    "gender",
    "lm_dlt_w_lhlt",
    "rates_and_cases",
    "value"
FROM "qatar-planning-and-statistics-authority-general-marriage-rate-by-nationality-and-gender-per-1000-population-15-year-and-above"
