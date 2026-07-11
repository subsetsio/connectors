-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Location codes are useful lookup values, but this model keeps the table keyless because the model verifier did not scan-verify code as row grain.
SELECT
    "id",
    "code",
    "name",
    "has_hrp",
    "in_gho",
    "from_cods",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-metadata-location"
