-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Member" AS member,
    "Party" AS party,
    "District" AS district,
    "Congress" AS congress,
    "Resignation Date" AS resignation_date,
    "Reason" AS reason,
    "Source" AS source,
    "Category" AS category
FROM "fivethirtyeight-congress-resignations-congressional-resignations"
