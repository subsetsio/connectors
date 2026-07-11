-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows combine teacher and principal inexperience measures plus low- and high-poverty subsets; those subsets are not additive totals.
SELECT
    "report_year",
    CAST("institution_id" AS BIGINT) AS institution_id,
    "entity_cd",
    "entity_name",
    "year",
    "num_teach",
    "num_teach_inexp",
    "per_teach_inexp",
    "tot_teach_low",
    "num_teach_low",
    "per_teach_low",
    "tot_teach_high",
    "num_teach_high",
    "per_teach_high",
    "num_princ",
    "num_princ_inexp",
    "per_princ_inexp",
    "tot_princ_low",
    "num_princ_low",
    "per_princ_low",
    "tot_princ_high",
    "num_princ_high",
    "per_princ_high",
    "teach_data_rep_flag",
    "prin_data_rep_flag"
FROM "new-york-state-education-department-src-inexperienced-teachers-principals"
