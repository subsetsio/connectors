-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Regions" AS regions,
    "Periods" AS periods,
    "TotalSurface_1" AS totalsurface_1,
    "TransportTotal_2" AS transporttotal_2,
    "Railroad_3" AS railroad_3,
    "MainRoad_4" AS mainroad_4,
    "Airport_5" AS airport_5,
    "BuiltUpAreaTotal_6" AS builtupareatotal_6,
    "Residential_7" AS residential_7,
    "IndustryBusinessPublicInstitutions_8" AS industrybusinesspublicinstitutions_8,
    "SocioCulturalFacilities_9" AS socioculturalfacilities_9,
    "SemiBuiltUpAreaTotal_10" AS semibuiltupareatotal_10,
    "MiningArea_11" AS miningarea_11,
    "BuildingSite_12" AS buildingsite_12,
    "OtherSemiBuiltUpArea_13" AS othersemibuiltuparea_13,
    "RecreationTotal_14" AS recreationtotal_14,
    "ParkAndPublicGarden_15" AS parkandpublicgarden_15,
    "SportGrounds_16" AS sportgrounds_16,
    "OtherRecreationUsage_17" AS otherrecreationusage_17,
    "AgricultureTotal_18" AS agriculturetotal_18,
    "Greenhouses_19" AS greenhouses_19,
    "OtherAgriculturalUsage_20" AS otheragriculturalusage_20,
    "WoodlandAndNatureTotal_21" AS woodlandandnaturetotal_21,
    "Woodland_22" AS woodland_22,
    "NaturalOpenArea_23" AS naturalopenarea_23,
    "WaterTotal_24" AS watertotal_24,
    "InlandWaterTotal_25" AS inlandwatertotal_25,
    "TidalWaterTotal_26" AS tidalwatertotal_26,
    "Regions_label" AS regions_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-37105eng"
