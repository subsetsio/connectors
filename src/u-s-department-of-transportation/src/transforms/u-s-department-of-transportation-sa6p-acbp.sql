-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    "dot_number",
    "type_license",
    strptime("order1_serve_date", '%m/%d/%Y')::DATE AS order1_serve_date,
    "order2_type_desc",
    strptime("order2_effective_date", '%m/%d/%Y')::DATE AS order2_effective_date
FROM "u-s-department-of-transportation-sa6p-acbp"
