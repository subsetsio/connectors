-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_generations_in_household",
    "indicator",
    "age_and_number_of_children",
    "leibkonna_suurus",
    "county",
    "value"
FROM "statistics-estonia-rl0726.px"
