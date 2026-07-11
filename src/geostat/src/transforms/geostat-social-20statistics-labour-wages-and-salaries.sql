-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarters",
    CAST("years" AS BIGINT) AS years,
    "economic_activity",
    "sex_sectors",
    "value"
FROM "geostat-social-20statistics-labour-wages-and-salaries"
