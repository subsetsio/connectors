-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reporting Area" AS reporting_area,
    CAST("MMWR Year" AS BIGINT) AS mmwr_year,
    CAST("MMWR Week" AS BIGINT) AS mmwr_week,
    "Brucellosis, Current week" AS brucellosis_current_week,
    "Brucellosis, Current week, flag" AS brucellosis_current_week_flag,
    CAST("Brucellosis, Previous 52 weeks Max†" AS BIGINT) AS brucellosis_previous_52_weeks_max,
    "Brucellosis, Previous 52 weeks Max†, flag" AS brucellosis_previous_52_weeks_max_flag,
    CAST("Brucellosis, Cum 2022†" AS BIGINT) AS brucellosis_cum_2022,
    "Brucellosis, Cum 2022†, flag" AS brucellosis_cum_2022_flag,
    CAST("Brucellosis, Cum 2021†" AS BIGINT) AS brucellosis_cum_2021,
    "Brucellosis, Cum 2021, flag" AS brucellosis_cum_2021_flag,
    CAST("Campylobacteriosis, Current week" AS BIGINT) AS campylobacteriosis_current_week,
    "Campylobacteriosis, Current week, flag" AS campylobacteriosis_current_week_flag,
    CAST("Campylobacteriosis, Previous 52 weeks Max†" AS BIGINT) AS campylobacteriosis_previous_52_weeks_max,
    "Campylobacteriosis, Previous 52 weeks Max†, flag" AS campylobacteriosis_previous_52_weeks_max_flag,
    CAST("Campylobacteriosis, Cum 2022†" AS BIGINT) AS campylobacteriosis_cum_2022,
    "Campylobacteriosis, Cum 2022†, flag" AS campylobacteriosis_cum_2022_flag,
    CAST("Campylobacteriosis, Cum 2021†" AS BIGINT) AS campylobacteriosis_cum_2021,
    "Campylobacteriosis, Cum 2021†, flag" AS campylobacteriosis_cum_2021_flag,
    CAST("Candida auris, clinical§, Current week" AS BIGINT) AS candida_auris_clinical_current_week,
    "Candida auris, clinical§, Current week, flag" AS candida_auris_clinical_current_week_flag,
    CAST("Candida auris, clinical§, Previous 52 weeks Max†" AS BIGINT) AS candida_auris_clinical_previous_52_weeks_max,
    "Candida auris, clinical§, Previous 52 weeks Max†, flag" AS candida_auris_clinical_previous_52_weeks_max_flag,
    CAST("Candida auris, clinical§, Cum 2022†" AS BIGINT) AS candida_auris_clinical_cum_2022,
    "Candida auris, clinical§, Cum 2022†, flag" AS candida_auris_clinical_cum_2022_flag,
    CAST("Candida auris, clinical§, Cum 2021†" AS BIGINT) AS candida_auris_clinical_cum_2021,
    "Candida auris, clinical§, Cum 2021, flag" AS candida_auris_clinical_cum_2021_flag,
    "Location 1" AS location_1,
    "Location 2" AS location_2,
    CAST("Reporting Area Sort" AS BIGINT) AS reporting_area_sort,
    "geocode"
FROM "cdc-n322-ce6f"
