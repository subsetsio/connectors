-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "administrative_geography",
    "geography",
    "sic_unofficial",
    "unofficialstandardindustrialclassification",
    "enterprises_and_local_units",
    "enterprisesandlocalunits"
FROM "ons-uk-business-by-enterprises-and-local-units"
