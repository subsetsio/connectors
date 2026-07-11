-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: HOME homeownership value limits include HUD area definitions used for program eligibility and should not be interpreted as a complete county-only geography.
SELECT
    "state",
    "county_name",
    "metropolitan_fmr_area_name",
    "1_unit",
    "2_unit",
    "3_unit",
    "4_unit",
    "unadjusted_median_value",
    "years_worth_of_sales_data",
    "number_of_sales_for_unadjusted_median",
    "1_unit_1",
    "2_unit_1",
    "3_unit_1",
    "4_unit_1",
    "unadjusted_median_value_1",
    "years_worth_of_sales_data_1",
    "number_of_sales_in_time_period_for_unadjusted_median",
    "geographic_area_used",
    "geographic_area_used_1",
    "state_fips",
    "fmr_metro_code",
    "state_county_fips",
    "col_22",
    "col_23",
    "change_from_2014_to_existing",
    "change_from_2014_to_new",
    "col_19",
    "col_20",
    "col_21",
    "number_of_sales_for_unadjusted_median_1",
    "state2",
    "metro_code",
    "fipscounty",
    "metropolitan_fmr_area_name_1",
    "fiscal_year"
FROM "hud-home-ownership-value-limits"
