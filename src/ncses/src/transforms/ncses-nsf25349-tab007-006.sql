-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State or location" AS state_or_location,
    "Rank" AS rank,
    "Totala" AS totala,
    "Male" AS male,
    "Female" AS female,
    "Science and engineering - Total" AS science_and_engineering_total,
    "Science and engineering - Male" AS science_and_engineering_male,
    "Science and engineering - Female" AS science_and_engineering_female,
    "Non-science and engineering - Total" AS non_science_and_engineering_total,
    "Non-science and engineering - Male" AS non_science_and_engineering_male,
    "Non-science and engineering - Female" AS non_science_and_engineering_female
FROM "ncses-nsf25349-tab007-006"
