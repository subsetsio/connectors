-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "Year" AS "year",
    "% of GDP" AS "of_gdp",
    "gov't" AS "gov_t",
    "authorities",
    "Grant Comm." AS "grant_comm",
    "totals (£)" AS "totals",
    "authorities_2",
    "gov't_2" AS "gov_t_2",
    "authorities_3",
    "Grant Comm._2" AS "grant_comm_2",
    "totals (£)_2" AS "totals_2",
    "Total" AS "total",
    "education",
    "education_2",
    "education_3",
    "education_4",
    "education_5",
    "training",
    "education_6",
    "inspection",
    "(residual)" AS "residual",
    "GDP" AS "gdp",
    "GDP_2" AS "gdp_2",
    "GDP_3" AS "gdp_3",
    "Mitchell GDP" AS "mitchell_gdp",
    "in BofE GDP" AS "in_bofe_gdp"
FROM "gpih-uk-educ-exp-1833-1997a"
