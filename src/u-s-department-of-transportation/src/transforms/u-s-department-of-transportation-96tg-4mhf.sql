-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    "dot_number",
    "ins_form_code",
    "mod_col_1",
    "policy_no",
    strptime("recv_date", '%m/%d/%Y')::DATE AS recv_date,
    "ins_class_code",
    "mod_col_2",
    CAST("mod_col_3" AS BIGINT) AS mod_col_3,
    CAST("mod_col_4" AS BIGINT) AS mod_col_4,
    strptime("rej_date", '%m/%d/%Y')::DATE AS rej_date,
    "inser_branch",
    "name_company",
    "rej_reasons",
    CAST("min_cov_amount" AS BIGINT) AS min_cov_amount
FROM "u-s-department-of-transportation-96tg-4mhf"
