-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Misdrijven" AS misdrijven,
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "Verblijfstitel" AS verblijfstitel,
    "Strafduur" AS strafduur,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85841ned"
