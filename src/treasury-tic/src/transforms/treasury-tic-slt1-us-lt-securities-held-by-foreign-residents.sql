-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes jurisdictions and aggregate categories alongside countries, so filter to the desired geography level before summing across countries.
SELECT
    "country",
    CAST("country_code" AS BIGINT) AS country_code,
    strptime("date", '%Y-%m')::DATE AS date,
    "for_lt_total_pos",
    "for_lt_total_net",
    "for_lt_total_valchg",
    "for_lt_treas_pos",
    "for_lt_treas_net",
    "for_lt_treas_valchg",
    "for_lt_agcy_pos",
    "for_lt_agcy_net",
    "for_lt_agcy_valchg",
    "for_lt_corp_pos",
    "for_lt_corp_net",
    "for_lt_corp_valchg",
    "for_lt_eqty_pos",
    "for_lt_eqty_net",
    "for_lt_eqty_valchg"
FROM "treasury-tic-slt1-us-lt-securities-held-by-foreign-residents"
