-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "AgeGroupOfHusband_Years_Total" AS agegroupofhusband_years_total,
    "AgeGroupOfHusband_Years_Below25" AS agegroupofhusband_years_below25,
    "AgeGroupOfHusband_Years_25_29" AS agegroupofhusband_years_25_29,
    "AgeGroupOfHusband_Years_30_34" AS agegroupofhusband_years_30_34,
    "AgeGroupOfHusband_Years_35_39" AS agegroupofhusband_years_35_39,
    "AgeGroupOfHusband_Years_40_44" AS agegroupofhusband_years_40_44,
    "AgeGroupOfHusband_Years_45_49" AS agegroupofhusband_years_45_49,
    "AgeGroupOfHusband_Years_50_54" AS agegroupofhusband_years_50_54,
    "AgeGroupOfHusband_Years_55_59" AS agegroupofhusband_years_55_59,
    "AgeGroupOfHusband_Years_60_64" AS agegroupofhusband_years_60_64,
    "AgeGroupOfHusband_Years_65andOver" AS agegroupofhusband_years_65andover
FROM "sg-data-d-74e4757b6da52ef57be10508f7668360"
