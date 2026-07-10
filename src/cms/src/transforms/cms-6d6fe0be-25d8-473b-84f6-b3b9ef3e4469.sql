-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Name of Initiative" AS name_of_initiative,
    "Participant Name" AS participant_name,
    "Geographic Reach" AS geographic_reach,
    "Location" AS location,
    "Participant's Organization" AS participant_s_organization,
    "City" AS city,
    "State" AS state
FROM "cms-6d6fe0be-25d8-473b-84f6-b3b9ef3e4469"
