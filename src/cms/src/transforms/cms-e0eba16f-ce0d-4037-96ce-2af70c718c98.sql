-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "aco_id",
    "par_lbn",
    "aco_name",
    CAST("perf_year" AS BIGINT) AS perf_year,
    "start_date",
    "term_date",
    "prvdr_class",
    "capitation_arrangement",
    "apo_election",
    "telehealth_waiver",
    "pdhv_waiver",
    "snf_waiver",
    "cmhv_waiver",
    "homeboundhh_waiver",
    "hospicecc_waiver",
    "ptbcost_bei_waiver",
    "chronicdisease_bei_waiver",
    "diabeticshoe_waiver",
    "hit_waiver",
    "mnt_waiver"
FROM "cms-e0eba16f-ce0d-4037-96ce-2af70c718c98"
