-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "state",
    "agency",
    "division",
    "combo",
    "address",
    "city",
    "state_1",
    "zip_code",
    "phone",
    "fax",
    "email",
    "business_hours",
    "website",
    "oa",
    "point_of_contact",
    "geo_ref1",
    "office"
FROM "u-s-department-of-transportation-buxa-ujat"
