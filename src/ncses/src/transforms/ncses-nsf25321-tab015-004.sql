-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Field of study" AS field_of_study,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "Primary work activitya - Any R and Db - Number" AS primary_work_activitya_any_r_and_db_number,
    "Primary work activitya - Any R and Db - SE" AS primary_work_activitya_any_r_and_db_se,
    "Primary work activitya - Otherc - Number" AS primary_work_activitya_otherc_number,
    "Primary work activitya - Otherc - SE" AS primary_work_activitya_otherc_se
FROM "ncses-nsf25321-tab015-004"
