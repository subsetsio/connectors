-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows span multiple survey topics and workbook sheets; filter topic and sheet before comparing or aggregating values.
SELECT
    "date",
    "topic",
    "sheet",
    "series",
    "value"
FROM "dallas-fed-agsurvey"
