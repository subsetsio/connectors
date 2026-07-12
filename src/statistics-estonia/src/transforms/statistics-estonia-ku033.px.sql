-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "language_of_instruction_at_school",
    "type_of_school",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-ku033.px"
