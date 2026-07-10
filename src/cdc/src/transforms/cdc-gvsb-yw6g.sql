-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "level",
    CAST("perc_diff" AS DOUBLE) AS perc_diff,
    CAST("percent_pos" AS DOUBLE) AS percent_pos,
    CAST("percent_pos_2_week" AS DOUBLE) AS percent_pos_2_week,
    CAST("percent_pos_4_week" AS DOUBLE) AS percent_pos_4_week,
    CAST("number_tested" AS BIGINT) AS number_tested,
    CAST("number_tested_2_week" AS BIGINT) AS number_tested_2_week,
    CAST("number_tested_4_week" AS BIGINT) AS number_tested_4_week,
    "posted",
    "mmwrweek_end"
FROM "cdc-gvsb-yw6g"
