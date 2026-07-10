-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "digits",
    CAST("section" AS BIGINT) AS section,
    "desc_en",
    "desc_bm"
FROM "dosm-sitc"
