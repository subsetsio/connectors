-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Fair Market Rent rows mix county records and HUD FMR area records; choose the relevant area code family before aggregating or comparing geographies.
SELECT
    "fips2010",
    "fmr_0",
    "fmr_1",
    "fmr_2",
    "fmr_3",
    "fmr_4",
    "state",
    "metro_code",
    "areaname",
    "countyname",
    "county_town_name",
    "pop2017",
    "state_alpha",
    CAST("metro" AS DOUBLE) AS metro,
    "fips",
    "hud_area_name",
    "hud_area_code",
    "pop2020",
    "stusps",
    "pop2022",
    "pop2023",
    "fiscal_year"
FROM "hud-fmr"
