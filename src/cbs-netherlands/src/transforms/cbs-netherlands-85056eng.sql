-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Verplaatsingskenmerken" AS verplaatsingskenmerken,
    "Populatie" AS populatie,
    "Vervoerwijzen" AS vervoerwijzen,
    "Marges" AS marges,
    "Regiokenmerken" AS regiokenmerken,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85056eng"
