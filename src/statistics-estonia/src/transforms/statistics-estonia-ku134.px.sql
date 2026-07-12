-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "origin_of_broadcast",
    "television_channel",
    "value"
FROM "statistics-estonia-ku134.px"
