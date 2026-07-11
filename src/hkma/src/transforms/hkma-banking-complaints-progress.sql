-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Combines `new` half-yearly complaint progress rows and `old` monthly legacy rows in one segmented endpoint; use the segment-specific period column before time-series analysis.
SELECT
    "end_of_half_year",
    "conduct_related_r",
    "conduct_related_c",
    "general_bank_r",
    "general_bank_c",
    "total_cur_r",
    "total_cur_c",
    "segment",
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "conduct_related_last_mth_p",
    "conduct_related_cur_mth_r",
    "conduct_related_cur_mth_c",
    "conduct_related_cur_mth_p",
    "general_bank_last_mth_p",
    "general_bank_cur_mth_r",
    "general_bank_cur_mth_c",
    "general_bank_cur_mth_p",
    "total_last_mth_p",
    "total_cur_mth_r",
    "total_cur_mth_c",
    "total_cur_mth_p"
FROM "hkma-banking-complaints-progress"
