-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "DiplomaOpPeilmoment" AS diplomaoppeilmoment,
    "Geslacht" AS geslacht,
    "Herkomstkenmerken" AS herkomstkenmerken,
    "DefinitiefSchooladvies" AS definitiefschooladvies,
    "OnderwijspositieOpPeilmoment" AS onderwijspositieoppeilmoment,
    "Startjaar" AS startjaar,
    "Peilmoment" AS peilmoment,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85534ned"
