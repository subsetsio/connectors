-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "mother_tongue_2",
    "mother_tongue_1",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rl214312.px"
