-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institute" AS institute,
    "Keywords" AS keywords,
    "Project" AS project,
    "Geographic Reach" AS geographic_reach,
    "Funding Amount" AS funding_amount,
    "3 year savings" AS "3_year_savings",
    "Summary" AS summary,
    "Category" AS category,
    "Stage" AS stage,
    "Model" AS model,
    "url",
    CAST("Unique ID" AS BIGINT) AS unique_id
FROM "cms-424de599-7a34-4243-af70-95d24dd675dd"
