-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Pre_Primary" AS pre_primary,
    "Primary" AS primary,
    "Secondary" AS secondary,
    "UpperSecondary" AS uppersecondary,
    "Polytechnic" AS polytechnic,
    "University" AS university
FROM "sg-data-d-77fe63cfafc6903c271ab0cbc6ee205e"
