-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "community_school_district",
    "of_teachers_assigned_to_teach_health"
FROM "nyc-open-data-36j9-c8ka"
