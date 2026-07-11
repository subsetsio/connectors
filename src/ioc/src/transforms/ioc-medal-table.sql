-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix all-sports totals with sport-level rows and all-gender totals with gender-specific rows; filter sport and gender before summing medal counts.
SELECT
    "edition",
    "games",
    "noc_code",
    "noc_name",
    "sport",
    "gender",
    "gold",
    "silver",
    "bronze",
    "total",
    "rank",
    "rank_total"
FROM "ioc-medal-table"
