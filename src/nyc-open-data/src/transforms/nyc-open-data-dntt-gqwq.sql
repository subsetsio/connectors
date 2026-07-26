-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inspection_id",
    "no_violation_found",
    "city_do_it",
    "owner_will_do_it",
    "capital_project_conflict_flag",
    "capital_project_conflicts",
    "cancel",
    "inspection_date",
    "is_311_inspection",
    "material_id",
    "pickup_sidewalk",
    "curb311",
    "pickup_curb",
    "other",
    "correspondence",
    "damage_id",
    "damage_type_code"
FROM "nyc-open-data-dntt-gqwq"
