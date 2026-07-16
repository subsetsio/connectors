-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Geslacht" AS geslacht,
    "Niveau" AS niveau,
    "Leerweg" AS leerweg,
    "Sectorkamer" AS sectorkamer,
    "Persoonskenmerken" AS persoonskenmerken,
    "MaatschappelijkePositie1JaarEerder" AS maatschappelijkepositie1jaareerder,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-85569ned"
