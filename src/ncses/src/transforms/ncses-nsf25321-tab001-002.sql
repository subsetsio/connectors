-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of study" AS field_of_study,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "Employed - Number" AS employed_number,
    "Employed - SE" AS employed_se,
    "Unemployeda - Number" AS unemployeda_number,
    "Unemployeda - SE" AS unemployeda_se,
    "Not in the labor forceb - Number" AS not_in_the_labor_forceb_number,
    "Not in the labor forceb - SE" AS not_in_the_labor_forceb_se
FROM "ncses-nsf25321-tab001-002"
