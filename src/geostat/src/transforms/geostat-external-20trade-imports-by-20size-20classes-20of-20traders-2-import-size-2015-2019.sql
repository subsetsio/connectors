-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "months",
    CAST("years" AS BIGINT) AS years,
    "size_classes",
    "value"
FROM "geostat-external-20trade-imports-by-20size-20classes-20of-20traders-2-import-size-2015-2019"
