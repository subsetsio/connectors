-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "5 Stars" AS "5_stars",
    "4 Stars" AS "4_stars",
    "3 Stars" AS "3_stars",
    "2 Stars" AS "2_stars",
    "1 Star" AS "1_star"
FROM "cms-hicp-9999"
