-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "labor_market_region",
    "street_address",
    "city",
    "state",
    CAST("zip_code" AS BIGINT) AS zip_code,
    "phone",
    "fax",
    "email",
    "url",
    "georeference"
FROM "new-york-state-department-of-labor-u56z-mms2"
