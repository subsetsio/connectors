-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CaribischNederland" AS caribischnederland,
    "Perioden" AS perioden,
    "TotaalHuishoudensEnBedrijven_1" AS totaalhuishoudensenbedrijven_1,
    "Totaal_2" AS totaal_2,
    "Prepaid_3" AS prepaid_3,
    "Postpaid_4" AS postpaid_4,
    "Bedrijven_5" AS bedrijven_5,
    "Totaal_6" AS totaal_6,
    "Fossiel_7" AS fossiel_7,
    "Hernieuwbaar_8" AS hernieuwbaar_8,
    "Oliedoorvoer_9" AS oliedoorvoer_9,
    "TotaalHuishoudensEnBedrijven_10" AS totaalhuishoudensenbedrijven_10,
    "Huishoudens_11" AS huishoudens_11,
    "Bedrijven_12" AS bedrijven_12,
    "Productie_13" AS productie_13,
    "CaribischNederland_label" AS caribischnederland_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81154ned"
