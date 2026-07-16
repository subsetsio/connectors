-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Id" AS id,
    "Measure" AS measure,
    "Populatie" AS populatie,
    "KenmerkenVanDeSchenking" AS kenmerkenvandeschenking,
    "KenmerkenVanDeSchenker" AS kenmerkenvandeschenker,
    "KenmerkenVanDeOntvanger" AS kenmerkenvandeontvanger,
    "Perioden" AS perioden,
    "Value" AS value,
    "StringValue" AS stringvalue,
    "ValueAttribute" AS valueattribute
FROM "cbs-netherlands-84465eng"
