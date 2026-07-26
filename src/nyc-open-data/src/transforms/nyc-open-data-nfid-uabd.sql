-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "order_number",
    "record_type",
    "order_type",
    "borough",
    "on_street",
    "on_street_suffix",
    "from_street",
    "from_street_suffix",
    "to_street",
    "to_street_suffix",
    "side_of_street",
    "order_completed_on_date",
    "sign_code",
    "sign_description",
    "sign_size",
    "sign_design_voided_on_date",
    "sign_location",
    "distance_from_intersection",
    "arrow_direction",
    "facing_direction",
    "sheeting_type",
    "support",
    "sign_notes",
    "sign_x_coord",
    "sign_y_coord"
FROM "nyc-open-data-nfid-uabd"
