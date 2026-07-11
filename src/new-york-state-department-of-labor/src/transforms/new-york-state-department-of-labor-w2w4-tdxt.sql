-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "new_york_state_agency_occupation_title",
    "agency",
    "division",
    "street_address",
    "city",
    "state",
    CAST("zip" AS BIGINT) AS zip,
    CAST("telephone" AS BIGINT) AS telephone,
    "url",
    "occupation_code",
    "occupation_title",
    "georeference"
FROM "new-york-state-department-of-labor-w2w4-tdxt"
