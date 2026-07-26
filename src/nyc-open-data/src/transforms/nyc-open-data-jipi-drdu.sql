-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_name",
    "honorees_first_name_cornerstone_award_1",
    "honorees_last_name_cornerstone_award_1",
    "what_year_did_your_honoree_move_on_the_block_or_in_your_building",
    "honorees_first_name_cornerstone_award_2",
    "honorees_last_name_cornerstone_award_2",
    "what_year_did_your_honoree_2_move_on_the_block_or_in_your_building",
    "honorees_first_name_cornerstone_award_3",
    "honorees_last_name_cornerstone_award_3",
    "what_year_did_your_honoree_3_move_on_the_block_or_in_your_building",
    "first_name_extra",
    "last_name_extra",
    "year_extra"
FROM "nyc-open-data-jipi-drdu"
