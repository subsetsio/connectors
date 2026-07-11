-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_attendence",
    "regions",
    "value"
FROM "geostat-population-20census-202014-disability-49-4-population-under-18-with-health-related-limitations-by-school-attendence"
