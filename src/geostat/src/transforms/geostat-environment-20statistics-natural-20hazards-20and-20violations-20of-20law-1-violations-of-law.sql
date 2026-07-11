-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "violation_types",
    CAST("year" AS BIGINT) AS year,
    "regions",
    "value"
FROM "geostat-environment-20statistics-natural-20hazards-20and-20violations-20of-20law-1-violations-of-law"
