-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source cube has duplicated dimension combinations in the raw profile, so no row key is declared; treat rows as source observation records rather than a uniquely keyed dimensional cube.
SELECT
    "gender",
    CAST("year" AS BIGINT) AS year,
    "fields_of_science",
    "value"
FROM "geostat-gender-20statistics-education-13-number-of-doctoral-graduates-by-programmes"
