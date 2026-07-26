-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "projectid",
    "buildingid",
    "bedroomsize",
    "maxallowableincome",
    "totalunits",
    "medianinitiallegalrent",
    "highinitiallegalrent",
    "lowinitiallegalrent",
    "medianactualrent",
    "highactualrent",
    "lowactualrent"
FROM "nyc-open-data-9ay9-xkek"
