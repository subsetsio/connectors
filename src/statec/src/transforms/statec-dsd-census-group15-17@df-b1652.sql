-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "SEX: Sex" AS sex_sex,
    "AGE: Age class" AS age_age_class,
    "LMS: Legal marital status" AS lms_legal_marital_status,
    "HST: Household status" AS hst_household_status,
    "FST: Familly status" AS fst_familly_status,
    "HAR: Housing arrangements" AS har_housing_arrangements,
    "LOC_SIZE: Size of the locality" AS loc_size_size_of_the_locality,
    "WSTATUS: Working status" AS wstatus_working_status,
    "ISCO08: Occupation (ISCO-08)" AS isco08_occupation_isco_08,
    "EDU: Educational level" AS edu_educational_level,
    "SIE: Employment status" AS sie_employment_status,
    "LPW: Place of work" AS lpw_place_of_work,
    "C_BIRTH: Country of birth" AS c_birth_country_of_birth,
    "CITIZEN: Citizenship" AS citizen_citizenship,
    "YAE: Year of arrival in the country since 1980" AS yae_year_of_arrival_in_the_country_since_1980,
    "YAT: Year of arrival in the country since 2010" AS yat_year_of_arrival_in_the_country_since_2010,
    "ROY: Place of usual residence one year prior to the census" AS roy_place_of_usual_residence_one_year_prior_to_the_census,
    "GEO: Geographic level" AS geo_geographic_level,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier
FROM "statec-dsd-census-group15-17@df-b1652"
