-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_name",
    "first_and_last_name_1",
    "what_year_did_your_honoree_1_move_on_the_block_or_in_your_building",
    "first_and_last_name_2",
    "what_year_did_your_honoree_2_move_on_the_block_or_in_your_building",
    "first_and_last_name_3",
    "what_year_did_your_honoree_3_move_on_the_block_or_in_your_building",
    "first_and_last_extra_name",
    "what_year_did_your_honoree_extra_move_on_the_block_or_in_your_building"
FROM "nyc-open-data-ajh7-4wqg"
