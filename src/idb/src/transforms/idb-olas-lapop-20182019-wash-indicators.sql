-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "iso3",
    CAST("count_respondents" AS BIGINT) AS count_respondents,
    "scope",
    "gender",
    "quintile",
    "indicator",
    CAST("value" AS DOUBLE) AS value,
    "source_resource"
FROM "idb-olas-lapop-20182019-wash-indicators"
