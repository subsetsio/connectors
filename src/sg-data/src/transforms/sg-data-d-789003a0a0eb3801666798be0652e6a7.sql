-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Coefficient" AS coefficient,
    "PrimaryInput_Importsofgoodsandservices" AS primaryinput_importsofgoodsandservices,
    "PrimaryInput_Taxeslesssubsidiesonproducts" AS primaryinput_taxeslesssubsidiesonproducts,
    "PrimaryInput_Compensationofemployees" AS primaryinput_compensationofemployees,
    "PrimaryInput_Othertaxeslesssubsidiesonproduction" AS primaryinput_othertaxeslesssubsidiesonproduction,
    "PrimaryInput_Grossoperatingsurplus" AS primaryinput_grossoperatingsurplus,
    "PrimaryInput_Total" AS primaryinput_total
FROM "sg-data-d-789003a0a0eb3801666798be0652e6a7"
