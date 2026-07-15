-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "AgeGroupofWife_Years_Total" AS agegroupofwife_years_total,
    "AgeGroupofWife_Years_Below30" AS agegroupofwife_years_below30,
    "AgeGroupofWife_Years_30_34" AS agegroupofwife_years_30_34,
    "AgeGroupofWife_Years_35_39" AS agegroupofwife_years_35_39,
    "AgeGroupofWife_Years_40_44" AS agegroupofwife_years_40_44,
    "AgeGroupofWife_Years_45_49" AS agegroupofwife_years_45_49,
    "AgeGroupofWife_Years_50_54" AS agegroupofwife_years_50_54,
    "AgeGroupofWife_Years_55_59" AS agegroupofwife_years_55_59,
    "AgeGroupofWife_Years_60_64" AS agegroupofwife_years_60_64,
    "AgeGroupofWife_Years_65andOver" AS agegroupofwife_years_65andover
FROM "sg-data-d-c9551d36a009d0def59d4b2f298573fa"
