-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "liquid",
    "car",
    CAST("count" AS BIGINT) AS count,
    CAST("year" AS BIGINT) AS year
FROM "u-s-department-of-transportation-gbe2-48iq"
