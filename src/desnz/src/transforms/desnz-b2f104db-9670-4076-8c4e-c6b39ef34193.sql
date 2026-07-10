-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Departmental spending rows come from monthly transparency files and may repeat suppliers or descriptions; keep period and resource context when counting transactions.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-b2f104db-9670-4076-8c4e-c6b39ef34193"
