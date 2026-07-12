-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_live_born_children",
    "place_of_residence_of_woman",
    "educational_level_of_woman",
    "age_group_of_woman",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv096.px"
