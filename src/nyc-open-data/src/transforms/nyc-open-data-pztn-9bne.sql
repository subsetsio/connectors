-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "incident_key",
    "victim_id",
    "victim_age_group",
    "victim_sex",
    "victim_race",
    "stat_murder_flg"
FROM "nyc-open-data-pztn-9bne"
