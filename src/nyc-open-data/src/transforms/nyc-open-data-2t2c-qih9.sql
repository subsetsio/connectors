-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_number",
    "agency_name",
    "fiscal_year",
    "personnel_type_code",
    "personnel_type_name",
    "code_for_fulltime_ftes",
    "fulltimefulltime_equivalents_ft_fte_positions",
    "city_funded_headcount",
    "ifa_funded_headcount",
    "cd_funded_headcount",
    "other_funded_headcount",
    "total"
FROM "nyc-open-data-2t2c-qih9"
