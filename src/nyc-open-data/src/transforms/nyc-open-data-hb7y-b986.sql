-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "indicator_name",
    "indicator_number",
    "grouping_1",
    "grouping_2",
    "grouping_3",
    "grouping_4",
    "grouping_5",
    "grouping_6",
    "number_of_cases"
FROM "nyc-open-data-hb7y-b986"
