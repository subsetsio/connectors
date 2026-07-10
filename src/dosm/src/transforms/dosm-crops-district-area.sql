-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; treat rows as source observations at the published granularity.
SELECT
    "date",
    "state",
    "district",
    "crop_type",
    "crop_species",
    "planted_area"
FROM "dosm-crops-district-area"
