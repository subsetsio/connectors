-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Variable codes are scoped by the File column; join on both the module/file context and the variable code where available.
SELECT
    "File" AS file,
    "Sort_Cat" AS sort_cat,
    "Category" AS category,
    "Sort_ID" AS sort_id,
    "Variable" AS variable,
    "Tool" AS tool,
    "Excel" AS excel
FROM "eu-klems-variable-dictionary"
