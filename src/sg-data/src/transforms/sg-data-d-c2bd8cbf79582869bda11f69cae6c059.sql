-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "appln_petition_date",
    "bankruptcy_no"
FROM "sg-data-d-c2bd8cbf79582869bda11f69cae6c059"
