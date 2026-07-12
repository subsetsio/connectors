-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    CAST("reference_period" AS BIGINT) AS reference_period,
    "agricultural_land_field_crop",
    "county_and_agricultural_unit",
    "value"
FROM "statistics-estonia-pm0281.px"
