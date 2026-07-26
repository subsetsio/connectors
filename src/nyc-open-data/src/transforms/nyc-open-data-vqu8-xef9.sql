-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "order_number",
    "borough",
    "on_street",
    "from_street",
    "to_street",
    "side_of_the_street",
    "sign_description",
    "relief_stand",
    "space_count",
    "shape_length"
FROM "nyc-open-data-vqu8-xef9"
