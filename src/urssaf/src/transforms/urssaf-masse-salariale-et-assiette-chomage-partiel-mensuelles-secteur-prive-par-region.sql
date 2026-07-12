-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "dernier_jour_du_mois",
    "code_region",
    "masse_salariale_brute",
    "glissement_annuel_masse_salariale",
    "assiette_chomage_partiel",
    "part_assiette_chomage_partiel"
FROM "urssaf-masse-salariale-et-assiette-chomage-partiel-mensuelles-secteur-prive-par-region"
