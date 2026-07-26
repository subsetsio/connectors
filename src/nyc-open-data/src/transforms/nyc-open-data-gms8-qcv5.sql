-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permit_tag_num",
    "permit_effective_date",
    "permit_expiration_date",
    "permit_status",
    "lost_app_vehicle_stolen",
    "appl_date",
    "appl_status"
FROM "nyc-open-data-gms8-qcv5"
