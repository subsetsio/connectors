-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "annual_leave_entitlement",
    "distribution"
FROM "sg-data-d-6dd79ec2994f118e796c2acd15d3c90f"
