-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Elections Performance Index measures are state-level indicators for one EPI release; compare only like indicators across states.
SELECT
    "state_abbv",
    CAST("state_fips" AS DOUBLE) AS state_fips,
    CAST("index_2016" AS DOUBLE) AS index_2016,
    CAST("rank_2016" AS DOUBLE) AS rank_2016,
    CAST("indicator_count_2016" AS DOUBLE) AS indicator_count_2016
FROM "mit-election-lab-dvn-mqmmhz"
