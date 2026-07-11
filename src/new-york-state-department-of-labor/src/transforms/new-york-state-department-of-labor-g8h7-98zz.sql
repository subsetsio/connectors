-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "county",
    "workforce_information_act_regions",
    "name",
    "street_address",
    "city",
    "state",
    CAST("zip" AS BIGINT) AS zip,
    "phone",
    "fax",
    "email",
    "url",
    "hours",
    "parking",
    "access",
    "directions",
    "location_1",
    "georeference"
FROM "new-york-state-department-of-labor-g8h7-98zz"
