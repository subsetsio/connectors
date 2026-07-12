-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_live_born_children",
    "indicator",
    "age_group_of_woman",
    "county",
    "legal_marital_status_of_woman",
    "value"
FROM "statistics-estonia-rl0413.px"
