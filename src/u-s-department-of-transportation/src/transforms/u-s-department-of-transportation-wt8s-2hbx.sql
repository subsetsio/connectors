-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "change_date",
    CAST("inspection_id" AS BIGINT) AS inspection_id,
    CAST("insp_unit_id" AS BIGINT) AS insp_unit_id,
    CAST("insp_unit_type_id" AS BIGINT) AS insp_unit_type_id,
    CAST("insp_unit_number" AS BIGINT) AS insp_unit_number,
    "insp_unit_make",
    "insp_unit_company",
    "insp_unit_license",
    "insp_unit_license_state",
    "insp_unit_vehicle_id_number",
    "insp_unit_decal",
    "insp_unit_decal_number"
FROM "u-s-department-of-transportation-wt8s-2hbx"
