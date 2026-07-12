-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attainment_of_woman",
    "labour_status_of_woman",
    "age_group_of_woman",
    "county",
    "indicator",
    "value"
FROM "statistics-estonia-rl0416.px"
