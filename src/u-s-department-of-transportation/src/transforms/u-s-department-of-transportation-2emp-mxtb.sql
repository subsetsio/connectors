-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    "dot_number",
    "co_name",
    "attn_to_or_title",
    "street_po",
    "city",
    "state_code",
    "ctry_code",
    "zip_code"
FROM "u-s-department-of-transportation-2emp-mxtb"
