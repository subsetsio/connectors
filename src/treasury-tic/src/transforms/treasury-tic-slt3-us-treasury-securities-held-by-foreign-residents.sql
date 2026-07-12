-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes jurisdictions and aggregate categories alongside countries, so filter to the desired geography level before summing across countries.
SELECT
    "country",
    CAST("country_code" AS BIGINT) AS country_code,
    strptime("date", '%Y-%m')::DATE AS date,
    "for_treas_pos",
    "for_treas_net",
    "for_lt_treas_pos",
    "for_lt_treas_net",
    "for_lt_treas_valchg",
    "for_st_treas_pos",
    "for_st_treas_net"
FROM "treasury-tic-slt3-us-treasury-securities-held-by-foreign-residents"
