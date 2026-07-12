-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "plate_type",
    "vehicle_manufacture",
    "vehicle_status",
    "owner_type",
    "model_year",
    "handicap_flag",
    "vehicle_flag",
    "gender",
    "nationality_group",
    "birth_year",
    "total"
FROM "qatar-planning-and-statistics-authority-vehicle"
