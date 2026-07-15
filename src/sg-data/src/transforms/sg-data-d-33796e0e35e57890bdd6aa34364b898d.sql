-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "total_international_visitor_arrivals"
FROM "sg-data-d-33796e0e35e57890bdd6aa34364b898d"
