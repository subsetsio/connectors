-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Footnote" AS BIGINT) AS footnote,
    "Reason for No Score" AS reason_for_no_score
FROM "cms-footnotes"
