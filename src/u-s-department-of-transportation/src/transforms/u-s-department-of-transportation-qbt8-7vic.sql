-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "change_date",
    CAST("inspection_id" AS BIGINT) AS inspection_id,
    CAST("vioseqnum" AS BIGINT) AS vioseqnum,
    CAST("adjseq" AS BIGINT) AS adjseq,
    CAST("citation_code" AS BIGINT) AS citation_code,
    "citation_result"
FROM "u-s-department-of-transportation-qbt8-7vic"
