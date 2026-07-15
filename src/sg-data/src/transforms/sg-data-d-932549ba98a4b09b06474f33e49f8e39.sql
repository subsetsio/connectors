-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PerCent" AS percent,
    "Total" AS total,
    "MonthlyExpenditureGroup_1_Below1_000" AS monthlyexpendituregroup_1_below1_000,
    "MonthlyExpenditureGroup_1_1_000_1_999" AS monthlyexpendituregroup_1_1_000_1_999,
    "MonthlyExpenditureGroup_1_2_000_2_999" AS monthlyexpendituregroup_1_2_000_2_999,
    "MonthlyExpenditureGroup_1_3_000_3_999" AS monthlyexpendituregroup_1_3_000_3_999,
    "MonthlyExpenditureGroup_1_4_000_4_999" AS monthlyexpendituregroup_1_4_000_4_999,
    "MonthlyExpenditureGroup_1_5_000_5_999" AS monthlyexpendituregroup_1_5_000_5_999,
    "MonthlyExpenditureGroup_1_6_000_7_999" AS monthlyexpendituregroup_1_6_000_7_999,
    "MonthlyExpenditureGroup_1_8_000_9_999" AS monthlyexpendituregroup_1_8_000_9_999,
    "MonthlyExpenditureGroup_1_10_000_11_999" AS monthlyexpendituregroup_1_10_000_11_999,
    "MonthlyExpenditureGroup_1_12_000_14_999" AS monthlyexpendituregroup_1_12_000_14_999,
    "MonthlyExpenditureGroup_1_15_000andOver" AS monthlyexpendituregroup_1_15_000andover
FROM "sg-data-d-932549ba98a4b09b06474f33e49f8e39"
