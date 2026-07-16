-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Woningtype" AS woningtype,
    "Gebruiksoppervlakte" AS gebruiksoppervlakte,
    "Bouwjaar" AS bouwjaar,
    "Bewonersklasse" AS bewonersklasse,
    "HoofdverwarmingEnZonnestroom" AS hoofdverwarmingenzonnestroom,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85140ned"
