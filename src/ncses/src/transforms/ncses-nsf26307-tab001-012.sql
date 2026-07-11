-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Year" AS year,
    "Total" AS total,
    "DOD - Number" AS dod_number,
    "DOD - Percent" AS dod_percent,
    "DOE - Number" AS doe_number,
    "DOE - Percent" AS doe_percent,
    "HHS: NIH - Number" AS hhs_nih_number,
    "HHS: NIH - Percent" AS hhs_nih_percent,
    "HHS: Other HHS - Number" AS hhs_other_hhs_number,
    "HHS: Other HHS - Percent" AS hhs_other_hhs_percent,
    "NASA - Number" AS nasa_number,
    "NASA - Percent" AS nasa_percent,
    "NSF - Number" AS nsf_number,
    "NSF - Percent" AS nsf_percent,
    "USDA - Number" AS usda_number,
    "USDA - Percent" AS usda_percent,
    "Other - Number" AS other_number,
    "Other - Percent" AS other_percent
FROM "ncses-nsf26307-tab001-012"
