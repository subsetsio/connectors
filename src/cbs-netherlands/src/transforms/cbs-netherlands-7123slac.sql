-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Slachtdieren" AS slachtdieren,
    "Perioden" AS perioden,
    "AantalSlachtingen_1" AS aantalslachtingen_1,
    "GeslachtGewicht_2" AS geslachtgewicht_2,
    "Slachtdieren_label" AS slachtdieren_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-7123slac"
