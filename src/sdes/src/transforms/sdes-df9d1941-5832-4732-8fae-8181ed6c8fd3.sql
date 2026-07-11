-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ANNEE" AS annee,
    "REGION_CODE" AS region_code,
    "REGION_LIBELLE" AS region_libelle,
    "NB_EPL" AS nb_epl,
    "NB_AIRES" AS nb_aires,
    "SURFACE" AS surface,
    "DENSITE" AS densite,
    "PART_ENTREPOSAGE" AS part_entreposage,
    "PART_TRANSPORT_LOGISTIQUE" AS part_transport_logistique,
    "PART_INDUSTRIE" AS part_industrie,
    "PART_COMMERCE_GROS" AS part_commerce_gros,
    "PART_COMMERCE_DETAIL_AUTO" AS part_commerce_detail_auto,
    "PART_AUTRE" AS part_autre
FROM "sdes-df9d1941-5832-4732-8fae-8181ed6c8fd3"
