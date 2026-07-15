-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "MonthlyIncomeFromWorkOfHusband_Below1_000" AS monthlyincomefromworkofhusband_below1_000,
    "MonthlyIncomeFromWorkOfHusband_1_000_1_499" AS monthlyincomefromworkofhusband_1_000_1_499,
    "MonthlyIncomeFromWorkOfHusband_1_500_1_999" AS monthlyincomefromworkofhusband_1_500_1_999,
    "MonthlyIncomeFromWorkOfHusband_2_000_2_499" AS monthlyincomefromworkofhusband_2_000_2_499,
    "MonthlyIncomeFromWorkOfHusband_2_500_2_999" AS monthlyincomefromworkofhusband_2_500_2_999,
    "MonthlyIncomeFromWorkOfHusband_3_000_3_999" AS monthlyincomefromworkofhusband_3_000_3_999,
    "MonthlyIncomeFromWorkOfHusband_4_000_4_999" AS monthlyincomefromworkofhusband_4_000_4_999,
    "MonthlyIncomeFromWorkOfHusband_5_000_5_999" AS monthlyincomefromworkofhusband_5_000_5_999,
    "MonthlyIncomeFromWorkOfHusband_6_000_6_999" AS monthlyincomefromworkofhusband_6_000_6_999,
    "MonthlyIncomeFromWorkOfHusband_7_000_7_999" AS monthlyincomefromworkofhusband_7_000_7_999,
    "MonthlyIncomeFromWorkOfHusband_8_000_8_999" AS monthlyincomefromworkofhusband_8_000_8_999,
    "MonthlyIncomeFromWorkOfHusband_9_000_9_999" AS monthlyincomefromworkofhusband_9_000_9_999,
    "MonthlyIncomeFromWorkOfHusband_10_000_10_999" AS monthlyincomefromworkofhusband_10_000_10_999,
    "MonthlyIncomeFromWorkOfHusband_11_000_11_999" AS monthlyincomefromworkofhusband_11_000_11_999,
    "MonthlyIncomeFromWorkOfHusband_12_000andOver" AS monthlyincomefromworkofhusband_12_000andover,
    "MonthlyIncomeFromWorkOfHusband_NotWorking" AS monthlyincomefromworkofhusband_notworking
FROM "sg-data-d-4736803af7f4e507826de26306621076"
