-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "LeeftijdOp31December" AS leeftijdop31december,
    "VolgordeVanGeboorteUitDeMoeder" AS volgordevangeboorteuitdemoeder,
    "GeboortegeneratieVrouw" AS geboortegeneratievrouw,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85750ned"
