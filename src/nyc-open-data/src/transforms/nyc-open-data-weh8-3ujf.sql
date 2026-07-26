-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_system" AS system,
    "parentid",
    "department",
    "description",
    "synturf_location",
    "system_type",
    "turf_type",
    "infill_material",
    "jop",
    "maint_by",
    "maint_by_spec",
    "construction_entity",
    "construction_entity_spec",
    "contract_type",
    "contract_number",
    "commission_date",
    "retired",
    "borough",
    "shape",
    "featurestatus"
FROM "nyc-open-data-weh8-3ujf"
