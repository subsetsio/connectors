-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("ID" AS BIGINT) AS id,
    "Country_Name" AS country_name,
    CAST("Country_ID" AS BIGINT) AS country_id,
    CAST("Region_Code" AS BIGINT) AS region_code,
    "Region_Name" AS region_name,
    CAST("State_Code" AS BIGINT) AS state_code,
    "State_Name" AS state_name,
    "Municipal_Code" AS municipal_code,
    "Municipality_Name" AS municipality_name,
    CAST("Metro_area_Code" AS BIGINT) AS metro_area_code,
    "Metro_area_Name" AS metro_area_name,
    "Microregion_Name" AS microregion_name,
    CAST("Microregion_Code" AS BIGINT) AS microregion_code,
    CAST("Year_Text" AS BIGINT) AS year_text,
    CAST("Year_Date" AS BIGINT) AS year_date,
    CAST("Year_of_creation_of_municipality_post-2000" AS BIGINT) AS year_of_creation_of_municipality_post_2000,
    CAST("Municipality_belongs_to_a_metro_area" AS BIGINT) AS municipality_belongs_to_a_metro_area,
    CAST("Municipality_is_seat_of_the_state_government" AS BIGINT) AS municipality_is_seat_of_the_state_government,
    CAST("Municipality_is_primate" AS BIGINT) AS municipality_is_primate,
    CAST("Territorial_extension_km2" AS DOUBLE) AS territorial_extension_km2,
    "Indicator_Name" AS indicator_name,
    "Indicator_ID" AS indicator_id,
    CAST("Indicator_Code" AS BIGINT) AS indicator_code,
    CAST("Value" AS DOUBLE) AS value,
    "Location_1" AS location_1,
    "source_resource"
FROM "idb-data-associated-with-growing-resources-for-growing-cities-density-and-the-c"
