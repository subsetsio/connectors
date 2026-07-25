-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "unique_carrier",
    CAST("total" AS BIGINT) AS total,
    CAST("atlantic" AS BIGINT) AS atlantic,
    CAST("domestic" AS BIGINT) AS domestic,
    CAST("international" AS BIGINT) AS international,
    CAST("latin_america" AS BIGINT) AS latin_america,
    CAST("pacific" AS BIGINT) AS pacific,
    CAST("system" AS BIGINT) AS system,
    "carrier_name"
FROM "u-s-department-of-transportation-9tn7-rkk2"
