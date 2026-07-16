-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AantalSporen" AS aantalsporen,
    "RegioS" AS regios,
    "SpoorwegenSoort" AS spoorwegensoort,
    "Perioden" AS perioden,
    "LengteSpoorwegtraject_1" AS lengtespoorwegtraject_1,
    "AantalSporen_label" AS aantalsporen_label,
    "RegioS_label" AS regios_label,
    "SpoorwegenSoort_label" AS spoorwegensoort_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71024ned"
