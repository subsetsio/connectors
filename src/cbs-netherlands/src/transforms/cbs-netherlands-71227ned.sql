-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AshoogtenWindmolens" AS ashoogtenwindmolens,
    "Perioden" AS perioden,
    "InGebruikGenomenWindmolens_1" AS ingebruikgenomenwindmolens_1,
    "UitGebruikGenomenWindmolens_2" AS uitgebruikgenomenwindmolens_2,
    "OpgesteldeWindmolensEindeVanJaar_3" AS opgesteldewindmolenseindevanjaar_3,
    "InGebruikGenomenRotoroppervlak_4" AS ingebruikgenomenrotoroppervlak_4,
    "UitGebruikGenomenRotoroppervlak_5" AS uitgebruikgenomenrotoroppervlak_5,
    "OpgesteldRotoroppervlakEindeJaar_6" AS opgesteldrotoroppervlakeindejaar_6,
    "InGebruikGenomenVemogen_7" AS ingebruikgenomenvemogen_7,
    "UitGebruikGenomenVermogen_8" AS uitgebruikgenomenvermogen_8,
    "OpgesteldVermogenEindeJaar_9" AS opgesteldvermogeneindejaar_9,
    "Elektriciteitsproductie_10" AS elektriciteitsproductie_10,
    "Productiefactor_11" AS productiefactor_11,
    "ProductiePerRotoroppervlak_12" AS productieperrotoroppervlak_12,
    "AantalVollasturen_13" AS aantalvollasturen_13,
    "AshoogtenWindmolens_label" AS ashoogtenwindmolens_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71227ned"
