-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Postcode electricity and gas estimates contain very granular geography and multiple fuel/consumption measures; filter fuel and geography before aggregation.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-e7d4c1cf-45a0-4070-878f-24ad9641f655"
