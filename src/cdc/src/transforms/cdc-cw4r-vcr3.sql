-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Severe acute respiratory syndrome-associated coronavirus desease, Current week" AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_current_week,
    "Severe acute respiratory syndrome-associated coronavirus desease, Current week, flag" AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_current_week_flag,
    CAST("Severe acute respiratory syndrome-associated coronavirus desease, Previous 52 weeks Max†" AS BIGINT) AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_previous_52_weeks_max,
    "Severe acute respiratory syndrome-associated coronavirus desease, Previous 52 weeks Max†, flag" AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_previous_52_weeks_max_flag,
    CAST("Severe acute respiratory syndrome-associated coronavirus desease, Cum 2021†" AS BIGINT) AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_cum_2021,
    "Severe acute respiratory syndrome-associated coronavirus desease, Cum 2021†, flag" AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_cum_2021_flag,
    CAST("Severe acute respiratory syndrome-associated coronavirus desease, Cum 2020†" AS BIGINT) AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_cum_2020,
    "Severe acute respiratory syndrome-associated coronavirus desease, Cum 2020†, flag" AS severe_acute_respiratory_syndrome_associated_coronavirus_desease_cum_2020_flag,
    CAST("Shiga toxin-producing Escherichia coli(STEC), Current week" AS BIGINT) AS shiga_toxin_producing_escherichia_coli_stec_current_week,
    "Shiga toxin-producing Escherichia coli(STEC), Current week, flag" AS shiga_toxin_producing_escherichia_coli_stec_current_week_flag,
    CAST("Shiga toxin-producing Escherichia coli(STEC), Previous 52 weeks Max†" AS BIGINT) AS shiga_toxin_producing_escherichia_coli_stec_previous_52_weeks_max,
    "Shiga toxin-producing Escherichia coli(STEC), Previous 52 weeks Max†, flag" AS shiga_toxin_producing_escherichia_coli_stec_previous_52_weeks_max_flag,
    CAST("Shiga toxin-producing Escherichia coli(STEC), Cum 2021†" AS BIGINT) AS shiga_toxin_producing_escherichia_coli_stec_cum_2021,
    "Shiga toxin-producing Escherichia coli(STEC), Cum 2021†, flag" AS shiga_toxin_producing_escherichia_coli_stec_cum_2021_flag,
    CAST("Shiga toxin-producing Escherichia coli(STEC), Cum 2020†" AS BIGINT) AS shiga_toxin_producing_escherichia_coli_stec_cum_2020,
    "Shiga toxin-producing Escherichia coli(STEC), Cum 2020†, flag" AS shiga_toxin_producing_escherichia_coli_stec_cum_2020_flag,
    CAST("Shigellosis, Current week" AS BIGINT) AS shigellosis_current_week,
    "Shigellosis, Current week, flag" AS shigellosis_current_week_flag,
    CAST("Shigellosis, Previous 52 weeks Max†" AS BIGINT) AS shigellosis_previous_52_weeks_max,
    "Shigellosis, Previous 52 weeks Max†, flag" AS shigellosis_previous_52_weeks_max_flag,
    CAST("Shigellosis, Cum 2021†" AS BIGINT) AS shigellosis_cum_2021,
    "Shigellosis, Cum 2021†, flag" AS shigellosis_cum_2021_flag,
    CAST("Shigellosis, Cum 2020†" AS BIGINT) AS shigellosis_cum_2020,
    "Shigellosis, Cum 2020†, flag" AS shigellosis_cum_2020_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-cw4r-vcr3"
