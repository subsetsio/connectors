-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Retirement experiences" AS retirement_experiences,
    "U.S. residing doctorate recipients - Total - Number" AS u_s_residing_doctorate_recipients_total_number,
    "U.S. residing doctorate recipients - Total - SE" AS u_s_residing_doctorate_recipients_total_se,
    "U.S. residing doctorate recipients - Employed previously retireda - Full time - Percent" AS u_s_residing_doctorate_recipients_employed_previously_retireda_full_time_percent,
    "U.S. residing doctorate recipients - Employed previously retireda - Full time - SE" AS u_s_residing_doctorate_recipients_employed_previously_retireda_full_time_se,
    "U.S. residing doctorate recipients - Employed previously retireda - Part time - Percent" AS u_s_residing_doctorate_recipients_employed_previously_retireda_part_time_percent,
    "U.S. residing doctorate recipients - Employed previously retireda - Part time - SE" AS u_s_residing_doctorate_recipients_employed_previously_retireda_part_time_se,
    "U.S. residing doctorate recipients - Not employed retiredb - Under 67 - Percent" AS u_s_residing_doctorate_recipients_not_employed_retiredb_under_67_percent,
    "U.S. residing doctorate recipients - Not employed retiredb - Under 67 - SE" AS u_s_residing_doctorate_recipients_not_employed_retiredb_under_67_se,
    "U.S. residing doctorate recipients - Not employed retiredb - 67–75 - Percent" AS u_s_residing_doctorate_recipients_not_employed_retiredb_67_75_percent,
    "U.S. residing doctorate recipients - Not employed retiredb - 67–75 - SE" AS u_s_residing_doctorate_recipients_not_employed_retiredb_67_75_se,
    "Non-U.S. residing doctorate recipients - Total - 67–75 - Number" AS non_u_s_residing_doctorate_recipients_total_67_75_number,
    "Non-U.S. residing doctorate recipients - Total - 67–75 - SE" AS non_u_s_residing_doctorate_recipients_total_67_75_se,
    "Non-U.S. residing doctorate recipients - Employed previously retireda - Full time - Percent" AS non_u_s_residing_doctorate_recipients_employed_previously_retireda_full_time_percent,
    "Non-U.S. residing doctorate recipients - Employed previously retireda - Full time - SE" AS non_u_s_residing_doctorate_recipients_employed_previously_retireda_full_time_se,
    "Non-U.S. residing doctorate recipients - Employed previously retireda - Part time - Percent" AS non_u_s_residing_doctorate_recipients_employed_previously_retireda_part_time_percent,
    "Non-U.S. residing doctorate recipients - Employed previously retireda - Part time - SE" AS non_u_s_residing_doctorate_recipients_employed_previously_retireda_part_time_se,
    "Non-U.S. residing doctorate recipients - Not employed retiredb - Under 67 - Percent" AS non_u_s_residing_doctorate_recipients_not_employed_retiredb_under_67_percent,
    "Non-U.S. residing doctorate recipients - Not employed retiredb - Under 67 - SE" AS non_u_s_residing_doctorate_recipients_not_employed_retiredb_under_67_se,
    "Non-U.S. residing doctorate recipients - Not employed retiredb - 67–75 - Percent" AS non_u_s_residing_doctorate_recipients_not_employed_retiredb_67_75_percent,
    "Non-U.S. residing doctorate recipients - Not employed retiredb - 67–75 - SE" AS non_u_s_residing_doctorate_recipients_not_employed_retiredb_67_75_se
FROM "ncses-nsf25321-tabr-002"
