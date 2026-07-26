-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_and_time_pst",
    "_language" AS language,
    "access_code",
    "duration_seconds"
FROM "nyc-open-data-wapz-jfhq"
