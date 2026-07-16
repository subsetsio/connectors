-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SOKlassen" AS soklassen,
    "Bedrijfstypen" AS bedrijfstypen,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "AantalBedrijven_1" AS aantalbedrijven_1,
    "EconomischeOmvangSO_2" AS economischeomvangso_2,
    "OppervlakteCultuurgrond_3" AS oppervlaktecultuurgrond_3,
    "SOKlassen_label" AS soklassen_label,
    "Bedrijfstypen_label" AS bedrijfstypen_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80786ned"
