-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "year",
    "interaction",
    "value"
FROM "geostat-gender-20statistics-ict-7-interaction-with-public-authorities-or-public-services-over-the-intern"
