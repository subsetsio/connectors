-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grand_secteur_d_activite",
    "secteur_na17",
    "secteur_na38",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "masse_salariale_brute",
    "glissement_annuel_de_la_ms",
    "assiette_chomage_partiel",
    "part_assiette_chomage_partiel"
FROM "urssaf-assiette-chomage-partiel-trimestrielle-du-secteur-prive-par-na38"
