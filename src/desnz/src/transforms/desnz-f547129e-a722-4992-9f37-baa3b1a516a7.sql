-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Registered heat-network rows are notification records under metering and billing regulations; avoid treating them as deployment counts without filtering status and resource context.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-f547129e-a722-4992-9f37-baa3b1a516a7"
