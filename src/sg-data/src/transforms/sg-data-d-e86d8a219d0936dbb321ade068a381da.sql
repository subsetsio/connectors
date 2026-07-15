-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "buildingname",
    "buildingaddress",
    "buildingtype",
    "mainbuildingfunction",
    "buildingsize",
    "yearobtainedtopcsc",
    "greenmarkrating",
    "greenmarkyearofaward",
    "greenmarkversion",
    "grossfloorarea",
    "percentageofairconditionedfloorarea",
    "averagemonthlybuildingoccupancyrate",
    "numberofhotelrooms",
    "typeofairconditioningsystem",
    "ageofchiller",
    "centralisedairconditioningplantefficiency",
    "yearoflastchillerplantaudithealthcheck",
    "percentageusageofled",
    "installationofsolarpv",
    "2017",
    "2018",
    "2019",
    "2020"
FROM "sg-data-d-e86d8a219d0936dbb321ade068a381da"
