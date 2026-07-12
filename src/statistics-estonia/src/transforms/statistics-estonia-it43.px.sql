-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "seller_s_country_of_location_and_goods_services",
    "group_of_individuals",
    "indicator",
    "value"
FROM "statistics-estonia-it43.px"
