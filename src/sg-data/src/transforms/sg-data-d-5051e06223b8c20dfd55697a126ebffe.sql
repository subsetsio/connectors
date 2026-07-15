-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "sick_leave",
    "proportion"
FROM "sg-data-d-5051e06223b8c20dfd55697a126ebffe"
