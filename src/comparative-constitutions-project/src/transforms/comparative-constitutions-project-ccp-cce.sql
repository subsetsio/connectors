-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are constitutional chronology events, not one row per constitution or one row per country-year; aggregate only after choosing the event types relevant to the analysis.
SELECT
    CAST("cowcode" AS BIGINT) AS cowcode,
    "country",
    CAST("year" AS BIGINT) AS year,
    CAST("systid" AS BIGINT) AS systid,
    CAST("evntid" AS BIGINT) AS evntid,
    "evnttype"
FROM "comparative-constitutions-project-ccp-cce"
