-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LOCODE_PORT" AS locode_port,
    "PORT" AS port,
    "FACADE" AS facade,
    "CODE_REGION" AS code_region,
    "REGION" AS region,
    "STATUT" AS statut,
    "MOUV" AS mouv,
    "ANNEE" AS annee,
    "TONNAGE_TOT" AS tonnage_tot,
    "MAR_TOT" AS mar_tot,
    "TARE_TOT" AS tare_tot,
    "VRACS_LIQUIDES" AS vracs_liquides,
    "BRUT" AS brut,
    "RAFFINE" AS raffine,
    "GAZ_NATUREL" AS gaz_naturel,
    "AUTRES_VRACS_L" AS autres_vracs_l,
    "VRACS_SOLIDES" AS vracs_solides,
    "CEREALES" AS cereales,
    "NOUR_ANIMALES" AS nour_animales,
    "CHARBON" AS charbon,
    "MINERAIS" AS minerais,
    "ENGRAIS" AS engrais,
    "AUTRES_VRACS_S" AS autres_vracs_s,
    "CONT_TOT" AS cont_tot,
    "CONT_MAR" AS cont_mar,
    "CONT_TARE" AS cont_tare,
    "RORO_TOT" AS roro_tot,
    "RORO_MAR" AS roro_mar,
    "RORO_TARE" AS roro_tare,
    "RORO_TOURISME" AS roro_tourisme,
    "AUTRE_MAR_DIV" AS autre_mar_div,
    "EVP_TOT" AS evp_tot
FROM "sdes-89c4e831-27ae-4fe7-8ff7-d6c82fa4a841"
