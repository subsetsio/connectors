-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This reproduction-style EPI table combines derived election-administration measures; use the source column definitions before treating similarly named measures as interchangeable.
SELECT
    "state_abbv",
    "state_fips",
    CAST("year" AS BIGINT) AS year,
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
    "nonvoter_illness_onyear_pct",
    "nonvoter_illness_offyear_pct",
    "nonvoter_reg_onyear_pct",
    "nonvoter_reg_offyear_pct",
    "online_reg",
    "wait",
    "residual",
    "pct_reg_of_vep_vrs",
    "vep_turnout",
    "nonvoter_illness_onyear_new",
    "eric_membership",
    "risk_limiting_audits",
    "nonvoter_illness_offyear_new"
FROM "mit-election-lab-dvn-9uf1zm"
