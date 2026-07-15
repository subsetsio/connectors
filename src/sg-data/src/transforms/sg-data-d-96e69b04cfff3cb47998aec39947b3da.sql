-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "region",
    "no_of_visitor_arrivals"
FROM "sg-data-d-96e69b04cfff3cb47998aec39947b3da"
