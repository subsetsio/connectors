-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "lottery_id",
    "lottery_name",
    "lottery_status",
    "development_type",
    "lottery_start_date",
    "lottery_end_date",
    "building_count",
    "unit_count",
    "unit_distribution_studio",
    "unit_distribution_1_bedroom",
    "unit_distribution_2_bedrooms",
    "unit_distribution_3_bedrooms",
    "unit_distribution_4_bedroom",
    "applied_income_ami_category_extremely_low_income",
    "applied_income_ami_category_very_low_income",
    "applied_income_ami_category_low_income",
    "applied_income_ami_category_moderate_income",
    "applied_income_ami_category_middle_income",
    "applied_income_ami_category_above_middle_income",
    "lottery_mobility_percentage",
    "lottery_visionhearing_percentage",
    "lottery_community_board_percentage",
    "lottery_municipal_employeemilitary_veteran_percentage",
    "lottery_nycha_percentage",
    "lottery_senior_percentage",
    "borough",
    "postcode",
    "community_board",
    "latitude",
    "longitude"
FROM "nyc-open-data-vy5i-a666"
