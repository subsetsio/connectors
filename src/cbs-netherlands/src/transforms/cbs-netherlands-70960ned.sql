-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "InGebruikGenomenWindmolens_1" AS ingebruikgenomenwindmolens_1,
    "UitGebruikGenomenWindmolens_2" AS uitgebruikgenomenwindmolens_2,
    "OpgesteldeWindmolensEindeVanJaar_3" AS opgesteldewindmolenseindevanjaar_3,
    "InGebruikGenomenRotoroppervlak_4" AS ingebruikgenomenrotoroppervlak_4,
    "UitGebruikGenomenRotoroppervlak_5" AS uitgebruikgenomenrotoroppervlak_5,
    "OpgesteldRotoroppervlakEindeJaar_6" AS opgesteldrotoroppervlakeindejaar_6,
    "InGebruikGenomenVermogen_7" AS ingebruikgenomenvermogen_7,
    "UitGebruikGenomenVermogen_8" AS uitgebruikgenomenvermogen_8,
    "OpgesteldVermogenEindeJaar_9" AS opgesteldvermogeneindejaar_9,
    "GenormaliseerdeProductie_10" AS genormaliseerdeproductie_10,
    "NietGenormaliseerdeProductie_11" AS nietgenormaliseerdeproductie_11,
    "Productiefactor_12" AS productiefactor_12,
    "ProductiePerRotoroppervlak_13" AS productieperrotoroppervlak_13,
    "AantalVollasturen_14" AS aantalvollasturen_14,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70960ned"
