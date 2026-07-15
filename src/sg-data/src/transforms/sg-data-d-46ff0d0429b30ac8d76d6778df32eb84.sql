-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "FloorAreaofResidence_60sqm" AS floorareaofresidence_60sqm,
    "FloorAreaofResidence_60to80sqm" AS floorareaofresidence_60to80sqm,
    "FloorAreaofResidence_80to100sqm" AS floorareaofresidence_80to100sqm,
    "FloorAreaofResidence_100to120sqm" AS floorareaofresidence_100to120sqm,
    "FloorAreaofResidence_120sqm" AS floorareaofresidence_120sqm,
    "NumberofPersonsinHouseholds" AS numberofpersonsinhouseholds,
    "MeanFloorAreaperPerson_sqm" AS meanfloorareaperperson_sqm,
    "MedianFloorAreaperPerson_sqm" AS medianfloorareaperperson_sqm
FROM "sg-data-d-46ff0d0429b30ac8d76d6778df32eb84"
