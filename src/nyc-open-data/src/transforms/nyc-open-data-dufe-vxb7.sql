-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tri_incident_number",
    "subject_injury_level",
    "subject_injured",
    "age",
    "subject_race",
    "subject_gender",
    "force_against_mos",
    "subject_used_force"
FROM "nyc-open-data-dufe-vxb7"
