-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Coefficient" AS coefficient,
    "Imports_TaxesOnProductsAndPrimaryInputs_Importsofgoodsandservic" AS imports_taxesonproductsandprimaryinputs_importsofgoodsandservic,
    "Imports_TaxesOnProductsAndPrimaryInputs_Importduties" AS imports_taxesonproductsandprimaryinputs_importduties,
    "Imports_TaxesOnProductsAndPrimaryInputs_Taxesonproducts" AS imports_taxesonproductsandprimaryinputs_taxesonproducts,
    "Imports_TaxesOnProductsAndPrimaryInputs_Othertaxeslesssubsidies" AS imports_taxesonproductsandprimaryinputs_othertaxeslesssubsidies,
    "Imports_TaxesOnProductsAndPrimaryInputs_Compensationofemployees" AS imports_taxesonproductsandprimaryinputs_compensationofemployees,
    "Imports_TaxesOnProductsAndPrimaryInputs_Grossoperatingsurplus" AS imports_taxesonproductsandprimaryinputs_grossoperatingsurplus,
    "Imports_TaxesOnProductsAndPrimaryInputs_Finaldemand" AS imports_taxesonproductsandprimaryinputs_finaldemand
FROM "sg-data-d-ccf955c3647b52732fefc29d31662cf9"
