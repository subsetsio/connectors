-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "jobcountry",
    CAST("AI_share_postings" AS DOUBLE) AS ai_share_postings
FROM "indeed-hiring-lab-ai-posting"
