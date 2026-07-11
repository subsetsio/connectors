-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_date",
    "intraday_repo_at_0900",
    "overnight_repo_at_0900",
    "plp_fac_at_0900",
    "intraday_repo_at_1100",
    "overnight_repo_at_1100",
    "plp_fac_at_1100",
    "intraday_repo_at_1400",
    "overnight_repo_at_1400",
    "plp_fac_at_1400",
    "intraday_repo_at_1600",
    "overnight_repo_at_1600",
    "plp_fac_at_1600"
FROM "hkma-rmb-liquidity-facility-usage"
