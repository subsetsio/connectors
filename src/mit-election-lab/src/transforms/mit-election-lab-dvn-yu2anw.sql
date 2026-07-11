-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Elections Performance Index measures are state-level indicators for one EPI release; compare only like indicators across states.
SELECT
    "state_abbv",
    "n_abs_nonret",
    "n_abs_rej_all_ballots",
    "n_eavs_completeness",
    "n_nonvoter_illness_pct",
    "n_nonvoter_reg_pct",
    "n_online_reg",
    "n_pct_reg_of_vep_vrs",
    CAST("n_post_election_audit" AS BIGINT) AS n_post_election_audit,
    "n_prov_partic",
    "n_prov_rej_all",
    "n_reg_rej",
    "n_uocava_nonret",
    "n_uocava_rej",
    "n_vep_turnout",
    "n_wait",
    "n_website",
    "state",
    "index"
FROM "mit-election-lab-dvn-yu2anw"
