-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "monthyear",
    strptime("randomly_generated_audit_date", '%m/%d/%Y')::DATE AS randomly_generated_audit_date,
    strptime("alternate_randomly_generated_audit_date", '%m/%d/%Y')::DATE AS alternate_randomly_generated_audit_date
FROM "nyc-open-data-8hgr-brxd"
