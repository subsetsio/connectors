-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "TotaalTechnologischeInnovatoren_1" AS totaaltechnologischeinnovatoren_1,
    "AandeelVanDeOnderzoekspopulatie_2" AS aandeelvandeonderzoekspopulatie_2,
    "TotaalTechnologischeInnovatoren_3" AS totaaltechnologischeinnovatoren_3,
    "Productinnovatoren_4" AS productinnovatoren_4,
    "Procesinnovatoren_5" AS procesinnovatoren_5,
    "SamenwerkendeInnovatoren_6" AS samenwerkendeinnovatoren_6,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80066ned"
