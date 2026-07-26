-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "facility_name",
    "location_type",
    "_operator" AS operator,
    "status",
    "open",
    "hours_of_operation",
    "accessibility",
    "restroom_type",
    "changing_stations",
    "additional_notes",
    "website",
    "latitude",
    "longitude",
    "_location" AS location
FROM "nyc-open-data-i7jb-7jku"
