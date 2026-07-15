-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "sick_leave",
    "proportion"
FROM "sg-data-d-b6ca499d5ec2f3c3bc8f735e271d9b11"
