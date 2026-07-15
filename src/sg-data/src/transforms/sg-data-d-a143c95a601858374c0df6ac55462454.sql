-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "annual_leave_entitlement",
    "distribution"
FROM "sg-data-d-a143c95a601858374c0df6ac55462454"
