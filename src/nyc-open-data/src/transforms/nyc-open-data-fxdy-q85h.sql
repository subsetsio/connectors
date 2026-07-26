-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "mmr_goal",
    "critical",
    "performance_indicator",
    "fy11",
    "fy12",
    "fy13",
    "fy14",
    "fy15",
    "tgt15",
    "tgt16",
    "desired_direction",
    "_5_yr_trend" AS 5_yr_trend
FROM "nyc-open-data-fxdy-q85h"
