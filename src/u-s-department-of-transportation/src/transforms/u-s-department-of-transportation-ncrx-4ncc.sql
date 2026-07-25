-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rid",
    CAST("statecode" AS BIGINT) AS statecode,
    "stationid",
    "helmet",
    "age",
    CAST("type" AS BIGINT) AS type,
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("madt" AS BIGINT) AS madt,
    CAST("updatedon" AS TIMESTAMP) AS updatedon
FROM "u-s-department-of-transportation-ncrx-4ncc"
