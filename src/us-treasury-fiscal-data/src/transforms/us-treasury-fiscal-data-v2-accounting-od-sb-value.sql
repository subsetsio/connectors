-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime(NULLIF("redemp_period", 'null'), '%Y-%m')::DATE AS redemp_period,
    CAST(NULLIF("redemption_year", 'null') AS BIGINT) AS redemption_year,
    CAST(NULLIF("redemption_month", 'null') AS BIGINT) AS redemption_month,
    "series_cd",
    CAST(NULLIF("issue_year", 'null') AS BIGINT) AS issue_year,
    "issue_jan_amt",
    "issue_feb_amt",
    "issue_mar_amt",
    "issue_apr_amt",
    "issue_may_amt",
    "issue_jun_amt",
    "issue_jul_amt",
    "issue_aug_amt",
    "issue_sep_amt",
    "issue_oct_amt",
    "issue_nov_amt",
    "issue_dec_amt",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr
FROM "us-treasury-fiscal-data-v2-accounting-od-sb-value"
