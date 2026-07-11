-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Sector codes are useful lookup values, but this model keeps the table keyless because the model verifier did not scan-verify code as row grain.
SELECT
    "code",
    "name"
FROM "ocha-metadata-sector"
