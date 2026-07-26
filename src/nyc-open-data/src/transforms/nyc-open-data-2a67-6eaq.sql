-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "admin_district",
    "_2021_complaints_septjan" AS 2021_complaints_septjan,
    "_2021_material_incidents_septjan" AS 2021_material_incidents_septjan,
    "race",
    "ethnicity_or_national_origin_or_both",
    "religion",
    "gender",
    "weight",
    "gender_identityexpression",
    "disability",
    "sexual_orientation"
FROM "nyc-open-data-2a67-6eaq"
