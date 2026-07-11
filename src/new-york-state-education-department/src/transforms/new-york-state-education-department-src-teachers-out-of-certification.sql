-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows combine overall and poverty-subset out-of-certification measures; low- and high-poverty subsets should not be treated as complete additive partitions.
SELECT
    "report_year",
    CAST("institution_id" AS BIGINT) AS institution_id,
    "entity_cd",
    "entity_name",
    "year",
    "num_teach_oc",
    "num_out_cert",
    "per_out_cert",
    "tot_out_cert_low",
    "num_out_cert_low",
    "per_out_cert_low",
    "tot_out_cert_high",
    "num_out_cert_high",
    "per_out_cert_high",
    "out_of_cert_data_rep_flag"
FROM "new-york-state-education-department-src-teachers-out-of-certification"
