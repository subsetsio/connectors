-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "basketid",
    "baskettype",
    "direction",
    "location_description",
    "ownertype",
    "section",
    "stateplane_labelx",
    "stateplane_labely",
    "stateplane_snappedx",
    "stateplane_snappedy",
    "streetname1",
    "streetname2",
    "objectid",
    "point"
FROM "nyc-open-data-8znf-7b2c"
