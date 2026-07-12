-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("state_id" AS BIGINT) AS state_id,
    "provider_name",
    CAST("accepts_cc_subsidy" AS BIGINT) AS accepts_cc_subsidy,
    CAST("reporting_date" AS TIMESTAMP) AS reporting_date,
    CAST("trs_effective_sd" AS TIMESTAMP) AS trs_effective_sd,
    CAST("trs_effective_ed" AS TIMESTAMP) AS trs_effective_ed,
    "tx_rising_star_rating"
FROM "texas-workforce-commission-socrata-wmur-pmzc"
