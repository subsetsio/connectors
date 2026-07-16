-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "TotalEnergySupplyTPES_1" AS totalenergysupplytpes_1,
    "IndigenousProductionTotal_2" AS indigenousproductiontotal_2,
    "IndigenousProductionHardCoal_3" AS indigenousproductionhardcoal_3,
    "IndigenousProductionLignite_4" AS indigenousproductionlignite_4,
    "Imports_5" AS imports_5,
    "Exports_6" AS exports_6,
    "Bunkers_7" AS bunkers_7,
    "StockChange_8" AS stockchange_8,
    "PatentFuelOutput_9" AS patentfueloutput_9,
    "OutputTotal_10" AS outputtotal_10,
    "ManufactureOfCokeOvenProductsOutput_11" AS manufactureofcokeovenproductsoutput_11,
    "OutputOther_12" AS outputother_12,
    "OutputByPublicGasWorksCompanies_13" AS outputbypublicgasworkscompanies_13,
    "DeliveryByEnergyCompanies_14" AS deliverybyenergycompanies_14,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-71554eng"
