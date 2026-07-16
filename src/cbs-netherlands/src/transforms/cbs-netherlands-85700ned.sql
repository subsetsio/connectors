-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "UitstromersMboMetEnZonderDiploma" AS uitstromersmbometenzonderdiploma,
    "Uitkeringen" AS uitkeringen,
    "Studierichting" AS studierichting,
    "Peilmoment" AS peilmoment,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85700ned"
