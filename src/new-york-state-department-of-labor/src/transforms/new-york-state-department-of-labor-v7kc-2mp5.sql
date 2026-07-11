-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "field_office",
    "counties_served",
    "name",
    "street_address",
    "city",
    "state",
    CAST("zip" AS BIGINT) AS zip,
    "phone",
    "email",
    "location_1",
    "georeference"
FROM "new-york-state-department-of-labor-v7kc-2mp5"
