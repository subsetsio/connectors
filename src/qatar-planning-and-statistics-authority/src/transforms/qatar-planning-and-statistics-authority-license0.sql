-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_type",
    "motorcycle_permit",
    "car_permit",
    "medtruck_permit",
    "trailer_permit",
    "first_issuedate",
    "hearing_flag",
    "organ_flag",
    "issue_department",
    "gender",
    "nationality_group",
    "birthyear",
    "total"
FROM "qatar-planning-and-statistics-authority-license0"
