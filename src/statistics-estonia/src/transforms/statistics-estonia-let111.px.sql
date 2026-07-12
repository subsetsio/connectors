-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "useful_floor_space_per_household_member",
    "structure_of_household",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-let111.px"
