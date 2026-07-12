-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "use_of_virtual_or_other_innovative_solutions",
    CAST("year" AS BIGINT) AS year,
    "group_of_persons",
    "indicator",
    "value"
FROM "statistics-estonia-kut034.px"
