-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "MonthlyIncomefromWork1_ofHusband_Below1_000" AS monthlyincomefromwork1_ofhusband_below1_000,
    "MonthlyIncomefromWork1_ofHusband_1_000_1_999" AS monthlyincomefromwork1_ofhusband_1_000_1_999,
    "MonthlyIncomefromWork1_ofHusband_2_000_2_999" AS monthlyincomefromwork1_ofhusband_2_000_2_999,
    "MonthlyIncomefromWork1_ofHusband_3_000_3_999" AS monthlyincomefromwork1_ofhusband_3_000_3_999,
    "MonthlyIncomefromWork1_ofHusband_4_000_4_999" AS monthlyincomefromwork1_ofhusband_4_000_4_999,
    "MonthlyIncomefromWork1_ofHusband_5_000_5_999" AS monthlyincomefromwork1_ofhusband_5_000_5_999,
    "MonthlyIncomefromWork1_ofHusband_6_000_6_999" AS monthlyincomefromwork1_ofhusband_6_000_6_999,
    "MonthlyIncomefromWork1_ofHusband_7_000_7_999" AS monthlyincomefromwork1_ofhusband_7_000_7_999,
    "MonthlyIncomefromWork1_ofHusband_8_000_8_999" AS monthlyincomefromwork1_ofhusband_8_000_8_999,
    "MonthlyIncomefromWork1_ofHusband_9_000_9_999" AS monthlyincomefromwork1_ofhusband_9_000_9_999,
    "MonthlyIncomefromWork1_ofHusband_10_000_10_999" AS monthlyincomefromwork1_ofhusband_10_000_10_999,
    "MonthlyIncomefromWork1_ofHusband_11_000_11_999" AS monthlyincomefromwork1_ofhusband_11_000_11_999,
    "MonthlyIncomefromWork1_ofHusband_12_000_14_999" AS monthlyincomefromwork1_ofhusband_12_000_14_999,
    "MonthlyIncomefromWork1_ofHusband_15_000andOver" AS monthlyincomefromwork1_ofhusband_15_000andover,
    "MonthlyIncomefromWork1_ofHusband_NotEmployed" AS monthlyincomefromwork1_ofhusband_notemployed
FROM "sg-data-d-0c3bb89a2e033e6d2f6fe5e4ade4fce4"
