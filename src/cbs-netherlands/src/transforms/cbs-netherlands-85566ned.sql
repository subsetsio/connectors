-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Geslacht" AS geslacht,
    "OnderwijsPositieBasisjaar" AS onderwijspositiebasisjaar,
    "OnderwijsPositieVolgendSchooljaar" AS onderwijspositievolgendschooljaar,
    "GeboortelandOuders" AS geboortelandouders,
    "Herkomstland" AS herkomstland,
    "Regiokenmerken" AS regiokenmerken,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85566ned"
