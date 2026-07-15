-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Coefficient" AS coefficient,
    "Importsofgoodsandservices_Direct" AS importsofgoodsandservices_direct,
    "Importsofgoodsandservices_Indirect" AS importsofgoodsandservices_indirect,
    "Importsofgoodsandservices_Total" AS importsofgoodsandservices_total
FROM "sg-data-d-bc5000f7e912a412da1ddafa593ae826"
