-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TijdelijkNietBeschikbaar" AS tijdelijknietbeschikbaar,
    "TijdelijkNietBeschikbaar_1" AS tijdelijknietbeschikbaar_1,
    "TijdelijkNietBeschikbaar_2" AS tijdelijknietbeschikbaar_2,
    "TijdelijkNietBeschikbaar_label" AS tijdelijknietbeschikbaar_label
FROM "cbs-netherlands-84528ned"
