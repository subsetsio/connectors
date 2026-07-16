-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Geslacht" AS geslacht,
    "LeeftijdPersoon" AS leeftijdpersoon,
    "Persoonskenmerken" AS persoonskenmerken,
    "HemelsbredeAfstandTotOuder" AS hemelsbredeafstandtotouder,
    "GeslachtInNederlandWonendeOuder" AS geslachtinnederlandwonendeouder,
    "RegioS" AS regios,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-83246ned"
