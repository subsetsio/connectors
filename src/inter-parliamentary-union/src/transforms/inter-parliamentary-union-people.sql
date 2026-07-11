-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source can emit duplicate person_code rows, especially placeholder records; de-duplicate by the needed person attributes before counting people.
SELECT
    "person_code",
    "title_salutation",
    "first_name",
    "family_name",
    "gender",
    "dob_year",
    "dob_month",
    "dob_day",
    "person_country"
FROM "inter-parliamentary-union-people"
