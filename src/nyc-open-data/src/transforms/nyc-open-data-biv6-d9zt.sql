-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "district",
    "building_code",
    "dbn",
    "school_name",
    "schoolfood_code",
    "breakfast_before_bell_adp_fy18",
    "breakfast_before_bell_adp_fy19",
    "breakfast_in_classroom_adp_where_available_see_key_tab_fy18",
    "breakfast_in_classroom_adp_where_available_see_key_tab_fy19",
    "breakfast_before_bell_y_breakfast_before_bell_in_any_part_of_dbn_fy18",
    "breakfast_before_bell_y_breakfast_before_bell_in_any_part_of_dbn_fy19",
    "breakfast_in_classroom_offered_y_bic_in_any_part_of_dbn_fy18",
    "breakfast_in_classroom_offered_y_bic_in_any_part_of_dbn_fy19",
    "grab_go_offered_y_gg_in_any_part_of_dbn_fy18",
    "grab_go_offered_y_gg_in_any_part_of_dbn_fy19",
    "lunches_adp_fy18",
    "lunches_adp_fy19",
    "salad_bar_y_salad_bar_offered_in_building_fy18",
    "salad_bar_y_salad_bar_offered_in_building_fy19",
    "snacks_adp_fy18",
    "snacks_adp_fy19",
    "suppers_adp_fy18",
    "suppers_adp_fy19"
FROM "nyc-open-data-biv6-d9zt"
