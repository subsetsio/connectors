-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: EPI indicator records represent state-level election-administration measures; compare values within a consistent indicator definition.
SELECT
    "state_abbv",
    CAST("state_fips" AS DOUBLE) AS state_fips,
    CAST("year" AS DOUBLE) AS year,
    CAST("website_pollingplace" AS BIGINT) AS website_pollingplace,
    "website_reg_status",
    "website_precinct_ballot",
    "website_absentee_status",
    "website_provisional_status",
    "reg_rej",
    "prov_partic",
    "prov_rej_all",
    "abs_rej_all_ballots",
    "abs_nonret",
    "uocava_rej",
    "uocava_nonret",
    "eavs_completeness",
    "post_election_audit",
    CAST("nonvoter_illness_pct" AS DOUBLE) AS nonvoter_illness_pct,
    CAST("nonvoter_reg_pct" AS DOUBLE) AS nonvoter_reg_pct,
    "online_reg",
    "wait",
    "residual",
    "pct_reg_of_vep_vrs",
    CAST("vep_turnout" AS DOUBLE) AS vep_turnout
FROM "mit-election-lab-dvn-skcc60"
