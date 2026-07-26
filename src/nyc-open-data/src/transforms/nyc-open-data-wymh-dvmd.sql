-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "metric",
    "totalnoofcalls",
    "avgspeedofanswer",
    "callpctansweredwi30secs",
    "_month" AS month,
    "_year" AS year
FROM "nyc-open-data-wymh-dvmd"
