-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "district",
    "breakfast_before_bell_adp_fy19",
    "breakfast_before_bell_adp_fy20",
    "breakfast_in_classroom_adp_fy19",
    "breakfast_in_classroom_adp_fy20",
    "breakfast_before_bell_by_dbn_fy19",
    "breakfast_before_bell_by_dbn_fy20",
    "breakfast_in_classroom_offered_by_dbn_fy19",
    "breakfast_in_classroom_offered_by_dbn_fy20",
    "grab_go_offered_by_dbn_fy19",
    "grab_go_offered_by_dbn_fy20",
    "lunches_adp_fy19",
    "lunches_adp_fy20",
    "salad_bar_count_of_unique_bldg_code_fy19",
    "salad_bar_count_of_unique_bldg_code_fy20",
    "after_school_snacks_adp_fy19",
    "after_school_snacks_adp_fy20",
    "after_school_suppers_adp_fy19",
    "after_school_suppers_adp_fy20"
FROM "nyc-open-data-756x-9djt"
