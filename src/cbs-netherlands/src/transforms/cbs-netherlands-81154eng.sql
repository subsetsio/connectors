-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CaribbeanNetherlands" AS caribbeannetherlands,
    "Periods" AS periods,
    "TotalHouseholdsAndCompanies_1" AS totalhouseholdsandcompanies_1,
    "Total_2" AS total_2,
    "Prepaid_3" AS prepaid_3,
    "Postpaid_4" AS postpaid_4,
    "Companies_5" AS companies_5,
    "Total_6" AS total_6,
    "Fossil_7" AS fossil_7,
    "Renewable_8" AS renewable_8,
    "OilTransit_9" AS oiltransit_9,
    "TotalHouseholdsAndCompanies_10" AS totalhouseholdsandcompanies_10,
    "Households_11" AS households_11,
    "Companies_12" AS companies_12,
    "Production_13" AS production_13,
    "CaribbeanNetherlands_label" AS caribbeannetherlands_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-81154eng"
