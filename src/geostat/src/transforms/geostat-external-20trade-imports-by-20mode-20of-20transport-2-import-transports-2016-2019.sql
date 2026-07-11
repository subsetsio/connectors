-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarters_and_months",
    CAST("years" AS BIGINT) AS years,
    "mode_of_transport",
    "value"
FROM "geostat-external-20trade-imports-by-20mode-20of-20transport-2-import-transports-2016-2019"
