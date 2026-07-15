-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "AgeGroupofHusband_Years_Total" AS agegroupofhusband_years_total,
    "AgeGroupofHusband_Years_Below30" AS agegroupofhusband_years_below30,
    "AgeGroupofHusband_Years_30_34" AS agegroupofhusband_years_30_34,
    "AgeGroupofHusband_Years_35_39" AS agegroupofhusband_years_35_39,
    "AgeGroupofHusband_Years_40_44" AS agegroupofhusband_years_40_44,
    "AgeGroupofHusband_Years_45_49" AS agegroupofhusband_years_45_49,
    "AgeGroupofHusband_Years_50_54" AS agegroupofhusband_years_50_54,
    "AgeGroupofHusband_Years_55_59" AS agegroupofhusband_years_55_59,
    "AgeGroupofHusband_Years_60_64" AS agegroupofhusband_years_60_64,
    "AgeGroupofHusband_Years_65andOver" AS agegroupofhusband_years_65andover
FROM "sg-data-d-c42a8e0d78923303e2b938167ced06ea"
