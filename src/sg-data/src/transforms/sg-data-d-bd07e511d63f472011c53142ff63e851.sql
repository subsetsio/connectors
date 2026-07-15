-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "residential_status",
    "user_type",
    "no._solar_pv_inst." AS no_solar_pv_inst
FROM "sg-data-d-bd07e511d63f472011c53142ff63e851"
