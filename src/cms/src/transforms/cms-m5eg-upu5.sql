-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "ZIP Code" AS zip_code
FROM "cms-m5eg-upu5"
