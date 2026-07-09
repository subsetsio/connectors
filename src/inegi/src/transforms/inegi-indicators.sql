-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One indicator id appears on several rows: description is the indicator's geographic-disaggregation label (e.g. 'Total nacional'), not the concept name, so code alone is not unique. The concept grouping lives in the topic each series carries in inegi-values.
SELECT
    CAST("code" AS BIGINT) AS code,
    "description"
FROM "inegi-indicators"
