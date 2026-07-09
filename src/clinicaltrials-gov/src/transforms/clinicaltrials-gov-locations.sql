-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long table of study-site rows; a single study can have many locations, and location fields are site descriptors rather than normalized geography.
SELECT
    "nct_id",
    "facility",
    "city",
    "state",
    "zip",
    "country",
    "location_status"
FROM "clinicaltrials-gov-locations"
