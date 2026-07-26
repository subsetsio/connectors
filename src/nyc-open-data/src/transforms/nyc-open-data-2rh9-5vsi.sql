-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "agency_name",
    "servicename",
    "goal",
    "goal_description"
FROM "nyc-open-data-2rh9-5vsi"
