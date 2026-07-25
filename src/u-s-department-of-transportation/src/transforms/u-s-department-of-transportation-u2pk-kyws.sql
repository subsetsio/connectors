-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("personal" AS BIGINT) AS personal,
    CAST("instructional" AS BIGINT) AS instructional,
    CAST("other" AS BIGINT) AS other,
    CAST("air_taxi" AS BIGINT) AS air_taxi,
    CAST("business" AS BIGINT) AS business,
    CAST("total" AS BIGINT) AS total
FROM "u-s-department-of-transportation-u2pk-kyws"
