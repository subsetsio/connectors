-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Leeftijden" AS leeftijden,
    "Perioden" AS perioden,
    "PersonenMetEenBetalingsachterstand_1" AS personenmeteenbetalingsachterstand_1,
    "PersMetBetalingsachterstandRelatief_2" AS persmetbetalingsachterstandrelatief_2,
    "Geslacht_label" AS geslacht_label,
    "Leeftijden_label" AS leeftijden_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81062ned"
