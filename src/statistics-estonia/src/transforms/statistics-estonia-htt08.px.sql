-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "size_class_of_enterprise",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-htt08.px"
