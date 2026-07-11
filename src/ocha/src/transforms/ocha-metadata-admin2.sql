-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "admin1_ref",
    "code",
    "name",
    "from_cods",
    "reference_period_start",
    "reference_period_end",
    "admin1_code",
    "admin1_name",
    "location_code",
    "location_name",
    "location_ref"
FROM "ocha-metadata-admin2"
