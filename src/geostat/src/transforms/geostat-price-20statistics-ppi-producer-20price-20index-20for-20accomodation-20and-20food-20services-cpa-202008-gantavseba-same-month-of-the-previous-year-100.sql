-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    CAST("year" AS BIGINT) AS year,
    "groups",
    "value"
FROM "geostat-price-20statistics-ppi-producer-20price-20index-20for-20accomodation-20and-20food-20services-cpa-202008-gantavseba-same-month-of-the-previous-year-100"
