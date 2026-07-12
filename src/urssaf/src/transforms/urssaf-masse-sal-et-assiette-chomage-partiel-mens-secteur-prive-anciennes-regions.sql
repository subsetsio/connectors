-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ancienne_region",
    "dernier_jour_du_mois",
    "code_ancienne_region",
    "masse_salariale_brute",
    "glissement_annuel_masse_salariale",
    "assiette_chomage_partiel",
    "part_assiette_chomage_partiel"
FROM "urssaf-masse-sal-et-assiette-chomage-partiel-mens-secteur-prive-anciennes-regions"
