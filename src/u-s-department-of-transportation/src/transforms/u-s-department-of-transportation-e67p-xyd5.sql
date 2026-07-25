-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The current raw snapshot is empty; consumers should treat this table as an upstream placeholder until a non-empty source update lands.
SELECT
    "docket_number",
    "usdot_number",
    "op_auth_type",
    "order1_serve_date",
    "order1_type_desc",
    "order1_effective_date"
FROM "u-s-department-of-transportation-e67p-xyd5"
