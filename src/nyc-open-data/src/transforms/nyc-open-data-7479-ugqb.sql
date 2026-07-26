-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inmateid",
    "admitted_dt",
    "discharged_dt",
    "custody_level",
    "bradh",
    "race",
    "gender",
    "age",
    "inmate_status_code",
    "sealed",
    "srg_flg",
    "top_charge",
    "infraction"
FROM "nyc-open-data-7479-ugqb"
