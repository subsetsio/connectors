-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "AgeGroupOfHusband_Years_Below25" AS agegroupofhusband_years_below25,
    "AgeGroupOfHusband_Years_25_29" AS agegroupofhusband_years_25_29,
    "AgeGroupOfHusband_Years_30_34" AS agegroupofhusband_years_30_34,
    "AgeGroupOfHusband_Years_35_39" AS agegroupofhusband_years_35_39,
    "AgeGroupOfHusband_Years_40_44" AS agegroupofhusband_years_40_44,
    "AgeGroupOfHusband_Years_45_49" AS agegroupofhusband_years_45_49,
    "AgeGroupOfHusband_Years_50_54" AS agegroupofhusband_years_50_54,
    "AgeGroupOfHusband_Years_55_59" AS agegroupofhusband_years_55_59,
    "AgeGroupOfHusband_Years_60_64" AS agegroupofhusband_years_60_64,
    "AgeGroupOfHusband_Years_65_69" AS agegroupofhusband_years_65_69,
    "AgeGroupOfHusband_Years_70andOver" AS agegroupofhusband_years_70andover
FROM "sg-data-d-9e2be3cfc611e1cbb8784c77295ecb6e"
