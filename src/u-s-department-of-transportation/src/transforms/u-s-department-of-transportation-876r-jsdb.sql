-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "change_date",
    CAST("inspection_id" AS BIGINT) AS inspection_id,
    CAST("insp_violation_id" AS BIGINT) AS insp_violation_id,
    CAST("seq_no" AS BIGINT) AS seq_no,
    CAST("part_no" AS BIGINT) AS part_no,
    "part_no_section",
    "insp_viol_unit",
    CAST("insp_unit_id" AS BIGINT) AS insp_unit_id,
    CAST("insp_violation_category_id" AS BIGINT) AS insp_violation_category_id,
    "out_of_service_indicator",
    CAST("defect_verification_id" AS BIGINT) AS defect_verification_id,
    "citation_number",
    "viol_code",
    "viol_desc"
FROM "u-s-department-of-transportation-876r-jsdb"
