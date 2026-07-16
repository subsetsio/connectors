-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Goederenstromen" AS goederenstromen,
    "HerkomstBestemmingLadenLossen" AS herkomstbestemmingladenlossen,
    "WerelddelenEnLandengroepen" AS werelddelenenlandengroepen,
    "Goederengroepen" AS goederengroepen,
    "Vervoerwijzen" AS vervoerwijzen,
    "Containervervoer" AS containervervoer,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-84668eng"
