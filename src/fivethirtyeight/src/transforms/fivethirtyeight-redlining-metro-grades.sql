-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "metro_area",
    "holc_grade",
    "white_pop",
    "black_pop",
    "hisp_pop",
    "asian_pop",
    "other_pop",
    "total_pop",
    "pct_white",
    "pct_black",
    "pct_hisp",
    "pct_asian",
    "pct_other",
    "lq_white",
    "lq_black",
    "lq_hisp",
    "lq_asian",
    "lq_other",
    "surr_area_white_pop",
    "surr_area_black_pop",
    "surr_area_hisp_pop",
    "surr_area_asian_pop",
    "surr_area_other_pop",
    "surr_area_pct_white",
    "surr_area_pct_black",
    "surr_area_pct_hisp",
    "surr_area_pct_asian",
    "surr_area_pct_other"
FROM "fivethirtyeight-redlining-metro-grades"
