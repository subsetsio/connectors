-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sectors" AS sectors,
    "CombinedHeatAndPowerCHP" AS combinedheatandpowerchp,
    "InstallationTypes" AS installationtypes,
    "Periods" AS periods,
    "TotalInput_1" AS totalinput_1,
    "NaturalGasInput_2" AS naturalgasinput_2,
    "FuelOilInput_3" AS fueloilinput_3,
    "HardCoalInput_4" AS hardcoalinput_4,
    "OtherFuelInput_5" AS otherfuelinput_5,
    "TotalInput_6" AS totalinput_6,
    "NaturalGasInput_7" AS naturalgasinput_7,
    "FuelOilInput_8" AS fueloilinput_8,
    "HardCoalInput_9" AS hardcoalinput_9,
    "OtherFuelInput_10" AS otherfuelinput_10,
    "TotalOutput_11" AS totaloutput_11,
    "ElectricityOutput_12" AS electricityoutput_12,
    "HeatOutput_13" AS heatoutput_13,
    "TotalOutput_14" AS totaloutput_14,
    "ElectricityOutput_15" AS electricityoutput_15,
    "HeatOutput_16" AS heatoutput_16,
    "ElectricalPower_17" AS electricalpower_17,
    "ThermalPower_18" AS thermalpower_18,
    "Installations_19" AS installations_19,
    "Sectors_label" AS sectors_label,
    "CombinedHeatAndPowerCHP_label" AS combinedheatandpowerchp_label,
    "InstallationTypes_label" AS installationtypes_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-37823eng"
