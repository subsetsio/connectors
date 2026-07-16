-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "WaterBoards" AS waterboards,
    "Periods" AS periods,
    "WaterSystemLevyResidents_1" AS watersystemlevyresidents_1,
    "WaterSystemLevyUnbuiltOnLand_2" AS watersystemlevyunbuiltonland_2,
    "WaterSystemLevyNatureAreas_3" AS watersystemlevynatureareas_3,
    "WaterSystemLevyBuiltUpLand_4" AS watersystemlevybuiltupland_4,
    "BuiltUpLandDwellings_5" AS builtuplanddwellings_5,
    "BuiltUpLandNonResidentialBuildings_6" AS builtuplandnonresidentialbuildings_6,
    "RoadLevyUnbuiltOnLand_7" AS roadlevyunbuiltonland_7,
    "RoadLevyForResidents_8" AS roadlevyforresidents_8,
    "RoadLevyNatureAreas_9" AS roadlevynatureareas_9,
    "RoadLevyBuiltUpLand_10" AS roadlevybuiltupland_10,
    "BuiltUpLandDwellings_11" AS builtuplanddwellings_11,
    "LandNonResidentialBuildings_12" AS landnonresidentialbuildings_12,
    "NonTaskRelatedLevyForResidents_13" AS nontaskrelatedlevyforresidents_13,
    "NonTaskRelatedLevyUnbuiltOnLand_14" AS nontaskrelatedlevyunbuiltonland_14,
    "NonTaskRelatedLevyNatureAreas_15" AS nontaskrelatedlevynatureareas_15,
    "NonTaskRelatedLevyBuiltUpLand_16" AS nontaskrelatedlevybuiltupland_16,
    "WastewaterTreatmentLevy_17" AS wastewatertreatmentlevy_17,
    "PollutionLevy_18" AS pollutionlevy_18,
    "WaterBoards_label" AS waterboards_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80892eng"
