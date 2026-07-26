-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "opt_code",
    "site_name",
    "school_name",
    "number_of_riders"
FROM "nyc-open-data-kjgh-ywbx"
