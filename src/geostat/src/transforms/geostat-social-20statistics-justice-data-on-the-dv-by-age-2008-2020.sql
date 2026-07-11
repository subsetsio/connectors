-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "victims_and_perpetrators",
    CAST("years" AS BIGINT) AS years,
    "age_groups",
    "regions",
    "value"
FROM "geostat-social-20statistics-justice-data-on-the-dv-by-age-2008-2020"
