-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dollar" AS dollar,
    "Total" AS total,
    "MonthlyIncomeGroup_1_Below1_000" AS monthlyincomegroup_1_below1_000,
    "MonthlyIncomeGroup_1_1_000_1_999" AS monthlyincomegroup_1_1_000_1_999,
    "MonthlyIncomeGroup_1_2_000_2_999" AS monthlyincomegroup_1_2_000_2_999,
    "MonthlyIncomeGroup_1_3_000_3_999" AS monthlyincomegroup_1_3_000_3_999,
    "MonthlyIncomeGroup_1_4_000_4_999" AS monthlyincomegroup_1_4_000_4_999,
    "MonthlyIncomeGroup_1_5_000_5_999" AS monthlyincomegroup_1_5_000_5_999,
    "MonthlyIncomeGroup_1_6_000_7_999" AS monthlyincomegroup_1_6_000_7_999,
    "MonthlyIncomeGroup_1_8_000_9_999" AS monthlyincomegroup_1_8_000_9_999,
    "MonthlyIncomeGroup_1_10_000_11_999" AS monthlyincomegroup_1_10_000_11_999,
    "MonthlyIncomeGroup_1_12_000_14_999" AS monthlyincomegroup_1_12_000_14_999,
    "MonthlyIncomeGroup_1_15_000_19_999" AS monthlyincomegroup_1_15_000_19_999,
    "MonthlyIncomeGroup_1_20_000andOver" AS monthlyincomegroup_1_20_000andover
FROM "sg-data-d-2c0cee49fae1ff6e3e8b30594ba52f0f"
