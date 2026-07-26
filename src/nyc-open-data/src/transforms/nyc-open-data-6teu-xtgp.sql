-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inmateid",
    "admitted_dt",
    "discharged_dt",
    "race",
    "gender",
    "inmate_status_code",
    "top_charge"
FROM "nyc-open-data-6teu-xtgp"
