-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reason_for_damage",
    CAST("year" AS BIGINT) AS year,
    "county",
    "value"
FROM "statistics-estonia-kk514.px"
