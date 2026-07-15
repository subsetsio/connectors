-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "buildingname",
    "buildingaddress",
    "buildingtype",
    "greenmarkstatus",
    "greenmarkrating",
    "greenmarkyearaward",
    "buildingsize",
    "grossfloorarea",
    "2017energyuseintensity",
    "2018energyusintensity",
    "voluntarydisclosure"
FROM "sg-data-d-16e7a5921aef24f610f808b16d1480ce"
