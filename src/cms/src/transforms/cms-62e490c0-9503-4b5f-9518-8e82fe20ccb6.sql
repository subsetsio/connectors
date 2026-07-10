-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("MSA" AS BIGINT) AS msa,
    "MSA Title" AS msa_title,
    "Counties" AS counties
FROM "cms-62e490c0-9503-4b5f-9518-8e82fe20ccb6"
