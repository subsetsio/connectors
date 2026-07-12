-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is a species observation within a submitted checklist at a count location; aggregate counts only after choosing the intended checklist, location, species, and time dimensions.
SELECT
    "LOC_ID" AS loc_id,
    CAST("LATITUDE" AS DOUBLE) AS latitude,
    CAST("LONGITUDE" AS DOUBLE) AS longitude,
    "SUBNATIONAL1_CODE" AS subnational1_code,
    "ENTRY_TECHNIQUE" AS entry_technique,
    "SUB_ID" AS sub_id,
    "OBS_ID" AS obs_id,
    CAST("Month" AS BIGINT) AS month,
    CAST("Day" AS BIGINT) AS day,
    CAST("Year" AS BIGINT) AS year,
    "PROJ_PERIOD_ID" AS proj_period_id,
    "SPECIES_CODE" AS species_code,
    "alt_full_spp_code",
    CAST("HOW_MANY" AS BIGINT) AS how_many,
    "PLUS_CODE" AS plus_code,
    CAST("VALID" AS BIGINT) AS valid,
    CAST("REVIEWED" AS BIGINT) AS reviewed,
    CAST("DAY1_AM" AS BIGINT) AS day1_am,
    CAST("DAY1_PM" AS BIGINT) AS day1_pm,
    CAST("DAY2_AM" AS BIGINT) AS day2_am,
    CAST("DAY2_PM" AS BIGINT) AS day2_pm,
    CAST("EFFORT_HRS_ATLEAST" AS DOUBLE) AS effort_hrs_atleast,
    CAST("SNOW_DEP_ATLEAST" AS DOUBLE) AS snow_dep_atleast,
    "Data_Entry_Method" AS data_entry_method
FROM "feederwatch-observations"
