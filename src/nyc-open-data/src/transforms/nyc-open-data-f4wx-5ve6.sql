-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_code",
    "agency_name",
    "ua_code",
    "ua_name",
    "title_code",
    "title_code_name",
    "minmum_salary",
    "maxmum_salary",
    "positions",
    "mean_salary",
    "annual_rate"
FROM "nyc-open-data-f4wx-5ve6"
